from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import JSONResponse

from Controller.pojo.LinkDataResponse import getLinkDataResponse
from Controller.pojo.LinkDataRequest import getLinkDataRequest, test
from Scrapers.producthistory import Myntra

# from Service.MyntraDataScrapeService import init_browser, close_browser
import uvicorn

from Service import MyntraDataScrapeService
from Service import Test
# Create FastAPI instance



# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await init_browser()
#     yield
#     await close_browser()

#
# app = FastAPI(lifespan=lifespan)
# @app.on_event("startup")
# async def on_startup():
#     await init_browser()
#
#
# @app.on_event("shutdown")
# async def on_shutdown():
#     await close_browser()



app = FastAPI()
@app.get("/", include_in_schema=False)
async def health():
    return JSONResponse({"status": "ok"})
@app.post("/getLinkData", response_model=getLinkDataResponse)
async def process_person(getLinkDataRequest: getLinkDataRequest):
    return await delegator(getLinkDataRequest)






def delegator(getLinkDataRequest: getLinkDataRequest):
    if "myntra" in getLinkDataRequest.link:
        return Myntra.action(getLinkDataRequest.link)











@app.post("/getLinkData2", response_model=getLinkDataResponse)
async def process_person(test: test):
    if(test.number == 1):
        response = Test.action()
    elif(test.number == 2):
        response = Test.action2()
    elif(test.number == 3):
        response = Test.action3()
    elif(test.number == 4):
        response = Test.action4()
    return response




# Run the application with uvicorn when this script is executed directly
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
