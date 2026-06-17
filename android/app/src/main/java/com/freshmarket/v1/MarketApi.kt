package com.freshmarket.v1

import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.engine.android.Android
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.request.get
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.http.ContentType
import io.ktor.http.contentType
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json
import java.net.URLEncoder

class MarketApi(
    private val baseUrl: String = BuildConfig.API_BASE_URL
) {
    private val client = HttpClient(Android) {
        install(ContentNegotiation) {
            json(Json {
                ignoreUnknownKeys = true
                explicitNulls = false
            })
        }
    }

    suspend fun cities(): List<CityDto> =
        client.get("$baseUrl/v1/cities").body()

    suspend fun today(cityCode: String): TodayRecommendationsDto =
        client.get("$baseUrl/v1/recommendations/today?cityCode=$cityCode").body()

    suspend fun search(keyword: String, category: String? = null, cityCode: String): List<IngredientDto> {
        val encodedKeyword = URLEncoder.encode(keyword, "UTF-8")
        val categoryQuery = category?.let { "&category=$it" } ?: ""
        return client.get("$baseUrl/v1/ingredients?cityCode=$cityCode&keyword=$encodedKeyword$categoryQuery").body()
    }

    suspend fun generateRecipes(request: RecipeRequestDto): List<RecipeCardDto> =
        client.post("$baseUrl/v1/recipes/generate") {
            contentType(ContentType.Application.Json)
            setBody(request)
        }.body()
}
