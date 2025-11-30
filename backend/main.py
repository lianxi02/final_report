from fastapi import FastAPI, Query
from typing import List
import random
from database import load_recipes

app = FastAPI(title="食譜查詢 API", version="1.0.0")

recipes = load_recipes()

@app.get("/")
def root():
    return {"message": "歡迎使用食譜查詢 API"}

# 多食材搜尋（使用 list[str]）
@app.get("/search")
def search_recipes(ingredient: List[str] = Query(...)):
    # 只要食譜中「包含所有指定食材」就回傳
    result = []
    for r in recipes:
        if all(i in r["ingredients"] for i in ingredient):
            result.append(r)

    return {
        "query": ingredient,
        "count": len(result),
        "results": result
    }

@app.get("/list")
def list_recipes():
    return {"count": len(recipes), "recipes": recipes}

@app.get("/random")
def random_recipe():
    return random.choice(recipes)

@app.get("/detail")
def recipe_detail(name: str):
    for r in recipes:
        if r["name"] == name:
            return r
    return {"error": f"找不到名為 {name} 的食譜"}
