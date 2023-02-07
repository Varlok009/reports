from fastapi import Request, APIRouter
from reports.heatmaps.heatmap_report import HeatmapReport
from fastapi.responses import FileResponse
from config import templates
from models.params import HeatmapParams

# from dependencies import get_token_header


heatmap_router = APIRouter(
    prefix="/heatmap",
    tags=["heatmap"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@heatmap_router.post('/credit_report', tags=['heatmap'])
async def get_heatmap_credit_report(request: Request, params: HeatmapParams):
    report = HeatmapReport(params).get_heatmap_credit_report()
    return FileResponse(report, filename='report.png', media_type="application/octet-stream")
    # return templates.TemplateResponse("report.html", {"request": request, "report": report})


@heatmap_router.post('/statement_report', tags=['heatmap'])
async def get_heatmap_statement_report(request: Request, params: HeatmapParams):
    report = HeatmapReport(params).get_heatmap_statement_report()
    return FileResponse(report, filename='report.png', media_type="application/octet-stream")
