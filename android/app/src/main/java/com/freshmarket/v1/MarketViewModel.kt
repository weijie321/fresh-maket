package com.freshmarket.v1

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class MarketUiState(
    val loading: Boolean = true,
    val error: String? = null,
    val cities: List<CityDto> = emptyList(),
    val selectedCity: CityDto? = null,
    val today: TodayRecommendationsDto? = null,
    val searchKeyword: String = "",
    val searchResults: List<IngredientDto> = emptyList(),
    val selectedIngredients: List<IngredientDto> = emptyList(),
    val recipes: List<RecipeCardDto> = emptyList()
)

class MarketViewModel(
    private val api: MarketApi = MarketApi()
) : ViewModel() {
    private val _state = MutableStateFlow(MarketUiState())
    val state: StateFlow<MarketUiState> = _state.asStateFlow()

    init {
        refresh()
    }

    fun refresh(cityCode: String? = null) {
        viewModelScope.launch {
            _state.value = _state.value.copy(loading = true, error = null)
            runCatching {
                val cities = api.cities()
                val city = cityCode?.let { code -> cities.firstOrNull { it.code == code } }
                    ?: _state.value.selectedCity
                    ?: cities.firstOrNull { it.code == "440100" }
                    ?: cities.first()
                val today = api.today(city.code)
                _state.value = _state.value.copy(
                    loading = false,
                    cities = cities,
                    selectedCity = city,
                    today = today,
                    error = null
                )
            }.onFailure { throwable ->
                _state.value = _state.value.copy(
                    loading = false,
                    error = throwable.message ?: "服务暂时不可用"
                )
            }
        }
    }

    fun selectCity(city: CityDto) {
        refresh(city.code)
    }

    fun search(keyword: String) {
        _state.value = _state.value.copy(searchKeyword = keyword)
        val city = _state.value.selectedCity ?: return
        viewModelScope.launch {
            runCatching {
                if (keyword.isBlank()) emptyList() else api.search(keyword.trim(), cityCode = city.code)
            }.onSuccess { results ->
                _state.value = _state.value.copy(searchResults = results, error = null)
            }.onFailure { throwable ->
                _state.value = _state.value.copy(error = throwable.message ?: "搜索失败")
            }
        }
    }

    fun toggleIngredient(ingredient: IngredientDto) {
        val current = _state.value.selectedIngredients
        val next = if (current.any { it.id == ingredient.id }) {
            current.filterNot { it.id == ingredient.id }
        } else {
            (current + ingredient).take(4)
        }
        _state.value = _state.value.copy(selectedIngredients = next)
    }

    fun generateRecipes() {
        val city = _state.value.selectedCity ?: return
        val ids = _state.value.selectedIngredients.map { it.id }
        if (ids.isEmpty()) return
        viewModelScope.launch {
            _state.value = _state.value.copy(loading = true, error = null)
            runCatching {
                api.generateRecipes(
                    RecipeRequestDto(
                        city_code = city.code,
                        ingredient_ids = ids,
                        people_count = 2,
                        cooking_time_minutes = 20,
                        taste_tags = listOf("家常", "快手")
                    )
                )
            }.onSuccess { recipes ->
                _state.value = _state.value.copy(loading = false, recipes = recipes)
            }.onFailure { throwable ->
                _state.value = _state.value.copy(
                    loading = false,
                    error = throwable.message ?: "生成失败"
                )
            }
        }
    }
}
