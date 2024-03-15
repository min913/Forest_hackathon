import logging
import os
import numpy as np
import pandas as pd
import ast
from fastapi import Depends, FastAPI, HTTPException, Request
from . import effect_exp_healing, effect_forest_hiking
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

my_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
program_list_data = pd.read_csv(os.path.join(my_path, "datasets/program_list.csv"))


def run(program_id=int):
    _program = program_list_data[program_list_data['id']==program_id]
    if(len(_program)==0):
        raise HTTPException(status_code=404, detail="Program not found")
    
    program = _program[0]

    
    effect = effect_exp_healing.run() if program["category"].isin(["숲 체험","산림 치유원"]) else effect_forest_hiking.run()

    return effect
    
    

