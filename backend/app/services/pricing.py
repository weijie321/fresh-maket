from __future__ import annotations

from .. import data
from ..models import Ingredient, PriceView


def value_label(avg_price: float, low_price: float, high_price: float, confidence: float) -> str:
    if confidence < 0.5:
        return "参考"
    span = max(high_price - low_price, 0.01)
    position = (avg_price - low_price) / span
    if position <= 0.35:
        return "划算"
    if position >= 0.72:
        return "偏贵"
    return "正常"


def get_price_view(ingredient: Ingredient, city_code: str) -> PriceView:
    city = data.get_city(city_code)
    snapshot = data.find_price_snapshot(ingredient.id, city)
    if not snapshot:
        return PriceView(
            ingredient_id=ingredient.id,
            ingredient_name=ingredient.name,
            value_label="暂无当地参考价",
            source="暂无",
            source_level="missing",
            confidence=0.0,
        )
    return PriceView(
        ingredient_id=ingredient.id,
        ingredient_name=ingredient.name,
        avg_price_yuan_per_jin=round(snapshot.avg_price_yuan_per_jin, 2),
        low_price_yuan_per_jin=round(snapshot.low_price_yuan_per_jin, 2),
        high_price_yuan_per_jin=round(snapshot.high_price_yuan_per_jin, 2),
        value_label=value_label(
            snapshot.avg_price_yuan_per_jin,
            snapshot.low_price_yuan_per_jin,
            snapshot.high_price_yuan_per_jin,
            snapshot.confidence,
        ),
        source=snapshot.source,
        source_level=snapshot.source_level,
        updated_at=snapshot.updated_at,
        confidence=snapshot.confidence,
    )
