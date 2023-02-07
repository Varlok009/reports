import uvicorn
from fastapi import FastAPI, Depends, Request, Query
from reports.report import Report
from reports.heatmaps.heatmap_report import HeatmapReport
from reports.time.time_report import TimeReport
from reports.basic.basic_report import BasicReport
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from db.data_base import DataBase as DB

app_reports = FastAPI()
app_reports.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
DB.set_data()


class QueryParams:
    def __init__(self,
                 partners: set[str] | None = Query(default=None),
                 years: set[int] | None = Query(default=None),
                 months: set[int] | None = Query(default=None),
                 days: bool = Query(default=False,
                                    title="Days of the week",
                                    description="Report for days"),
                 aggr: str = Query(default='count')):
        self.partners = None if partners is None else self.validate_partners(partners)
        self.years = years
        self.months = None if months is None else self.validate_months(months)
        self.days = days
        self.aggr = aggr

    @staticmethod
    def validate_partners(partners):
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

    @staticmethod
    def validate_months(months):
        validate_months = set()
        for month in months:
            if month not in set(range(1, 13)):
                raise HTTPException(
                    status_code=400,
                    detail=f"Wrong month number - <{month}>"
                )
            validate_months.add(month)
        return validate_months


class TimeQueryParams(QueryParams):
    def __init__(self,
                 partners: set[str] | None = Query(default=None),
                 years: set[int] | None = Query(default=None),
                 months: set[int] | None = Query(default=None),
                 days: bool = Query(default=False,
                                    title="Days of the week",
                                    description="Report for days"),
                 aggr: str = Query(default='median'),
                 stage: str | None = Query(default='funded')):
        super().__init__(partners, years, months, days, aggr)
        self.stage = stage


@app_reports.get('/')
async def root():
    return {"message": "Hello, this is a reporting api"}


@app_reports.get('/heatmap/credit_report')
async def get_heatmap_credit_report(request: Request, params: QueryParams = Depends()):
    report = HeatmapReport(partners=params.partners, years=params.years,
                           months=params.months, days=params.days, aggr=params.aggr
                           ).get_heatmap_credit_report()
    return templates.TemplateResponse("report.html", {"request": request, "report": report})


@app_reports.get('/heatmap/statement_report')
async def get_heatmap_statement_report(request: Request, params: QueryParams = Depends()):
    report = HeatmapReport(partners=params.partners, years=params.years,
                           months=params.months, days=params.days, aggr=params.aggr
                           ).get_heatmap_statement_report()
    return templates.TemplateResponse("report.html", {"request": request, "report": report})


@app_reports.get('/time')
async def get_time_report(request: Request, params: TimeQueryParams = Depends()):
    report = TimeReport(partners=params.partners, years=params.years,
                        months=params.months, days=params.days, aggr=params.aggr,
                        stage=params.stage
                        ).get_time_report()
    return templates.TemplateResponse("report.html", {"request": request, "report": report})

# @app_reports.get('/basic/bid_report', response_class=FileResponse)
# async def get_basic_bid_report(params: QueryParams = Depends()) -> FileResponse:
#     report = BasicReport(partners=params.partners, years=params.years,
#                          months=params.months, days=params.days
#                          ).get_basic_bid_report()
#     return FileResponse(report, filename="basic_bid_report.csv", media_type="application/octet-stream")


# if __name__ == "__main__":
#     uvicorn.run(app_reports, host="0.0.0.0", port=80, reload=True)
#     report_obj = Report()
#     report_obj.data = report_obj.get_data()
#     print(report_obj.data)
