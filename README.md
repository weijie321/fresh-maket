# 今日菜价 Fresh Market V1

一个“完整生鲜食材库 + 今日当地推荐”的 Android 原生 App 与后端 API 原型。

V1 的核心原则：

- 食材库要全，推荐不等于收录。
- 蔬菜、肉禽蛋、水产、少量高频加工品都能搜索和生成做法。
- 首页只主动推荐当地更适合今天购买的食材和搭配。
- 当地价格展示为参考价与区间，不承诺具体门店实时价。
- 不做交易、不接买菜平台、不做账号登录。

## 项目结构

```text
backend/        FastAPI 服务、种子数据、推荐/价格/菜谱逻辑、测试
android/app/    Kotlin + Jetpack Compose Android 客户端
docker-compose.yml
```

## 后端本地运行

Windows 双击或运行：

```powershell
E:\work\code\fresh-market-v1\backend\run-dev.bat
```

或者：

```powershell
cd E:\work\code\fresh-market-v1\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

接口文档：

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## 关键接口

- `GET /v1/cities`：城市列表。
- `GET /v1/ingredients?category=vegetable|meat|poultry|egg|aquatic|processed&keyword=...`：全库搜索。
- `GET /v1/recommendations/today?cityCode=440100&date=2026-06-17`：今日当地推荐。
- `GET /v1/prices?cityCode=440100&ingredientIds=shrimp,potato`：参考价格。
- `GET /v1/ingredients/{id}`：食材详情。
- `POST /v1/recipes/generate`：生成家常做法。
- `POST /v1/feedback`：匿名反馈入口。

## Android 运行

客户端默认 API 地址是 Android 模拟器访问宿主机的：

```text
http://10.0.2.2:8000
```

真机调试时，把 `android/app/build.gradle.kts` 中的 `API_BASE_URL` 改为电脑局域网 IP，例如：

```kotlin
buildConfigField("String", "API_BASE_URL", "\"http://192.168.1.10:8000\"")
```

然后用 Android Studio 打开 `E:\work\code\fresh-market-v1` 运行 `android:app`。

## 测试

```powershell
cd E:\work\code\fresh-market-v1\backend
.\.venv\Scripts\python.exe -m pytest -q
```

当前覆盖：

- 小众蔬菜、肉类部位、水产别名、加工品搜索。
- 广州和乌鲁木齐的地域推荐差异。
- 城市价与全国价兜底来源展示。
- 价格高或低置信食材不标“划算”。
- 蔬菜、肉类、水产、加工品组合菜谱生成。

## 后续接入点

- 真实价格源：替换 `backend/app/data.py` 中的 `PRICE_SNAPSHOTS`，或新增定时任务写入数据库。
- PostgreSQL：当前 Docker 已提供数据库服务，业务代码仍用内存种子数据，下一步可把 `ingredients`、`price_snapshots` 等迁入 ORM。
- DeepSeek：在后端设置 `DEEPSEEK_API_KEY` 后，把 `backend/app/services/recipes.py` 的隔离点替换为真实模型调用。
- 运营后台：为城市价格修正、食材别名、地域偏好和推荐权重提供管理页。
