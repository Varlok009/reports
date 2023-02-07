from pydantic import BaseModel, validator
from fastapi.exceptions import HTTPException


class BaseParams(BaseModel):
    partners: set[str] | None = None
    years: set[int] | None = None
    months: set[int] | None = None
    days: bool = False
    aggr: str = 'count'

    @validator("partners")
    @classmethod
    def validate_partners(cls, partners: set[str] | None):
        if not partners:
            return None
        validate_partners = set()
        excepted_partners = {'rosbank': 'Росбанк', 'setelem': 'Драйв Клик'}
        for partner in partners:
            if partner not in excepted_partners:
                raise HTTPException(
                    status_code=400,
                    detail=f"Wrong partner - <{partner}>"
                )
            validate_partners.add(excepted_partners.get(partner))
        return validate_partners

    @validator("months")
    @classmethod
    def validate_months(cls, months):
        if not months:
            return months
        validate_months = set()
        for month in months:
            if month not in set(range(1, 13)):
                raise HTTPException(
                    status_code=400,
                    detail=f"Wrong month number - <{month}>"
                )
            validate_months.add(month)
        return validate_months


class HeatmapParams(BaseParams):
    pass


class TimeParams(BaseParams):
    stage: str | None = 'funded'
    aggr: str = 'mean'
