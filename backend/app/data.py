from __future__ import annotations

from datetime import date
from typing import Dict, Iterable, List, Optional

from .models import (
    City,
    FreshnessForm,
    Ingredient,
    IngredientCategory,
    IngredientPart,
    PriceSnapshot,
)


CITIES: List[City] = [
    City(code="110100", name="北京", province="北京", region="north", climate_zone="temperate_north", profile=["north", "wheat", "home_style"]),
    City(code="310100", name="上海", province="上海", region="east", climate_zone="humid_east", profile=["east", "aquatic", "light"]),
    City(code="440100", name="广州", province="广东", region="south", climate_zone="subtropical_south", profile=["south", "aquatic", "light"]),
    City(code="510100", name="成都", province="四川", region="southwest", climate_zone="basin_southwest", profile=["southwest", "spicy", "home_style"]),
    City(code="230100", name="哈尔滨", province="黑龙江", region="northeast", climate_zone="cold_northeast", profile=["northeast", "stew", "pork"]),
    City(code="650100", name="乌鲁木齐", province="新疆", region="northwest", climate_zone="dry_northwest", profile=["northwest", "beef_lamb", "wheat"]),
    City(code="370200", name="青岛", province="山东", region="east", climate_zone="coastal_north", profile=["east", "aquatic", "seafood"]),
    City(code="420100", name="武汉", province="湖北", region="central", climate_zone="humid_central", profile=["central", "freshwater", "spicy"]),
    City(code="610100", name="西安", province="陕西", region="northwest", climate_zone="dry_northwest", profile=["northwest", "wheat", "beef_lamb"]),
    City(code="350200", name="厦门", province="福建", region="south", climate_zone="coastal_south", profile=["south", "seafood", "light"]),
]


def part(id_: str, name: str, parent: str, aliases: list[str], methods: list[str]) -> IngredientPart:
    return IngredientPart(id=id_, name=name, parent_id=parent, aliases=aliases, cooking_methods=methods)


