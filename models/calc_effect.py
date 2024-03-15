import logging
import os
import numpy as np
import pandas as pd
import ast
from fastapi import Depends, FastAPI, HTTPException, Request
from . import effect_exp_healing, effect_forest, effect_hiking
from datetime import datetime
import math

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

my_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
program_list_data = pd.read_csv(os.path.join(my_path, "datasets/program_list.csv"))


def run(
    program_id=int,
    height=float,
    birth_year=int,
    gender=str,
    weight=float,
) :
    age = datetime.today().year - birth_year
    age_range = str(math.floor(age / 10) * 10) + "대"

    _program = program_list_data[program_list_data["id"] == program_id]

    if len(_program) == 0:
        raise HTTPException(status_code=404, detail="Program not found")

    program = _program.iloc[0,:]
    print(program)
    print("================")
    effect = 0
    if program["category"]=="숲 체험" or program["category"]== "산림 치유원":
        effect= effect_exp_healing.run(height, age, gender, weight)
    elif program["category"] == "숲 길":
        effect=effect_forest.run(program["distance"], height, weight)
    else:
        effect=effect_hiking.run(program["distance"], gender, age_range)

    print(effect)
    
    return [program, effect]
