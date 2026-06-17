from __future__ import annotations

from datetime import date
from typing import Optional

from .. import data
from ..models import Ingredient, IngredientCategory, IngredientView


def season_label(ingredient: Ingredient, city_code: str, target_date: date) -> str:
    city = data.get_city(city_code)
    month = target_date.month
    in_month = month in ingredient.seasonal_months
    in_zone = not ingredient.climate_zones or city.climate_zone in ingredient.climate_zones
    if in_month and in_zone:
        return "当季"
    if len(ingredient.seasonal_months) == 12:
        return "常年供应"
    if not ingredient.seasonal_months:
        return "数据不足"
    return "非当季"


def to_view(ingredient: Ingredient, city_code: str = "110100", target_date: Optional[date] = None) -> IngredientView:
    target_date = target_date or date.today()
    return IngredientView(
        id=ingredient.id,
        name=ingredient.name,
        category=ingredient.category,
        subcategory=ingredient.subcategory,
        aliases=ingredient.aliases,
        forms=ingredient.forms,
        season_label=season_label(ingredient, city_code, target_date),
        cooking_methods=ingredient.cooking_methods,
        pairings=ingredient.pairings,
        region_tags=ingredient.region_tags,
        parts=ingredient.parts,
        notes=ingredient.notes,
    )


def search_ingredients(category: Optional[IngredientCategory], keyword: str, city_code: str) -> list[IngredientView]:
    return [to_view(item, city_code=city_code) for item in data.list_ingredients(category=category, keyword=keyword)]
