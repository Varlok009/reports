import base64
from fastapi import FastAPI, Request
from reports.deal_reports import Reports
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app_reports = FastAPI()
app_reports.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app_reports.get('/')
async def root():
    return {"message": "Hello, this is a reporting api"}


@app_reports.get('/deal_report', response_class=HTMLResponse)
async def get_deal_report(request: Request):
    print('deal report')
    report = Reports.get_report()
    report = report.decode('utf-8')
    return templates.TemplateResponse("report.html", {"request": request, "report": report})

