from fastapi import Request, APIRouter
from reports.time.time_report import TimeReport
from fastapi.responses import FileResponse
from config import templates
from models.params import TimeParams

# from dependencies import get_token_header


time_router = APIRouter(
    prefix="/time",
    tags=["time"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@time_router.post('/')
async def get_time_report(request: Request, params: TimeParams):
    report = TimeReport(params).get_time_report()
    return FileResponse(report, filename='report.png', media_type="application/octet-stream")
