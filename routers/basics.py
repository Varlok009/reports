from fastapi import Request, APIRouter
from reports.basic.basic_report import BasicReport
from fastapi.responses import FileResponse
from config import templates
from models.params import BaseParams

# from dependencies import get_token_header


basic_router = APIRouter(
    prefix="/basic",
    tags=["basic"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@basic_router.post('/statement')
async def get_time_report(request: Request, params: BaseParams):
    report = BasicReport(params).get_basic_statement_report()
    return FileResponse(report, filename='report.csv', media_type="application/octet-stream")
