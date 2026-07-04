import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'gateways'))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
import matlab
import pandas as pd
import numpy as np
import math

from fsda_gateway import FSDA

app = FastAPI(title="FSDA Local Gateway")

fsda = FSDA()


def make_json_safe(obj):
    """MATLAB/pandas/numpy output ko JSON-safe Python types mein convert karta hai."""
    if isinstance(obj, matlab.double):
        arr = [list(row) for row in obj]
        return make_json_safe(arr)
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, pd.DataFrame):
        df = obj.reset_index()
        return make_json_safe(df.to_dict(orient="records"))
    if isinstance(obj, pd.Timestamp):
        return str(obj)
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    return obj


class CallRequest(BaseModel):
    args: List[Any] = []


def convert_arg(a):
    """Numeric lists ko matlab.double mein convert karta hai; strings/bools ko waise hi rehne do."""
    if isinstance(a, list):
        return matlab.double(a)
    return a


@app.post("/call/{function_name}")
def call_function(function_name: str, request: CallRequest):
    try:
        converted_args = [convert_arg(a) for a in request.args]
        result = fsda.run(function_name, *converted_args)
        safe_result = make_json_safe(result)
        return {"status": "ok", "result": safe_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ping")
def ping():
    result = fsda.run('ping', 'Hello from server!')
    return {"status": "ok", "result": make_json_safe(result)}


@app.on_event("shutdown")
def shutdown_event():
    fsda.close()