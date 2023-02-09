from fastapi import Request, APIRouter
from reports.stages.stage_report import StageReport
from fastapi.responses import FileResponse
from config import templates
from models.params import StageParams

# from dependencies import get_token_header


stages_router = APIRouter(
    prefix="/stages",
    tags=["stages"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@stages_router.post('/')
async def get_time_report(request: Request, params: StageParams):
    report = StageReport(params).get_time_report()
    return FileResponse(report, filename='report.png', media_type="application/octet-stream")
