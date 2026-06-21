# Project Agent Notes

本项目是“今日菜价 Fresh Market V1”：Android 原生客户端 + FastAPI 后端。

## 运行与构建

- 后端入口：`backend/app/main.py`，本地默认运行在 `127.0.0.1:8000`。
- 后端测试命令：`cd backend; .\.venv\Scripts\python.exe -m pytest -q`。
- Android 客户端默认 API：`http://10.0.2.2:8000`，真机调试时用 `-PapiBaseUrl=http://<电脑局域网IP>:8000` 构建，不要手改源码。
- Android 客户端 `minSdk` 为 21，已在 OPPO R9 Plusm A（Android 5.1.1 / API 22）上安装并启动验证。
- 本机 Android 构建使用 `E:\work\jdk\21`、`E:\work\toolchain\android-sdk`、`E:\work\toolchain\gradle-8.10.2\bin\gradle.bat`。
- `local.properties`、`.venv/`、`.gradle/`、`android/app/build/` 都是本机产物，不要提交。

## 代码边界

- 食材库、价格样例和城市数据目前在 `backend/app/data.py`，推荐逻辑在 `backend/app/services/recommendations.py`。
- “食材库收录”和“首页推荐”保持分离：食材可查不代表一定推荐。
- 价格口径是城市参考价/区间，不是具体门店实时价。
- 没有配置 `DEEPSEEK_API_KEY` 时，菜谱生成走模板兜底，不应破坏离线可测性。
