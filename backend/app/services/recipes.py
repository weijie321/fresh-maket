from __future__ import annotations

import os
from typing import List

from .. import data
from ..models import RecipeCard, RecipeRequest


def ingredient_names(ids: List[str]) -> List[str]:
    names: List[str] = []
    for id_ in ids:
        item = data.get_ingredient(id_)
        if item:
            part = data.PART_BY_ID.get(id_)
            names.append(part.name if part else item.name)
    return names


def base_method(names: List[str], time_minutes: int) -> tuple[str, list[str]]:
    joined = "、".join(names)
    if any(name in joined for name in ["鲈鱼", "虾", "蛤蜊", "草鱼", "鲫鱼"]):
        return "清蒸/白灼", ["姜葱去腥", "大火短时间加热", "出锅后再淋热油或调味汁"]
    if any(name in joined for name in ["排骨", "牛腩", "羊肉"]):
        return "炖煮", ["先焯水去浮沫", "小火炖到软烂", "最后再调盐避免肉质发紧"]
    if time_minutes <= 20:
        return "快炒", ["食材切薄切小", "热锅快炒", "最后调味保持脆嫩"]
    return "家常烧", ["先煎炒出香味", "加少量水焖熟", "收汁后出锅"]


def fallback_recipes(request: RecipeRequest) -> List[RecipeCard]:
    names = ingredient_names(request.ingredient_ids)
    if not names:
        names = ["当季蔬菜"]
    method, tips = base_method(names, request.cooking_time_minutes)
    people = request.people_count
    joined = "、".join(names)
    cards = [
        RecipeCard(
            title=f"{joined}家常{method}",
            ingredient_names=names,
            time_minutes=min(max(request.cooking_time_minutes, 10), 45),
            difficulty="简单",
            ingredients=[f"{name}适量" for name in names] + [f"{people}人份主食按需准备"],
            seasonings=["盐", "生抽", "食用油", "葱姜蒜", "少量白胡椒"],
            steps=[
                f"将{joined}清洗处理，按易熟程度分别切好。",
                "热锅加油，先下葱姜蒜或耐炒食材炒出香味。",
                f"加入主要食材，用{method}方式烹调到断生或熟透。",
                "加入盐和生抽调味，口味重可少量加辣椒或醋。",
                "出锅前尝味，汤菜补热水，炒菜收干多余汤汁。",
            ],
            substitutions=["没有其中一种食材时，可用同类蔬菜或蛋类替换。", "水产可换鸡肉，猪肉可换豆腐做清淡版。"],
            tips=tips,
            source="template",
        ),
        RecipeCard(
            title=f"{joined}少油快手版",
            ingredient_names=names,
            time_minutes=min(max(request.cooking_time_minutes - 3, 8), 30),
            difficulty="简单",
            ingredients=[f"{name}适量" for name in names],
            seasonings=["盐", "蚝油或生抽", "蒜末", "少量淀粉水"],
            steps=[
                "食材提前沥干水分，肉类或水产用少量盐和淀粉抓匀。",
                "锅中放少量油，先处理肉类或水产，变色后盛出。",
                "再下蔬菜翻炒，沿锅边加一小勺水帮助成熟。",
                "倒回肉类或水产，加入调味料快速翻匀。",
                "用少量淀粉水薄薄挂汁即可出锅。",
            ],
            substitutions=["蚝油可换生抽加一点糖。", "不吃辣可省略辣椒，想更香可加黑胡椒。"],
            tips=["少油版本要用中大火快速完成。", "叶菜最后放，避免出水过多。"],
            source="template",
        ),
        RecipeCard(
            title=f"{joined}一锅汤菜",
            ingredient_names=names,
            time_minutes=max(request.cooking_time_minutes, 20),
            difficulty="简单",
            ingredients=[f"{name}适量" for name in names] + ["清水或高汤"],
            seasonings=["盐", "姜片", "白胡椒", "葱花"],
            steps=[
                "耐煮食材先下锅，肉类先焯水或煎香。",
                "加入清水或高汤煮开，转中小火煮出味道。",
                "再加入易熟蔬菜或水产，煮到刚熟。",
                "用盐和白胡椒调味，出锅撒葱花。",
            ],
            substitutions=["排骨可换鸡腿，鱼虾可换豆腐。", "清淡版只用盐和姜片即可。"],
            tips=["水产下锅后不要久煮。", "汤菜适合搭配米饭或面条。"],
            source="template",
        ),
    ]
    return cards


async def generate_recipes(request: RecipeRequest) -> List[RecipeCard]:
    # The DeepSeek integration point is intentionally isolated. Configure
    # DEEPSEEK_API_KEY later to replace this deterministic fallback.
    if not os.getenv("DEEPSEEK_API_KEY"):
        return fallback_recipes(request)
    return fallback_recipes(request)
