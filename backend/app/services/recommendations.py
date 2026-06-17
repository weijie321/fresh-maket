from __future__ import annotations

from datetime import date
from typing import Iterable, List

from .. import data
from ..models import (
    Ingredient,
    IngredientCategory,
    PairingRecommendation,
    RecommendationItem,
    TodayRecommendations,
)
from .catalog import season_label, to_view
from .pricing import get_price_view


GROUPS = {
    "today_vegetables": [IngredientCategory.vegetable, IngredientCategory.mushroom, IngredientCategory.soy],
    "today_meat_poultry_egg": [IngredientCategory.meat, IngredientCategory.poultry, IngredientCategory.egg],
    "today_aquatic": [IngredientCategory.aquatic],
    "processed_pairings": [IngredientCategory.processed],
}


def price_score(label: str, confidence: float) -> float:
    if label == "划算":
        return 1.0 * confidence
    if label == "正常":
        return 0.62 * confidence
    if label == "偏贵":
        return 0.2 * confidence
    if label == "参考":
        return 0.38 * confidence
    return 0.0


def region_score(ingredient: Ingredient, city_profile: Iterable[str]) -> float:
    profile = set(city_profile)
    tags = set(ingredient.region_tags)
    if not tags:
        return 0.25
    if tags & profile:
        return 1.0
    if "seafood" in tags and ("aquatic" in profile or "seafood" in profile):
        return 1.0
    if "northwest" in tags and "beef_lamb" in profile:
        return 0.9
    return 0.2


def seasonal_score(label: str) -> float:
    return {
        "当季": 1.0,
        "常年供应": 0.55,
        "非当季": 0.18,
        "数据不足": 0.08,
    }.get(label, 0.0)


def score_item(ingredient: Ingredient, city_code: str, target_date: date) -> tuple[float, list[str]]:
    city = data.get_city(city_code)
    label = season_label(ingredient, city_code, target_date)
    price = get_price_view(ingredient, city_code)
    p_score = price_score(price.value_label, price.confidence)
    s_score = seasonal_score(label)
    r_score = region_score(ingredient, city.profile)
    cooking_score = min(len(ingredient.cooking_methods) / 4, 1.0)
    pairing_score = min(len(ingredient.pairings) / 4, 1.0)
    processed_penalty = -0.22 if ingredient.category == IngredientCategory.processed else 0
    total = (
        p_score * 0.36
        + s_score * 0.24
        + r_score * 0.18
        + ingredient.common_score * 0.12
        + cooking_score * 0.06
        + pairing_score * 0.04
        + processed_penalty
    )
    reasons: list[str] = []
    if label == "当季":
        reasons.append("当前季节适合购买")
    elif label == "常年供应":
        reasons.append("常年供应稳定")
    if price.value_label in {"划算", "正常"}:
        reasons.append(f"当地参考价{price.value_label}")
    elif price.value_label == "偏贵":
        reasons.append("价格略高，推荐降权")
    if r_score >= 0.9:
        reasons.append("符合当地饮食偏好")
    if ingredient.pairings:
        reasons.append("容易搭配家常菜")
    if ingredient.category == IngredientCategory.processed:
        reasons.append("加工品仅作搭配参考")
    return round(total, 4), reasons


def build_item(ingredient: Ingredient, city_code: str, target_date: date) -> RecommendationItem:
    score, reasons = score_item(ingredient, city_code, target_date)
    return RecommendationItem(
        ingredient=to_view(ingredient, city_code, target_date),
        price=get_price_view(ingredient, city_code),
        score=score,
        reasons=reasons,
    )


def top_for_categories(categories: list[IngredientCategory], city_code: str, target_date: date, limit: int) -> List[RecommendationItem]:
    candidates = [item for item in data.INGREDIENTS if item.category in categories]
    items = [build_item(item, city_code, target_date) for item in candidates]
    strong = [item for item in items if item.price.source_level != "missing" and item.price.confidence >= 0.4]
    return sorted(strong, key=lambda item: item.score, reverse=True)[:limit]


def build_pairings(city_code: str, target_date: date) -> list[PairingRecommendation]:
    ranked = {item.ingredient.id: item for group in GROUPS.values() for item in top_for_categories(group, city_code, target_date, 10)}
    pairings: list[PairingRecommendation] = []
    for item in ranked.values():
        source = data.get_ingredient(item.ingredient.id)
        if not source:
            continue
        for pairing_id in source.pairings:
            pair = data.get_ingredient(pairing_id)
            if not pair:
                continue
            pair_item = ranked.get(pair.id) or build_item(pair, city_code, target_date)
            combined = round((item.score + pair_item.score) / 2, 4)
            title = f"{item.ingredient.name}+{pair.name}"
            reason = "价格和家常搭配都比较稳"
            if item.price.value_label == "划算" or pair_item.price.value_label == "划算":
                reason = "其中一项价格较划算，适合今天安排"
            pairings.append(
                PairingRecommendation(
                    title=title,
                    ingredient_ids=[item.ingredient.id, pair.id],
                    ingredient_names=[item.ingredient.name, pair.name],
                    score=combined,
                    reason=reason,
                )
            )
    dedup: dict[str, PairingRecommendation] = {}
    for pairing in pairings:
        key = "|".join(sorted(pairing.ingredient_ids))
        if key not in dedup or pairing.score > dedup[key].score:
            dedup[key] = pairing
    return sorted(dedup.values(), key=lambda item: item.score, reverse=True)[:8]


def today(city_code: str, target_date: date) -> TodayRecommendations:
    city = data.get_city(city_code)
    groups = {
        key: top_for_categories(categories, city_code, target_date, 8)
        for key, categories in GROUPS.items()
    }
    return TodayRecommendations(
        city=city,
        date=target_date.isoformat(),
        groups=groups,
        value_pairings=build_pairings(city_code, target_date),
    )
