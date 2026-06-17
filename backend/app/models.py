from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class IngredientCategory(str, Enum):
    vegetable = "vegetable"
    meat = "meat"
    poultry = "poultry"
    egg = "egg"
    aquatic = "aquatic"
    processed = "processed"
    soy = "soy"
    mushroom = "mushroom"


class FreshnessForm(str, Enum):
    fresh = "fresh"
    frozen = "frozen"
    dried = "dried"
    processed = "processed"


class City(BaseModel):
    code: str
    name: str
    province: str
    region: str
    climate_zone: str
    profile: List[str] = Field(default_factory=list)


class IngredientPart(BaseModel):
    id: str
    name: str
    parent_id: str
    aliases: List[str] = Field(default_factory=list)
    cooking_methods: List[str] = Field(default_factory=list)


class Ingredient(BaseModel):
    id: str
    name: str
    category: IngredientCategory
    subcategory: str
    aliases: List[str] = Field(default_factory=list)
    pinyin: str = ""
    forms: List[FreshnessForm] = Field(default_factory=lambda: [FreshnessForm.fresh])
    common_score: float = 0.5
    seasonal_months: List[int] = Field(default_factory=list)
    climate_zones: List[str] = Field(default_factory=list)
    cooking_methods: List[str] = Field(default_factory=list)
    pairings: List[str] = Field(default_factory=list)
    region_tags: List[str] = Field(default_factory=list)
    parts: List[IngredientPart] = Field(default_factory=list)
    notes: str = ""


class PriceSnapshot(BaseModel):
    ingredient_id: str
    city_code: Optional[str] = None
    province: Optional[str] = None
    region: Optional[str] = None
    avg_price_yuan_per_jin: float
    low_price_yuan_per_jin: float
    high_price_yuan_per_jin: float
    source: str
    source_level: str
    confidence: float = 0.7
    updated_at: str


class PriceView(BaseModel):
    ingredient_id: str
    ingredient_name: str
    avg_price_yuan_per_jin: Optional[float] = None
    low_price_yuan_per_jin: Optional[float] = None
    high_price_yuan_per_jin: Optional[float] = None
    value_label: str
    source: str
    source_level: str
    updated_at: Optional[str] = None
    confidence: float = 0.0


class IngredientView(BaseModel):
    id: str
    name: str
    category: IngredientCategory
    subcategory: str
    aliases: List[str]
    forms: List[FreshnessForm]
    season_label: str
    cooking_methods: List[str]
    pairings: List[str]
    region_tags: List[str]
    parts: List[IngredientPart]
    notes: str


class RecommendationItem(BaseModel):
    ingredient: IngredientView
    price: PriceView
    score: float
    reasons: List[str]


class PairingRecommendation(BaseModel):
    title: str
    ingredient_ids: List[str]
    ingredient_names: List[str]
    score: float
    reason: str


class TodayRecommendations(BaseModel):
    city: City
    date: str
    groups: dict[str, List[RecommendationItem]]
    value_pairings: List[PairingRecommendation]


class RecipeRequest(BaseModel):
    city_code: str = "110100"
    ingredient_ids: List[str]
    people_count: int = Field(default=2, ge=1, le=10)
    budget_preference: str = "balanced"
    cooking_time_minutes: int = Field(default=20, ge=5, le=120)
    taste_tags: List[str] = Field(default_factory=list)


class RecipeCard(BaseModel):
    title: str
    ingredient_names: List[str]
    time_minutes: int
    difficulty: str
    ingredients: List[str]
    seasonings: List[str]
    steps: List[str]
    substitutions: List[str]
    tips: List[str]
    source: str


class FeedbackRequest(BaseModel):
    device_id: str
    city_code: str
    ingredient_ids: List[str] = Field(default_factory=list)
    recommendation_id: Optional[str] = None
    rating: int = Field(ge=1, le=5)
    tags: List[str] = Field(default_factory=list)
    comment: str = ""
