from pydantic import BaseModel, validator, Field
from datetime import datetime


class BaseParams(BaseModel):
    partners: set[str] | None = Field(
        default=None,
        title='Bank partner',
        description='Partners in the report'
    )
    years: set[int] | None = Field(
        default=None,
        title='Years',
        description='The report is generated for the period of years'
    )
    months: set[int] | None = Field(
        default=None,
        title='Months',
        description='The report is generated for the period of months'
    )
    days: bool = Field(
        default=False,
        title='Report mode',
        description='Day of the week report'
    )
    aggr: str = Field(
        default='count',
        title='Aggregation method',
        description='Aggregation method in the report'
    )

    @validator("partners")
    @classmethod
    def validate_partner(cls, partners: set[str] | None) -> set[str] | None:
        if not partners:
            return None
        validate_partners = set()
        excepted_partners = {'rosbank': 'Росбанк', 'setelem': 'Драйв Клик'}
        for partner in partners:
            if partner not in excepted_partners:
                raise ValueError(f'Wrong name partner <{partner}>')
            validate_partners.add(excepted_partners.get(partner))
        return validate_partners

    @validator("years")
    @classmethod
    def validate_years(cls, years: set[int] | None) -> set[int] | None:
        if not years:
            return None
        for year in years:
            if year < 2020:
                raise ValueError(f"Year can't be less than 2020")
            if year > datetime.now().year:
                raise ValueError(f"Year can't be more than current year")
        return years

    @validator("months")
    @classmethod
    def validate_months(cls, months: set[int]) -> set[int] | None:
        if not months:
            return months
        for month in months:
            if month not in set(range(1, 13)):
                raise ValueError(f"Wrong month number - <{month}>")
        return months

    @validator("aggr")
    @classmethod
    def validate_aggr(cls, aggr: str) -> str:
        excepted_aggregate_func = {'count', 'sum', 'mean', 'median'}
        if aggr not in excepted_aggregate_func:
            raise ValueError(f"Unsupported aggregate function. Choose any from <{excepted_aggregate_func}>")
        return aggr


class HeatmapParams(BaseParams):
    pass


class TimeParams(BaseParams):
    aggr: str = Field(
        default='mean',
        title='Aggregation method',
        description='Aggregation method in the report'
    )
    stage: str | None = Field(
        default='funded',
        title='Statement stage',
        description='Report on applications with a completed stage'
    )

    @validator("stage")
    @classmethod
    def validate_stage(cls, stage: str) -> str:
        excepted_stage = {'pre_approved', 'approved', 'funded'}
        if stage not in excepted_stage:
            raise ValueError(f"Unsupported stage. Choose any from <{excepted_stage}>")
        return stage
