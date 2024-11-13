import asyncio
import traceback
from typing import Optional, List
import httpx
import humanize

from bums.endpoints import Endpoints
from bums.models import Mine
from env import Env
from telegram.client import TGClient
from telegram.platform import Platform
from fake_useragent import UserAgent
from utils.loggy import logger

import hashlib


class Bums:
    def __init__(
        self,
        peer_id: str,
        http_timeout: float = 120,
        platform: Platform = Platform.ANDROID,
    ) -> None:
        self.peer_id: str = peer_id
        self.client: httpx.AsyncClient = httpx.AsyncClient(
            timeout=http_timeout,
            headers={"User-Agent": UserAgent(os=platform.value).random},
        )

    async def _post(self, url: str, data: dict) -> Optional[httpx.Response]:
        try:
            return await self.client.post(url, data=data)
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Request to {url} failed with status {e.response.status_code}"
            )
            logger.error(traceback.print_exc())
        except Exception as e:
            logger.error(f"Request to {url} failed: {str(e)}")
            logger.error(traceback.print_exc())

    async def _get(self, url: str) -> Optional[httpx.Response]:
        try:
            return await self.client.get(url)
        except httpx.HTTPStatusError as e:
            logger.error(
                f"GET request to {url} failed with status {e.response.status_code}"
            )
        except Exception as e:
            logger.error(f"GET request to {url} failed: {str(e)}")
            logger.error(traceback.print_exc())

    def _generate_md5_hash(self, collect_amount: int, collect_seq_no: int) -> str:
        hash_key: str = "7be2a16a82054ee58398c5edb7ac4a5a"
        return hashlib.md5(
            f"{collect_amount}{collect_seq_no}{hash_key}".encode()
        ).hexdigest()

    async def _get_minelist(self) -> List[Mine]:
        response: Optional[httpx.Response] = await self._post(
            Endpoints.MINE_LIST_URL, {}
        )
        if response is None:
            return []
        lists = response.json().get("data", {}).get("lists", [])
        if not lists:
            logger.warning("Unable to get mine lists")
            logger.error(response.json())
            return []

        return [Mine(**mine) for mine in lists] if response else []

    async def _get_eligible_minelist(self) -> List[Mine]:
        return [mine for mine in await self._get_minelist() if not mine.limitText]

    def _find_best_mines(self, mines: List[Mine], budget: int) -> List[Mine]:
        affordable_mines: List[Mine] = [
            mine for mine in mines if mine.nextLevelCost <= budget
        ]
        return (
            sorted(
                affordable_mines, key=lambda mine: (mine.nextLevelCost, -mine.distance)
            )
            if affordable_mines
            else []
        )

    async def _get_signlists(self) -> Optional[dict]:
        response = await self._get(Endpoints.SIGN_LISTS_URL)
        return response.json() if response else None

    async def login(self) -> bool:
        self.client.headers.pop("Authorization", None)
        tg_client = TGClient()
        query: str = await tg_client.get_query_string(self.peer_id, short_name="app")
        response: Optional[httpx.Response] = await self._post(
            Endpoints.LOGIN_URL, data={"refCode": Env.REF_ID, "initData": query}
        )
        if not response:
            logger.error("Unable to login")
            logger.error(traceback.print_exc())
            return False

        token = response.json().get("data").get("token")
        if not token:
            logger.error("Unable to Login")
            logger.error(traceback.print_exc())
            logger.error(response.json())
            return False

        if response and response.status_code == 200:
            self.client.headers["Authorization"] = f"Bearer {token}"
            logger.success("Logged in successfully")
            return True
        return False

    async def get_userinfo(self) -> Optional[dict]:
        response: Optional[httpx.Response] = await self._get(Endpoints.GAME_INFO_URL)
        if response and response.status_code == 200:
            return response.json().get("data") if response else None

    async def tap(self, userinfo: dict) -> None:
        energy: int = userinfo["gameInfo"]["energySurplus"]
        collect_seq_no: int = userinfo["tapInfo"]["collectInfo"]["collectSeqNo"]
        resp = await self._post(
            Endpoints.TAP_URL,
            data={
                "collectAmount": energy,
                "collectSeqNo": collect_seq_no,
                "hashCode": self._generate_md5_hash(energy, collect_seq_no),
            },
        )
        if resp and resp.json().get("msg") == "OK":
            logger.success("Tap successful")
        else:
            logger.error("Tap failed")

    async def upgrade_mine(self, mine: Mine) -> bool:
        response: Optional[httpx.Response] = await self._post(
            Endpoints.UPGRADE_URL, data={"mineId": mine.mineId}
        )
        if (
            response
            and response.status_code == 200
            and response.json().get("msg") == "OK"
        ):
            logger.success(f"Upgraded mine {mine.mineId} successfully")
            return True
        return False

    async def process_upgrades(self) -> bool:
        is_upgraded = False
        logger.info("Processing multiple upgrades...")
        userinfo: Optional[dict] = await self.get_userinfo()
        if not userinfo:
            logger.warning("Unable to get user information")
            return False

        money: int = int(userinfo["gameInfo"]["coin"])
        eligible_mines: List[Mine] = await self._get_eligible_minelist()
        logger.info(f"Total Eligible Minelist: {len(eligible_mines)}")

        for best_mine in self._find_best_mines(eligible_mines, money):
            if money >= best_mine.nextLevelCost:
                logger.info(
                    f"Upgrading mine {best_mine.mineId} to level {best_mine.level + 1}"
                )
                await asyncio.sleep(3)
                if await self.upgrade_mine(best_mine):
                    is_upgraded = True
                    money -= best_mine.nextLevelCost
                    logger.info(f"Upgrade successful! Remaining Money: {money}")
            else:
                logger.info(f"Not enough money to upgrade mine {best_mine.mineId}.")
        return is_upgraded

    async def daily_sign(self) -> bool:
        signlists = await self._get_signlists()
        if signlists:
            if signlists.get("msg") == "OK":
                data = signlists.get("data", {})
                if not data:
                    logger.error(signlists)
                    return False
                if data.get("signStatus") != 0:
                    logger.info("Already claimed daily rewards")
                    return True
                resp = await self._post(Endpoints.DAILY_SIGN_URL, {})
                if resp and data.get("msg") == "OK":
                    logger.success("Received reward daily sign rewards")
                    return True
                else:
                    logger.warning("Failed to claim daily reward")
                    logger.error(signlists)
                    return False
            else:
                logger.warning("Unable to claim daily reward")
                logger.error(signlists)
        return False

    async def print_userinfo(self) -> None:
        print()
        logger.info("Getting user information...")
        await asyncio.sleep(3)
        try:
            response = await self.get_userinfo()
            if not response:
                return

            user_info = response["userInfo"]
            game_info = response["gameInfo"]
            tap_info = response["tapInfo"]
            mine_info = response["mineInfo"]
            print()
            logger.info(f"========== {user_info['nickName']} ==========")
            print()
            logger.info(f"ID: {user_info['userId']}")
            logger.info(f"Balance: {humanize.naturalsize(game_info['coin'],gnu=True)}")
            logger.info(
                f"Profit per hour: {humanize.naturalsize(mine_info['minePower'], gnu=True)}"
            )
            logger.info(f"Level: {game_info['level']}")
            logger.info(f"Energy Level: {tap_info['energy']['level']}")
            logger.info(
                f"Energy: {humanize.naturalsize(tap_info['energy']['value'], gnu=True)}"
            )
            print()
        except Exception as error:
            logger.error(f"Error getting user data: {str(error)}")