INGREDIENTS: List[Ingredient] = [
    Ingredient(id="tomato", name="西红柿", category=IngredientCategory.vegetable, subcategory="瓜茄类", aliases=["番茄"], pinyin="xihongshi fanqie", common_score=0.98, seasonal_months=[5, 6, 7, 8, 9], climate_zones=["temperate_north", "humid_east", "subtropical_south", "basin_southwest"], cooking_methods=["炒", "炖", "凉拌", "煮汤"], pairings=["egg", "beef", "tofu"], notes="家常高频蔬菜，适合快手炒菜和汤。"),
    Ingredient(id="cucumber", name="黄瓜", category=IngredientCategory.vegetable, subcategory="瓜类", aliases=["青瓜"], pinyin="huanggua qinggua", common_score=0.95, seasonal_months=[5, 6, 7, 8, 9], cooking_methods=["凉拌", "清炒", "拍拌"], pairings=["egg", "pork_lean", "shrimp"], notes="夏季清爽，适合凉拌和快炒。"),
    Ingredient(id="bitter_melon", name="苦瓜", category=IngredientCategory.vegetable, subcategory="瓜类", aliases=["凉瓜"], pinyin="kugua lianggua", common_score=0.7, seasonal_months=[5, 6, 7, 8, 9], climate_zones=["subtropical_south", "coastal_south", "basin_southwest"], cooking_methods=["炒", "酿", "煲汤"], pairings=["egg", "pork_ribs"], notes="夏季常见，南方推荐权重更高。"),
    Ingredient(id="loofah", name="丝瓜", category=IngredientCategory.vegetable, subcategory="瓜类", aliases=["水瓜"], pinyin="sigua shuigua", common_score=0.78, seasonal_months=[5, 6, 7, 8, 9], climate_zones=["subtropical_south", "humid_east", "coastal_south"], cooking_methods=["清炒", "煮汤", "蒸"], pairings=["egg", "clam", "shrimp"], notes="适合夏季清淡菜和汤。"),
    Ingredient(id="winter_melon", name="冬瓜", category=IngredientCategory.vegetable, subcategory="瓜类", aliases=["白瓜"], pinyin="donggua baigua", common_score=0.82, seasonal_months=[6, 7, 8, 9, 10], cooking_methods=["炖汤", "红烧", "清炒"], pairings=["pork_ribs", "shrimp", "duck"], notes="适合汤菜，夏秋推荐。"),
    Ingredient(id="eggplant", name="茄子", category=IngredientCategory.vegetable, subcategory="瓜茄类", aliases=["茄瓜"], pinyin="qiezi", common_score=0.92, seasonal_months=[5, 6, 7, 8, 9, 10], cooking_methods=["红烧", "蒸", "鱼香", "煎"], pairings=["pork_lean", "garlic", "green_pepper"], notes="下饭菜高频食材。"),
    Ingredient(id="green_pepper", name="青椒", category=IngredientCategory.vegetable, subcategory="椒类", aliases=["菜椒", "尖椒"], pinyin="qingjiao caijiao jianjiao", common_score=0.9, seasonal_months=[5, 6, 7, 8, 9, 10], cooking_methods=["炒", "虎皮", "凉拌"], pairings=["pork_lean", "egg", "potato"], notes="适合快炒。"),
    Ingredient(id="potato", name="土豆", category=IngredientCategory.vegetable, subcategory="根茎类", aliases=["马铃薯"], pinyin="tudou malingshu", common_score=0.99, seasonal_months=[1, 2, 3, 4, 5, 9, 10, 11, 12], cooking_methods=["炒", "炖", "焖", "煎"], pairings=["beef", "chicken", "green_pepper"], notes="全年供应，价格稳定。"),
    Ingredient(id="carrot", name="胡萝卜", category=IngredientCategory.vegetable, subcategory="根茎类", aliases=["红萝卜"], pinyin="huluobo hongluobo", common_score=0.88, seasonal_months=[1, 2, 3, 10, 11, 12], cooking_methods=["炒", "炖", "煮汤"], pairings=["beef", "pork_ribs", "egg"], notes="常年供应。"),
    Ingredient(id="lotus_root", name="莲藕", category=IngredientCategory.vegetable, subcategory="水生蔬菜", aliases=["藕"], pinyin="lianou ou", common_score=0.8, seasonal_months=[8, 9, 10, 11, 12], climate_zones=["humid_central", "humid_east", "subtropical_south"], cooking_methods=["炖汤", "清炒", "凉拌"], pairings=["pork_ribs", "pork_lean"], region_tags=["central"], notes="湖北等地偏好更高。"),
    Ingredient(id="water_spinach", name="空心菜", category=IngredientCategory.vegetable, subcategory="叶菜类", aliases=["通菜", "蕹菜"], pinyin="kongxincai tongcai wengcai", common_score=0.76, seasonal_months=[5, 6, 7, 8, 9], climate_zones=["subtropical_south", "coastal_south"], cooking_methods=["清炒", "蒜蓉"], pairings=["garlic", "chili"], region_tags=["south"], notes="南方夏季高频叶菜。"),
    Ingredient(id="bok_choy", name="小白菜", category=IngredientCategory.vegetable, subcategory="叶菜类", aliases=["青菜", "上海青"], pinyin="xiaobaicai qingcai shanghaiqing", common_score=0.91, seasonal_months=[1, 2, 3, 4, 10, 11, 12], cooking_methods=["清炒", "煮汤", "焯拌"], pairings=["mushroom", "tofu", "pork_lean"], notes="叶菜高频项。"),
    Ingredient(id="spinach", name="菠菜", category=IngredientCategory.vegetable, subcategory="叶菜类", aliases=["菠薐"], pinyin="bocai", common_score=0.84, seasonal_months=[1, 2, 3, 4, 11, 12], cooking_methods=["焯拌", "煮汤", "清炒"], pairings=["egg", "tofu"], notes="春冬推荐。"),
    Ingredient(id="chinese_cabbage", name="大白菜", category=IngredientCategory.vegetable, subcategory="叶菜类", aliases=["白菜"], pinyin="dabaicai baicai", common_score=0.9, seasonal_months=[1, 2, 10, 11, 12], climate_zones=["temperate_north", "cold_northeast"], cooking_methods=["炖", "炒", "煮汤"], pairings=["pork", "tofu", "vermicelli"], region_tags=["north", "northeast"], notes="北方秋冬高频。"),
    Ingredient(id="garlic", name="大蒜", category=IngredientCategory.vegetable, subcategory="葱姜蒜香草", aliases=["蒜"], pinyin="dasuan suan", common_score=0.96, seasonal_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], cooking_methods=["爆香", "蒜蓉", "腌"], pairings=["water_spinach", "eggplant", "clam"], notes="调味高频。"),
    Ingredient(id="shiitake", name="香菇", category=IngredientCategory.mushroom, subcategory="菌菇", aliases=["冬菇"], pinyin="xianggu donggu", forms=[FreshnessForm.fresh, FreshnessForm.dried], common_score=0.84, seasonal_months=[1, 2, 3, 9, 10, 11, 12], cooking_methods=["炒", "炖", "焖"], pairings=["chicken", "bok_choy", "tofu"], notes="鲜干皆常见。"),
    Ingredient(id="enoki", name="金针菇", category=IngredientCategory.mushroom, subcategory="菌菇", aliases=["金菇"], pinyin="jinzhengu jingu", common_score=0.8, seasonal_months=[1, 2, 3, 4, 10, 11, 12], cooking_methods=["煮", "蒸", "凉拌"], pairings=["beef", "tofu", "egg"], notes="火锅和快手菜常用。"),
    Ingredient(id="tofu", name="豆腐", category=IngredientCategory.soy, subcategory="豆制品", aliases=["北豆腐", "嫩豆腐"], pinyin="doufu", common_score=0.93, seasonal_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], cooking_methods=["煎", "炖", "烧", "煮汤"], pairings=["pork_lean", "bok_choy", "egg"], notes="豆制品作为搭配食材。"),
    Ingredient(id="pork", name="猪肉", category=IngredientCategory.meat, subcategory="畜肉", aliases=["猪鲜肉"], pinyin="zhurou", common_score=0.98, seasonal_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], cooking_methods=["炒", "炖", "红烧", "蒸"], pairings=["green_pepper", "eggplant", "bok_choy"], region_tags=["north", "northeast", "southwest"], notes="最常见肉类。", parts=[
        part("pork_belly", "五花肉", "pork", ["三层肉"], ["红烧", "回锅", "煎"]),
        part("pork_lean", "瘦肉", "pork", ["里脊肉", "精瘦肉"], ["快炒", "滑炒", "煮汤"]),
        part("pork_ribs", "排骨", "pork", ["肋排"], ["炖汤", "红烧", "蒸"]),
    ]),
    Ingredient(id="beef", name="牛肉", category=IngredientCategory.meat, subcategory="畜肉", aliases=["黄牛肉"], pinyin="niurou", common_score=0.86, seasonal_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], cooking_methods=["炒", "炖", "卤", "煎"], pairings=["tomato", "potato", "enoki"], region_tags=["northwest", "north"], notes="西北和北方推荐权重更高。", parts=[
        part("beef_shank", "牛腱", "beef", ["腱子肉"], ["卤", "炖"]),
        part("beef_brisket", "牛腩", "beef", ["坑腩"], ["炖", "红烧"]),
    ]),
    Ingredient(id="lamb", name="羊肉", category=IngredientCategory.meat, subcategory="畜肉", aliases=["羔羊肉"], pinyin="yangrou", common_score=0.72, seasonal_months=[1, 2, 10, 11, 12], cooking_methods=["炖", "炒", "涮"], pairings=["carrot", "potato", "scallion"], region_tags=["northwest", "north"], notes="冬季和西北推荐更高。"),
    Ingredient(id="chicken", name="鸡肉", category=IngredientCategory.poultry, subcategory="禽肉", aliases=["鲜鸡"], pinyin="jirou", common_score=0.93, seasonal_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], cooking_methods=["炒", "炖", "蒸", "煎"], pairings=["shiitake", "potato", "green_pepper"], notes="白肉高频。", parts=[
        part("chicken_wing", "鸡翅", "chicken", ["鸡中翅"], ["红烧", "烤", "煎"]),
        part("chicken_leg", "鸡腿", "chicken", ["琵琶腿"], ["炖", "煎", "卤"]),
        part("chicken_breast", "鸡胸肉", "chicken", ["鸡大胸"], ["煎", "凉拌", "滑炒"]),
    ]),
    Ingredient(id="duck", name="鸭肉", category=IngredientCategory.poultry, subcategory="禽肉", aliases=["鸭"], pinyin="yarou ya", common_score=0.72, seasonal_months=[5, 6, 7, 8, 9, 10], cooking_methods=["炖", "焖", "啤酒鸭"], pairings=["winter_melon", "potato"], region_tags=["south"], notes="南方和夏季汤菜适配。"),
    Ingredient(id="egg", name="鸡蛋", category=IngredientCategory.egg, subcategory="蛋类", aliases=["鲜鸡蛋"], pinyin="jidan", common_score=0.99, seasonal_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], cooking_methods=["炒", "蒸", "煮", "煎"], pairings=["tomato", "loofah", "spinach"], notes="家常万能搭配。"),
    Ingredient(id="grass_carp", name="草鱼", category=IngredientCategory.aquatic, subcategory="淡水鱼", aliases=["鲩鱼"], pinyin="caoyu huanyu", common_score=0.75, seasonal_months=[4, 5, 6, 7, 8, 9, 10], cooking_methods=["红烧", "水煮", "清蒸"], pairings=["tofu", "chili"], region_tags=["central", "south"], notes="淡水鱼高频。"),
    Ingredient(id="crucian_carp", name="鲫鱼", category=IngredientCategory.aquatic, subcategory="淡水鱼", aliases=["鲫瓜子"], pinyin="jiyu", common_score=0.72, seasonal_months=[1, 2, 3, 4, 10, 11, 12], cooking_methods=["煎", "炖汤", "红烧"], pairings=["tofu", "radish"], region_tags=["central", "east"], notes="适合汤。"),
    Ingredient(id="sea_bass", name="鲈鱼", category=IngredientCategory.aquatic, subcategory="海水鱼", aliases=["花鲈"], pinyin="luyu hualu", common_score=0.78, seasonal_months=[4, 5, 6, 7, 8, 9, 10], cooking_methods=["清蒸", "红烧", "煎"], pairings=["ginger", "scallion"], region_tags=["east", "south", "seafood"], notes="清蒸友好。"),
    Ingredient(id="hairtail", name="带鱼", category=IngredientCategory.aquatic, subcategory="海水鱼", aliases=["刀鱼"], pinyin="daiyu daoyu", forms=[FreshnessForm.fresh, FreshnessForm.frozen], common_score=0.74, seasonal_months=[1, 2, 10, 11, 12], cooking_methods=["红烧", "煎", "炸"], pairings=["green_pepper"], region_tags=["east", "north"], notes="常见海鱼。"),
    Ingredient(id="shrimp", name="虾", category=IngredientCategory.aquatic, subcategory="虾蟹贝螺", aliases=["鲜虾", "基围虾"], pinyin="xia xianxia jiweixia", forms=[FreshnessForm.fresh, FreshnessForm.frozen], common_score=0.82, seasonal_months=[4, 5, 6, 7, 8, 9, 10], cooking_methods=["白灼", "清炒", "蒸"], pairings=["loofah", "cucumber", "egg"], region_tags=["south", "east", "seafood"], notes="沿海推荐更高。", parts=[part("shrimp_meat", "虾仁", "shrimp", ["青虾仁"], ["滑炒", "蒸蛋", "煮汤"])]),
    Ingredient(id="clam", name="蛤蜊", category=IngredientCategory.aquatic, subcategory="虾蟹贝螺", aliases=["花甲", "花蛤"], pinyin="geli huajia huage", common_score=0.68, seasonal_months=[5, 6, 7, 8, 9], cooking_methods=["爆炒", "煮汤", "蒸"], pairings=["loofah", "garlic", "chili"], region_tags=["south", "east", "seafood"], notes="沿海城市推荐。"),
    Ingredient(id="squid", name="鱿鱼", category=IngredientCategory.aquatic, subcategory="头足类", aliases=["鲜鱿"], pinyin="youyu xianyou", forms=[FreshnessForm.fresh, FreshnessForm.frozen], common_score=0.62, seasonal_months=[4, 5, 6, 7, 8, 9, 10], cooking_methods=["爆炒", "白灼", "烧烤"], pairings=["green_pepper", "garlic"], region_tags=["seafood", "south"], notes="头足类高频。"),
    Ingredient(id="kelp", name="海带", category=IngredientCategory.aquatic, subcategory="海藻水产", aliases=["昆布"], pinyin="haidai kunbu", forms=[FreshnessForm.fresh, FreshnessForm.dried], common_score=0.72, seasonal_months=[1, 2, 3, 4, 5, 10, 11, 12], cooking_methods=["凉拌", "炖汤", "煮"], pairings=["pork_ribs", "tofu"], region_tags=["east", "north"], notes="海藻类。"),
    Ingredient(id="sausage", name="香肠", category=IngredientCategory.processed, subcategory="加工肉制品", aliases=["腊肠"], pinyin="xiangchang lachang", forms=[FreshnessForm.processed], common_score=0.52, seasonal_months=[1, 2, 11, 12], cooking_methods=["蒸", "炒", "煲饭"], pairings=["green_pepper", "potato"], notes="加工品只作为搭配和搜索，不做健康主推荐。"),
    Ingredient(id="bacon", name="培根", category=IngredientCategory.processed, subcategory="加工肉制品", aliases=["烟肉"], pinyin="peigen yanrou", forms=[FreshnessForm.processed], common_score=0.42, seasonal_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], cooking_methods=["煎", "炒"], pairings=["enoki", "egg", "potato"], notes="高频加工搭配。"),
    Ingredient(id="fish_ball", name="鱼丸", category=IngredientCategory.processed, subcategory="加工水产", aliases=["鱼蛋"], pinyin="yuwan yudan", forms=[FreshnessForm.processed], common_score=0.5, seasonal_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], cooking_methods=["煮", "炒", "火锅"], pairings=["bok_choy", "tofu"], notes="加工水产搭配。"),
]


