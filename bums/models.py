from pydantic import BaseModel


class Mine(BaseModel):
    mineId: int
    level: int
    nextLevelCost: int
    perHourReward: int
    nextPerHourReward: int
    distance: int
    status: int
    cateId: int
    limitMineId: int
    limitMineLevel: int
    limitText: str
    limitExperienceLevel: int
    limitInvite: int
