import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db.data_base import DataBase as DB
from routers import heatmaps, stages, basics


app_reports = FastAPI()
app_reports.include_router(heatmaps.heatmap_router)
app_reports.include_router(stages.stages_router)
app_reports.include_router(basics.basic_router)
app_reports.mount("/static", StaticFiles(directory="static"), name="static")
DB.set_data()


@app_reports.get('/')
async def root():
    return {"message": "Hello, this is a reporting api"}


# if __name__ == "__main__":
#     uvicorn.run(app_reports, host="0.0.0.0", port=80, reload=True)
#     report_obj = Report()
#     report_obj.data = report_obj.get_data()
#     print(report_obj.data)