PRICE_SNAPSHOTS: List[PriceSnapshot] = [
    PriceSnapshot(ingredient_id="tomato", city_code="110100", avg_price_yuan_per_jin=3.2, low_price_yuan_per_jin=2.5, high_price_yuan_per_jin=4.2, source="北京价格监测样例", source_level="city", confidence=0.86, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="cucumber", city_code="110100", avg_price_yuan_per_jin=2.4, low_price_yuan_per_jin=1.8, high_price_yuan_per_jin=3.2, source="北京价格监测样例", source_level="city", confidence=0.86, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="pork", city_code="110100", avg_price_yuan_per_jin=14.8, low_price_yuan_per_jin=12.8, high_price_yuan_per_jin=17.5, source="北京价格监测样例", source_level="city", confidence=0.82, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="egg", city_code="110100", avg_price_yuan_per_jin=4.8, low_price_yuan_per_jin=4.2, high_price_yuan_per_jin=5.6, source="北京价格监测样例", source_level="city", confidence=0.85, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="sea_bass", city_code="440100", avg_price_yuan_per_jin=18.0, low_price_yuan_per_jin=15.0, high_price_yuan_per_jin=22.0, source="广州市场参考样例", source_level="city", confidence=0.78, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="shrimp", city_code="440100", avg_price_yuan_per_jin=28.0, low_price_yuan_per_jin=23.0, high_price_yuan_per_jin=34.0, source="广州市场参考样例", source_level="city", confidence=0.76, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="water_spinach", city_code="440100", avg_price_yuan_per_jin=3.0, low_price_yuan_per_jin=2.2, high_price_yuan_per_jin=4.0, source="广州市场参考样例", source_level="city", confidence=0.8, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="beef", city_code="650100", avg_price_yuan_per_jin=35.0, low_price_yuan_per_jin=31.0, high_price_yuan_per_jin=42.0, source="乌鲁木齐市场参考样例", source_level="city", confidence=0.76, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="lamb", city_code="650100", avg_price_yuan_per_jin=36.0, low_price_yuan_per_jin=32.0, high_price_yuan_per_jin=43.0, source="乌鲁木齐市场参考样例", source_level="city", confidence=0.76, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="grass_carp", city_code="420100", avg_price_yuan_per_jin=9.0, low_price_yuan_per_jin=7.5, high_price_yuan_per_jin=11.0, source="武汉市场参考样例", source_level="city", confidence=0.78, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="lotus_root", city_code="420100", avg_price_yuan_per_jin=4.2, low_price_yuan_per_jin=3.5, high_price_yuan_per_jin=5.5, source="武汉市场参考样例", source_level="city", confidence=0.78, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="pork", province="四川", avg_price_yuan_per_jin=13.6, low_price_yuan_per_jin=11.8, high_price_yuan_per_jin=16.0, source="省级价格参考样例", source_level="province", confidence=0.68, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="eggplant", region="southwest", avg_price_yuan_per_jin=2.8, low_price_yuan_per_jin=2.0, high_price_yuan_per_jin=3.8, source="区域价格参考样例", source_level="region", confidence=0.62, updated_at="2026-06-17"),
    PriceSnapshot(ingredient_id="chicken", region="northwest", avg_price_yuan_per_jin=11.0, low_price_yuan_per_jin=9.5, high_price_yuan_per_jin=13.5, source="区域价格参考样例", source_level="region", confidence=0.62, updated_at="2026-06-17"),
]


