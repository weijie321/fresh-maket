from __future__ import annotations

from datetime import date
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from . import data
from .models import (
    City,
    FeedbackRequest,
    IngredientCategory,
    IngredientView,
    PriceView,
    RecipeCard,
    RecipeRequest,
    TodayRecommendations,
)
from .services.catalog import search_ingredients, to_view
from .services.pricing import get_price_view
from .services.recipes import generate_recipes
from .services.recommendations import today


app = FastAPI(title="Fresh Market V1 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/cities", response_model=List[City])
def cities() -> List[City]:
    return data.list_cities()


@app.get("/v1/ingredients", response_model=List[IngredientView])
def ingredients(
    category: Optional[IngredientCategory] = None,
    keyword: str = "",
    cityCode: str = Query(default="110100"),
) -> List[IngredientView]:
    return search_ingredients(category, keyword, cityCode)


@app.get("/v1/ingredients/{ingredient_id}", response_model=IngredientView)
def ingredient_detail(ingredient_id: str, cityCode: str = Query(default="110100")) -> IngredientView:
    ingredient = data.get_ingredient(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return to_view(ingredient, cityCode)


@app.get("/v1/prices", response_model=List[PriceView])
def prices(
    cityCode: str = Query(default="110100"),
    ingredientIds: str = Query(default=""),
    category: Optional[IngredientCategory] = None,
) -> List[PriceView]:
    if ingredientIds:
        ids = [item.strip() for item in ingredientIds.split(",") if item.strip()]
        ingredients_to_price = [data.get_ingredient(item_id) for item_id in ids]
        return [get_price_view(item, cityCode) for item in ingredients_to_price if item]
    ingredients_to_price = data.list_ingredients(category=category)
    return [get_price_view(item, cityCode) for item in ingredients_to_price]


@app.get("/v1/recommendations/today", response_model=TodayRecommendations)
def today_recommendations(
    cityCode: str = Query(default="110100"),
    targetDate: Optional[date] = Query(default=None, alias="date"),
) -> TodayRecommendations:
    return today(cityCode, targetDate or date.today())


@app.post("/v1/recipes/generate", response_model=List[RecipeCard])
async def recipes(request: RecipeRequest) -> List[RecipeCard]:
    return await generate_recipes(request)


@app.post("/v1/feedback")
def feedback(request: FeedbackRequest) -> dict[str, str]:
    # V1 stores no account data. Real persistence can be added behind this endpoint.
    return {"status": "accepted", "deviceId": request.device_id}
