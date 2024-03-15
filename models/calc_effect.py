import logging
import os
import numpy as np
import pandas as pd
import ast
from fastapi import Depends, FastAPI, HTTPException, Request
from . import effect_exp_healing, effect_forest, effect_hiking

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

my_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
program_list_data = pd.read_csv(os.path.join(my_path, "datasets/program_list.csv"))


def run(program_id=int, height=float, age=int, gender=str, weight=float):
    _program = program_list_data[program_list_data["id"] == program_id]
    if len(_program) == 0:
        raise HTTPException(status_code=404, detail="Program not found")

    program = _program[0]

    if program["category"].isin(["숲 체험", "산림 치유원"]):
        return effect_exp_healing.run(height, age, gender, weight)
    elif program["category"] == "숲 길":
        return effect_forest.run()
    else:
        return effect_hiking.run()