NATIONAL_PRICE_BASELINE: Dict[str, tuple[float, float, float]] = {
    "tomato": (3.5, 2.4, 5.0),
    "cucumber": (2.8, 1.8, 4.2),
    "bitter_melon": (4.0, 2.8, 6.0),
    "loofah": (3.8, 2.5, 5.8),
    "winter_melon": (1.8, 1.1, 3.0),
    "eggplant": (3.2, 2.2, 4.8),
    "green_pepper": (3.8, 2.5, 5.8),
    "potato": (1.9, 1.2, 3.0),
    "carrot": (2.3, 1.5, 3.5),
    "lotus_root": (4.8, 3.4, 7.0),
    "water_spinach": (3.5, 2.4, 5.2),
    "bok_choy": (2.7, 1.8, 4.2),
    "spinach": (4.0, 2.8, 6.2),
    "chinese_cabbage": (1.6, 0.9, 2.8),
    "garlic": (5.0, 3.6, 7.5),
    "shiitake": (7.5, 5.0, 11.0),
    "enoki": (4.5, 3.0, 7.0),
    "tofu": (2.5, 1.8, 3.8),
    "pork": (14.0, 11.5, 18.0),
    "beef": (38.0, 32.0, 48.0),
    "lamb": (39.0, 33.0, 50.0),
    "chicken": (10.5, 8.5, 13.5),
    "duck": (11.0, 8.5, 15.0),
    "egg": (4.9, 4.0, 6.2),
    "grass_carp": (8.5, 6.8, 11.0),
    "crucian_carp": (12.0, 9.0, 16.0),
    "sea_bass": (20.0, 16.0, 26.0),
    "hairtail": (16.0, 12.0, 23.0),
    "shrimp": (30.0, 22.0, 40.0),
    "clam": (8.0, 5.5, 12.0),
    "squid": (18.0, 13.0, 26.0),
    "kelp": (3.2, 2.0, 5.0),
    "sausage": (28.0, 20.0, 40.0),
    "bacon": (32.0, 24.0, 45.0),
    "fish_ball": (13.0, 9.0, 18.0),
}


