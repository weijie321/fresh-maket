package com.freshmarket.v1

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            FreshMarketTheme {
                val viewModel: MarketViewModel = viewModel()
                val state by viewModel.state.collectAsState()
                MarketScreen(
                    state = state,
                    onCitySelected = viewModel::selectCity,
                    onSearch = viewModel::search,
                    onIngredientToggle = viewModel::toggleIngredient,
                    onGenerateRecipes = viewModel::generateRecipes,
                    onRefresh = { viewModel.refresh() }
                )
            }
        }
    }
}

@Composable
fun FreshMarketTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = MaterialTheme.colorScheme.copy(
            primary = Color(0xFF2F7D57),
            secondary = Color(0xFFD56A36),
            surface = Color(0xFFFFFBF4),
            background = Color(0xFFF7F3EC)
        ),
        content = content
    )
}

@Composable
fun MarketScreen(
    state: MarketUiState,
    onCitySelected: (CityDto) -> Unit,
    onSearch: (String) -> Unit,
    onIngredientToggle: (IngredientDto) -> Unit,
    onGenerateRecipes: () -> Unit,
    onRefresh: () -> Unit
) {
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        LazyColumn(
            contentPadding = PaddingValues(18.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            item {
                Header(
                    state = state,
                    onCitySelected = onCitySelected,
                    onRefresh = onRefresh
                )
            }
            state.error?.let { error ->
                item { ErrorBand(error) }
            }
            state.today?.let { today ->
                item { PairingStrip(pairings = today.value_pairings) }
                item {
                    RecommendationSection("今日蔬菜", today.groups["today_vegetables"].orEmpty(), onIngredientToggle, state.selectedIngredients)
                }
                item {
                    RecommendationSection("今日肉禽蛋", today.groups["today_meat_poultry_egg"].orEmpty(), onIngredientToggle, state.selectedIngredients)
                }
                item {
                    RecommendationSection("今日水产", today.groups["today_aquatic"].orEmpty(), onIngredientToggle, state.selectedIngredients)
                }
            }
            item {
                SearchPanel(
                    keyword = state.searchKeyword,
                    results = state.searchResults,
                    selected = state.selectedIngredients,
                    recipes = state.recipes,
                    onSearch = onSearch,
                    onIngredientToggle = onIngredientToggle,
                    onGenerateRecipes = onGenerateRecipes
                )
            }
            if (state.loading) {
                item { LoadingBand() }
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun Header(
    state: MarketUiState,
    onCitySelected: (CityDto) -> Unit,
    onRefresh: () -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    Column(
        verticalArrangement = Arrangement.spacedBy(10.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween,
            modifier = Modifier.fillMaxWidth()
        ) {
            Column {
                Text("今日菜价", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                Text(
                    text = state.today?.date ?: "准备中",
                    color = Color(0xFF6F675C),
                    style = MaterialTheme.typography.bodyMedium
                )
            }
            Box {
                TextButton(onClick = { expanded = true }) {
                    Text(state.selectedCity?.name ?: "选城市")
                }
                DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                    state.cities.forEach { city ->
                        DropdownMenuItem(
                            text = { Text("${city.name} · ${city.province}") },
                            onClick = {
                                expanded = false
                                onCitySelected(city)
                            }
                        )
                    }
                }
            }
        }
        FlowRow(
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Pill("全品类食材库")
            Pill("当地参考价")
            Pill("性价比优先")
            Text(
                "刷新",
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.clickable(onClick = onRefresh).padding(horizontal = 8.dp, vertical = 5.dp)
            )
        }
    }
}

@Composable
fun RecommendationSection(
    title: String,
    items: List<RecommendationItemDto>,
    onIngredientToggle: (IngredientDto) -> Unit,
    selected: List<IngredientDto>
) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        items.take(5).forEach { item ->
            IngredientCard(
                item = item,
                selected = selected.any { it.id == item.ingredient.id },
                onClick = { onIngredientToggle(item.ingredient) }
            )
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun IngredientCard(
    item: RecommendationItemDto,
    selected: Boolean,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth().clickable(onClick = onClick),
        shape = RoundedCornerShape(8.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(Modifier.weight(1f)) {
                    Text(
                        item.ingredient.name,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        "${item.ingredient.subcategory} · ${item.ingredient.season_label}",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color(0xFF6F675C)
                    )
                }
                PriceBlock(item.price)
            }
            FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                item.reasons.take(3).forEach { Pill(it) }
                if (selected) Pill("已选")
            }
            if (selected) {
                Box(
                    Modifier.fillMaxWidth().height(2.dp).background(MaterialTheme.colorScheme.primary, RoundedCornerShape(2.dp))
                )
            }
        }
    }
}

@Composable
fun PriceBlock(price: PriceDto) {
    Column(horizontalAlignment = Alignment.End) {
        val priceText = price.avg_price_yuan_per_jin?.let { "${"%.1f".format(it)}元/斤" } ?: "暂无价"
        Text(priceText, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.secondary)
        Text(price.value_label, style = MaterialTheme.typography.labelMedium, color = Color(0xFF6F675C))
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun PairingStrip(pairings: List<PairingRecommendationDto>) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text("高性价比搭配", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            pairings.take(6).forEach { pairing ->
                Card(
                    shape = RoundedCornerShape(8.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFFEAF4ED))
                ) {
                    Column(Modifier.width(148.dp).padding(10.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        Text(pairing.title, fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text(pairing.reason, style = MaterialTheme.typography.bodySmall, color = Color(0xFF516257), maxLines = 2)
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun SearchPanel(
    keyword: String,
    results: List<IngredientDto>,
    selected: List<IngredientDto>,
    recipes: List<RecipeCardDto>,
    onSearch: (String) -> Unit,
    onIngredientToggle: (IngredientDto) -> Unit,
    onGenerateRecipes: () -> Unit
) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text("全库搜索", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        OutlinedTextField(
            value = keyword,
            onValueChange = onSearch,
            singleLine = true,
            label = { Text("输入蔬菜、肉类、水产或部位") },
            modifier = Modifier.fillMaxWidth()
        )
        if (results.isNotEmpty()) {
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                results.take(12).forEach { ingredient ->
                    val isSelected = selected.any { it.id == ingredient.id }
                    Text(
                        text = if (isSelected) "${ingredient.name} ✓" else ingredient.name,
                        color = if (isSelected) Color.White else Color(0xFF24352B),
                        modifier = Modifier
                            .background(
                                if (isSelected) MaterialTheme.colorScheme.primary else Color.White,
                                RoundedCornerShape(8.dp)
                            )
                            .clickable { onIngredientToggle(ingredient) }
                            .padding(horizontal = 12.dp, vertical = 8.dp)
                    )
                }
            }
        }
        if (selected.isNotEmpty()) {
            Text("已选：${selected.joinToString("、") { it.name }}", color = Color(0xFF4F5F54))
            Button(onClick = onGenerateRecipes, shape = RoundedCornerShape(8.dp)) {
                Text("生成做法")
            }
        }
        recipes.forEach { recipe ->
            RecipeCard(recipe)
        }
    }
}

@Composable
fun RecipeCard(recipe: RecipeCardDto) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(8.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White)
    ) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(recipe.title, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                Text("${recipe.time_minutes}分钟", color = MaterialTheme.colorScheme.secondary)
            }
            Text("调味：${recipe.seasonings.joinToString("、")}", color = Color(0xFF6F675C))
            recipe.steps.forEachIndexed { index, step ->
                Text("${index + 1}. $step")
            }
        }
    }
}

@Composable
fun Pill(text: String) {
    Text(
        text,
        style = MaterialTheme.typography.labelMedium,
        color = Color(0xFF315743),
        modifier = Modifier
            .background(Color(0xFFE6EFE8), RoundedCornerShape(8.dp))
            .padding(horizontal = 8.dp, vertical = 5.dp)
    )
}

@Composable
fun ErrorBand(message: String) {
    Text(
        message,
        color = Color(0xFF7F1D1D),
        modifier = Modifier.fillMaxWidth().background(Color(0xFFFFE7E7), RoundedCornerShape(8.dp)).padding(12.dp)
    )
}

@Composable
fun LoadingBand() {
    Text(
        "加载中",
        color = Color(0xFF6F675C),
        modifier = Modifier.fillMaxWidth().background(Color.White, RoundedCornerShape(8.dp)).padding(12.dp)
    )
}
