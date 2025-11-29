from fastapi import FastAPI
import json

app = FastAPI()

# 讀入資料
with open("data/recipes.json", "r", encoding="utf-8") as f:
    RECIPES = json.load(f)

@app.get("/")
def root():
    return {"message": "食譜查詢 API 已啟動 🍳"}

@app.get("/search")
def search_recipe(ingredient: str):
    results = []
    for r in RECIPES:
        if ingredient in r["ingredients"]:
            results.append(r)

    return {
        "query": ingredient,
        "count": len(results),
        "results": results
    }