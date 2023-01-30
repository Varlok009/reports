from fastapi import FastAPI, Depends, Request, Query
from reports.heatmaps.heatmap_report import HeatmapReport
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app_reports = FastAPI()
app_reports.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class QueryParams:
    def __init__(self,
                 partners: set[str] | None = Query(default=None),
                 years: set[int] | None = Query(default=None),
                 months: set[int] | None = Query(default=None),
                 days: bool | None = Query(default=None,
                                           title="Days of the week",
                                           description="Report for days")):
        self.partners = partners
        self.years = years
        self.months = months
        self.days = days


@app_reports.get('/')
async def root():
    return {"message": "Hello, this is a reporting api"}


@app_reports.get('/heatmap/deal_report')
async def get_deal_report(request: Request, params: QueryParams = Depends()):
    report = HeatmapReport().get_heatmap_deal_report()
    return templates.TemplateResponse("report.html", {"request": request, "report": report})
    # return {'params': params, 'partners': params.partners}


@app_reports.get('/heatmap/bid_report')
async def get_bid_report(request: Request, params: QueryParams = Depends()):
    report = HeatmapReport().get_heatmap_bid_report()
    return templates.TemplateResponse("report.html", {"request": request, "report": report})
    # return {'from Request': request.query_params, 'from params': params}
