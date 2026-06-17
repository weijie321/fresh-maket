from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_search_finds_vegetables_parts_aquatic_and_processed():
    assert client.get("/v1/ingredients", params={"keyword": "空心菜"}).json()[0]["id"] == "water_spinach"
    pork = client.get("/v1/ingredients", params={"keyword": "五花肉"}).json()
    assert pork and pork[0]["id"] == "pork"
    clam = client.get("/v1/ingredients", params={"keyword": "花甲"}).json()
    assert clam and clam[0]["id"] == "clam"
    sausage = client.get("/v1/ingredients", params={"category": "processed", "keyword": "香肠"}).json()
    assert sausage and sausage[0]["category"] == "processed"


def test_recommendations_change_by_city_profile():
    guangzhou = client.get("/v1/recommendations/today", params={"cityCode": "440100", "date": "2026-06-17"}).json()
    urumqi = client.get("/v1/recommendations/today", params={"cityCode": "650100", "date": "2026-06-17"}).json()

    guangzhou_aquatic = [item["ingredient"]["id"] for item in guangzhou["groups"]["today_aquatic"][:3]]
    urumqi_meat = [item["ingredient"]["id"] for item in urumqi["groups"]["today_meat_poultry_egg"][:3]]

    assert "sea_bass" in guangzhou_aquatic or "shrimp" in guangzhou_aquatic
    assert "beef" in urumqi_meat or "lamb" in urumqi_meat
    assert guangzhou["city"]["name"] == "广州"
    assert urumqi["city"]["name"] == "乌鲁木齐"


def test_price_fallback_source_level_is_visible():
    city_price = client.get("/v1/prices", params={"cityCode": "440100", "ingredientIds": "shrimp"}).json()[0]
    national_price = client.get("/v1/prices", params={"cityCode": "440100", "ingredientIds": "potato"}).json()[0]

    assert city_price["source_level"] == "city"
    assert national_price["source_level"] == "national"
    assert national_price["value_label"] in {"参考", "正常", "划算", "偏贵"}


def test_expensive_or_missing_items_are_not_marked_as_value():
    prices = client.get("/v1/prices", params={"cityCode": "440100", "ingredientIds": "bacon"}).json()
    assert prices[0]["value_label"] != "划算"


def test_recipe_generation_works_for_vegetable_meat_aquatic_and_processed():
    payload = {
        "city_code": "440100",
        "ingredient_ids": ["loofah", "shrimp", "bacon"],
        "people_count": 2,
        "cooking_time_minutes": 20,
        "taste_tags": ["清淡"],
    }
    recipes = client.post("/v1/recipes/generate", json=payload).json()

    assert len(recipes) >= 3
    assert all(recipe["steps"] for recipe in recipes)
    assert any("丝瓜" in "".join(recipe["ingredient_names"]) for recipe in recipes)
