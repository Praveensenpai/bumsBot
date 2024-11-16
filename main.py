import asyncio
from contextlib import suppress
from datetime import datetime, timedelta
import time
import traceback
from bums.bums import Bums
from env import Env
from utils.dt import human_readable
from utils.loggy import logger
from timecalculator import TimeCalculator


class BumsBot:
    def __init__(self, concurrency: int = 1) -> None:
        self.semaphore = asyncio.Semaphore(concurrency)
        self.last_sign_in_date = datetime.now().date() - timedelta(days=10)

    async def tap_task(self, bums: Bums, userinfo: dict) -> None:
        try:
            print()
            logger.info("===Tap task started===")
            print()
            await asyncio.sleep(3)
            await bums.tap(userinfo)
            await asyncio.sleep(3)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            logger.error(traceback.format_exc())

    async def daily_signin_task(self, bums: Bums) -> None:
        print()
        logger.info("===Daily Sign-in task started===")
        print()
        if self.last_sign_in_date == datetime.now().date():
            logger.info("Already signed in today, skipping daily sign-in.")
            return

        try:
            await asyncio.sleep(3)
            await bums.daily_sign()
            await asyncio.sleep(3)
            self.last_sign_in_date = datetime.now().date()
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            logger.error(traceback.format_exc())

    async def process_upgrades_task(self, bums: Bums) -> None:
        try:
            print()
            logger.info("===Process Upgrades task started===")
            print()
            await asyncio.sleep(3)
            while True:
                is_upgraded = await bums.process_upgrades()
                if not is_upgraded:
                    logger.info("No more money available to upgrade")
                    return
                logger.info("Let's take 1 minute break and proceed to upgrade another")
                await asyncio.sleep(60)

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            logger.error(traceback.format_exc())

    async def main(self):
        sleep_delay = Env.SLEEP_DELAY_MINUTES
        logger.info(f"SLEEP DELAY SET TO {sleep_delay} MINUTES")
        while True:
            try:
                bums = Bums("bums")
                is_logged = await bums.login()
                if not is_logged:
                    return
                userinfo = await bums.get_userinfo()
                if not userinfo:
                    logger.warning("Unable to get user information")
                    return

                await bums.print_userinfo()
                await self.daily_signin_task(bums)
                await self.tap_task(bums, userinfo)
                await self.process_upgrades_task(bums)
                rest_period = TimeCalculator.MINUTE * sleep_delay
                logger.info(
                    f"Lets take a rest for {human_readable(timedelta(seconds=rest_period))}"
                )
                await asyncio.sleep(rest_period)
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                logger.error(traceback.format_exc())
                logger.info("Let's take a 10 minutes break.")
                await asyncio.sleep(TimeCalculator.MINUTE * 10)

    def run(self):
        while True:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.main())
            except Exception as e:
                logger.error(traceback.format_exc())
                logger.error(f"Restarting event loop due to error: {e}")
            finally:
                with suppress(Exception):
                    loop.close()
                logger.info("Restarting the main loop...")
                time.sleep(10)


if __name__ == "__main__":
    BumsBot().run()
