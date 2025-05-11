from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn


class getLinkDataRequest(BaseModel):
    link: str


class test(BaseModel):
    number : int