CITY_BY_CODE = {city.code: city for city in CITIES}
INGREDIENT_BY_ID = {item.id: item for item in INGREDIENTS}
PART_BY_ID = {part.id: part for item in INGREDIENTS for part in item.parts}


def list_cities() -> List[City]:
    return CITIES


def get_city(city_code: str) -> City:
    return CITY_BY_CODE.get(city_code, CITY_BY_CODE["110100"])


def get_ingredient(ingredient_id: str) -> Optional[Ingredient]:
    if ingredient_id in INGREDIENT_BY_ID:
        return INGREDIENT_BY_ID[ingredient_id]
    part_obj = PART_BY_ID.get(ingredient_id)
    if part_obj:
        return INGREDIENT_BY_ID.get(part_obj.parent_id)
    return None


def list_ingredients(category: Optional[IngredientCategory] = None, keyword: str = "") -> List[Ingredient]:
    keyword_normalized = keyword.strip().lower()
    results: List[Ingredient] = []
    for item in INGREDIENTS:
        if category and item.category != category:
            continue
        haystack = " ".join([item.id, item.name, item.pinyin, *item.aliases, item.subcategory]).lower()
        part_haystack = " ".join([p.id + " " + p.name + " " + " ".join(p.aliases) for p in item.parts]).lower()
        if keyword_normalized and keyword_normalized not in haystack and keyword_normalized not in part_haystack:
            continue
        results.append(item)
    return sorted(results, key=lambda ingredient: (-ingredient.common_score, ingredient.name))


def find_price_snapshot(ingredient_id: str, city: City) -> Optional[PriceSnapshot]:
    for snapshot in PRICE_SNAPSHOTS:
        if snapshot.ingredient_id == ingredient_id and snapshot.city_code == city.code:
            return snapshot
    for snapshot in PRICE_SNAPSHOTS:
        if snapshot.ingredient_id == ingredient_id and snapshot.province == city.province:
            return snapshot
    for snapshot in PRICE_SNAPSHOTS:
        if snapshot.ingredient_id == ingredient_id and snapshot.region == city.region:
            return snapshot
    baseline = NATIONAL_PRICE_BASELINE.get(ingredient_id)
    if baseline:
        avg, low, high = baseline
        return PriceSnapshot(
            ingredient_id=ingredient_id,
            avg_price_yuan_per_jin=avg,
            low_price_yuan_per_jin=low,
            high_price_yuan_per_jin=high,
            source="全国批发价/市场价基线样例",
            source_level="national",
            confidence=0.45,
            updated_at=date.today().isoformat(),
        )
    return None


def all_categories() -> Iterable[IngredientCategory]:
    return IngredientCategory
