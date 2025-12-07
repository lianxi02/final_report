from fastapi import FastAPI, Query
from typing import List, Optional
import random
from database import load_recipes

app = FastAPI(title="食譜查詢 API", version="2.0.0")

recipes = load_recipes()

@app.get("/")
def root():
    return {"message": "歡迎使用強化版食譜查詢 API！"}

# 多條件搜尋：分類 + 多食材
@app.get("/search")
def search_recipes(
    category: Optional[str] = Query(None, description="分類：dessert（甜點）或 home（家常菜）"),
    ingredient: Optional[List[str]] = Query(
        None,
        description="📌 **甜點食材可選：**\n"
        "🍓 水果：草莓、香蕉、蘋果、芒果、酪梨、藍莓、地瓜、南瓜\n"
        "🥛 乳製品：鮮奶、豆漿、優格、乳酪\n"
        "🥚 蛋類：雞蛋、蛋黃\n"
        "🍯 甜味：蜂蜜、砂糖、黑糖、冰糖、楓糖漿\n"
        "🍫 烘焙：可可粉、巧克力豆、肉桂粉、泡打粉、吉利丁\n"
        "🥣 穀類：燕麥、紫米、糯米粉、低筋、中筋、餅乾\n"
        "🥑 豆類：豆腐、豆渣、紅豆\n\n"
        "📌 **家常菜食材可選：**\n"
        "🥬 蔬菜：蔥、蒜、洋蔥、青江菜、番茄\n"
        "🥩 肉類：雞肉、豬肉、牛肉、絞肉\n"
        "🐟 海鮮：蝦、魚肉、鮪魚罐頭\n"
        "🍳 基礎：雞蛋、醬油、鹽、糖、油\n"
        "🍚 主食：白飯、麵條、米粉\n"
    )
):
    result = recipes

    # 篩選分類
    if category:
        result = [r for r in result if r["category"] == category]

    # 多食材搜尋（需要全部符合）
    if ingredient:
        result = [r for r in result if all(i in r["ingredients"] for i in ingredient)]

    return {
        "category": category,
        "ingredients_query": ingredient,
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
def recipe_detail(name: str = Query(..., description="食譜名稱")):
    for r in recipes:
        if r["name"] == name:
            return r
    return {"error": f"找不到名為 {name} 的食譜"}

