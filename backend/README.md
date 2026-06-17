# Fresh Market API

FastAPI 后端，提供完整生鲜食材库、当地参考价、今日推荐和菜谱生成。

## 运行

```powershell
.\run-dev.bat
```

## 测试

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## 示例

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/v1/recommendations/today?cityCode=440100"

Invoke-RestMethod "http://127.0.0.1:8000/v1/ingredients?keyword=五花肉"

Invoke-RestMethod "http://127.0.0.1:8000/v1/prices?cityCode=440100&ingredientIds=shrimp,potato"
```
