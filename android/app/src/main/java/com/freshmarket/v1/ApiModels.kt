package com.freshmarket.v1

import kotlinx.serialization.Serializable

@Serializable
data class CityDto(
    val code: String,
    val name: String,
    val province: String,
    val region: String,
    val climate_zone: String,
    val profile: List<String> = emptyList()
)

@Serializable
data class IngredientPartDto(
    val id: String,
    val name: String,
    val parent_id: String,
    val aliases: List<String> = emptyList(),
    val cooking_methods: List<String> = emptyList()
)

@Serializable
data class IngredientDto(
    val id: String,
    val name: String,
    val category: String,
    val subcategory: String,
    val aliases: List<String> = emptyList(),
    val forms: List<String> = emptyList(),
    val season_label: String,
    val cooking_methods: List<String> = emptyList(),
    val pairings: List<String> = emptyList(),
    val region_tags: List<String> = emptyList(),
    val parts: List<IngredientPartDto> = emptyList(),
    val notes: String = ""
)

@Serializable
data class PriceDto(
    val ingredient_id: String,
    val ingredient_name: String,
    val avg_price_yuan_per_jin: Double? = null,
    val low_price_yuan_per_jin: Double? = null,
    val high_price_yuan_per_jin: Double? = null,
    val value_label: String,
    val source: String,
    val source_level: String,
    val updated_at: String? = null,
    val confidence: Double = 0.0
)

@Serializable
data class RecommendationItemDto(
    val ingredient: IngredientDto,
    val price: PriceDto,
    val score: Double,
    val reasons: List<String> = emptyList()
)

@Serializable
data class PairingRecommendationDto(
    val title: String,
    val ingredient_ids: List<String> = emptyList(),
    val ingredient_names: List<String> = emptyList(),
    val score: Double,
    val reason: String
)

@Serializable
data class TodayRecommendationsDto(
    val city: CityDto,
    val date: String,
    val groups: Map<String, List<RecommendationItemDto>> = emptyMap(),
    val value_pairings: List<PairingRecommendationDto> = emptyList()
)

@Serializable
data class RecipeRequestDto(
    val city_code: String,
    val ingredient_ids: List<String>,
    val people_count: Int = 2,
    val budget_preference: String = "balanced",
    val cooking_time_minutes: Int = 20,
    val taste_tags: List<String> = emptyList()
)

@Serializable
data class RecipeCardDto(
    val title: String,
    val ingredient_names: List<String> = emptyList(),
    val time_minutes: Int,
    val difficulty: String,
    val ingredients: List<String> = emptyList(),
    val seasonings: List<String> = emptyList(),
    val steps: List<String> = emptyList(),
    val substitutions: List<String> = emptyList(),
    val tips: List<String> = emptyList(),
    val source: String
)
