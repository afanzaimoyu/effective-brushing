<div align="center">
    <!-- 带超链接的技术徽章 -->
    <a href="https://docs.python.org/zh-cn/3/" target="_blank"><img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version"></a>
    <a href="https://fastapi.tiangolo.com/" target="_blank"><img src="https://img.shields.io/badge/FastAPI-0.104.1-green.svg" alt="FastAPI Version"></a>
    <a href="https://python-poetry.org/docs/" target="_blank"><img src="https://img.shields.io/badge/Poetry-1.7+-purple.svg" alt="Poetry Version"></a>
    <a href="https://www.oracle.com/technetwork/cn/database/database-technologies/sql/documentation/index.html" target="_blank"><img src="https://img.shields.io/badge/Oracle-12c+-orange.svg" alt="Oracle Version"></a>
    <a href="https://docs.flutter.dev/" target="_blank"><img src="https://img.shields.io/badge/Flutter-3.16+-cyan.svg" alt="Flutter Version"></a>
    <a href="https://min-io.cn/product/overview" target="_blank"><img src="https://img.shields.io/badge/MinIO-7.2+-red.svg" alt="MinIO Version"></a>
      
<h1>✨ Effective Brushing ✨</h1>

<p>📚 一站式<span style="color:#4299e1; font-weight:bold"><a href="#" target="_blank">题库练习APP</a></span>- 专注高效刷题体验</p>
</div>

---

## 📖 项目简介
Effective Brushing 是一款面向刷题备考场景的移动端应用，核心解决传统刷题工具的痛点，主打以下**核心能力**：
- 🎯 <span style="color:#4299e1; font-weight:bold">多模式练习</span>：支持**顺序练习/随机练习/题型训练/错题练习/收藏练习**，适配不同刷题场景
- 📱 <span style="color:#4299e1; font-weight:bold">离线刷题</span>：题库本地存储，断网状态下正常练习，联网自动同步答题记录
- 🤖 <span style="color:#48bb78; font-weight:bold">AI辅助能力</span>：拍照录题（OCR识别）、AI解析试题、智能试题去重
- 📊 <span style="color:#38b2ac; font-weight:bold">数据化复盘</span>：错因归纳、模拟考试、答题数据统计，精准定位薄弱点
- ⚡ <span style="color:#9f7aea; font-weight:bold">极致交互</span>：答对自动跳转下一题、自定义随机练习数目、一键打乱题目顺序
- 🔒 <span style="color:#9f7aaa; font-weight:bold">生产级稳定性</span>：完善的异常处理、数据库事务、Sentry 监控、日志体系，保障服务高可用
---

## 🛠 核心技术栈（附官方文档）
| 模块     | 技术选型                                                                                                                                        | 官方文档链接                                                                                                                                       |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| 后端核心   | Python 3.10+ + <a href="https://fastapi.org.cn/" target="_blank">FastAPI</a>                                                                | <a href="https://docs.python.org/zh-cn/3/" target="_blank">Python 3.10文档</a>、<a href="https://fastapi.org.cn/" target="_blank">FastAPI文档</a> |
| ORM框架  | <a href="https://www.sqlalchemy.org/" target="_blank">SQLAlchemy 2.0+</a>                                                                   | <a href="https://docs.sqlalchemy.org/en/20/" target="_blank">SQLAlchemy 2.0 文档</a>                                                           |
| 数据库迁移  | <a href="https://alembic.sqlalchemy.org/" target="_blank">Alembic</a>	                                                                      | <a href="https://alembic.sqlalchemy.org/docs/" target="_blank">Alembic 官方文档</a>                                                              |
| 依赖管理   | <a href="https://python-poetry.org" target="_blank">Poetry</a>                                                                              | <a href="https://python-poetry.org/docs/" target="_blank">Poetry官方文档</a>                                                                     |
| 代码规范   | <a href="https://docs.astral.sh/ruff/" target="_blank">Ruff</a>                                                                             | <a href="https://docs.astral.sh/ruff/" target="_blank">Ruff 官方文档</a>                                                                         |
| 数据库    | <a href="https://www.oracle.com/technetwork/cn/database/database-technologies/sql/documentation/index.html" target="_blank">Oracle 12c+</a> | <a href="https://www.oracle.com/technetwork/cn/database/database-technologies/sql/documentation/index.html" target="_blank">Oracle 12c文档</a> |
| 文件存储   | <a href="https://min-io.cn/product/overview" target="_blank">MinIO</a>                                                                      | <a href="https://min-io.cn/docs/minio/kubernetes/upstream/" target="_blank">MinIO Python SDK文档</a>                                           |
| 监控告警   | <a href="https://docs.sentry.io/" target="_blank">Sentry</a>                                                                                | <a href="https://docs.sentry.io/platforms/python/fastapi/" target="_blank">Sentry FastAPI 文档</a>                                             |
|
| 移动端前端  | <a href="https://flutter.dev/" target="_blank">Flutter 3.16+</a>                                                                            | <a href="https://docs.flutter.dev/" target="_blank">Flutter官方文档</a>                                                                          |
| Web管理端 | <a href="https://vuejs.org" target="_blank">Vue 3</a>                                                                                       | <a href="https://vuejs.org/guide/introduction.html" target="_blank">Vue 3文档</a>、<a href="https://react.dev/" target="_blank">React 18文档</a>  |
| 辅助能力   | OCR（百度API）、AI解析（讯飞星火API）                                                                                                                    | <a href="#" target="_blank">百度OCR文档</a>、<a href="#" target="_blank">讯飞星火API文档</a>                                                            |

---

## 📂 项目目录结构
```markdown
effective-brushing/  # 项目根目录
├── backend/          # Python后端（Poetry管理）
│   ├── .env          # 敏感配置（Oracle/MinIO/JWT/Sentry，gitignore）
│   ├── .env.example  # 配置模板（提交git，供参考）
│   ├── alembic.ini   # Alembic数据库迁移配置
│   ├── alembic/      # 数据库迁移脚本目录
│   ├── gunicorn_conf.py # Gunicorn生产服务配置
│   ├── start.sh      # 生产环境启动脚本（赋予执行权限）
│   ├── justfile      # 快捷命令配置（run/migrate/lint等）
│   ├── pyproject.toml # Poetry依赖配置
│   ├── ruff.toml     # Ruff代码规范配置
│   ├── logging_dev.ini # 开发环境日志配置
│   ├── logging_prod.ini # 生产环境日志配置
│   ├── src/          # 核心代码（Poetry推荐src布局）
│   │   ├── main.py   # FastAPI入口文件（生命周期/路由/异常处理）
│   │   ├── api/      # API路由层
│   │   │   └── v1/   # v1版本路由（用户/题库/上传/同步）
│   │   ├── core/     # 核心配置层（数据库/依赖/异常/配置）
│   │   ├── models/   # Oracle数据库模型（SQLAlchemy）
│   │   ├── schemas/  # Pydantic校验模型
│   │   ├── services/ # 业务逻辑层（用户/题库/MinIO/同步）
│   │   └── utils/    # 工具层（JWT/MinIO/Oracle/日志）
│   ├── tests/        # 单元测试/接口测试
│   │   ├── test_api/ # API测试
│   │   ├── test_services/ # 业务逻辑测试
│   │   └── test_utils/ # 工具函数测试
│   ├── logs/         # 日志目录（自动生成，gitignore）
│   └── tmp/          # 临时目录（跨平台兼容，gitignore）
├── frontend/         # 前端代码（前后端分离）
│   ├── mobile/       # Flutter移动端APP
│   │   ├── lib/      # Flutter核心代码
│   │   └── assets/   # 静态资源（图片/字体）
│   └── web/          # Vue 3管理后台
│       ├── src/      # Web核心代码
│       └── public/   # Web静态资源
├── docs/             # 开发文档
│   ├── prd/          # 产品需求文档
│   ├── tdd/          # 技术设计文档
│   ├── db_design/    # Oracle数据库设计（ER图/表结构）
│   └── charts/       # 架构图/流程图
├── .gitignore        # Git忽略规则（根目录）
└── README.md         # 项目总览文档
```

---


## ⚡ 快速启动指南（关键步骤高亮）
### 前置条件
* 已安装 Python 3.10+、Poetry、Oracle 12c+、MinIO 7.2+
* 已配置 Oracle 数据库连接、MinIO 存储桶、JWT 密钥、Sentry DSN（可选）
### 1. 后端启动（核心，分开发 / 生产环境）

#### 进入后端目录
```shell
cd effective-brushing/backend
```
#### ① 安装Poetry（首次使用，<span style="color:#e53e3e; font-weight:bold">必执行</span>）
```shell
# Windows
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python 

# Mac/Linux
curl -sSL https://install.python-poetry.org | python3 

# 验证安装
poetry --version
```
#### ② 配置环境变量（<span style="color:#e53e3e; font-weight:bold">必执行</span>）
```shell
# 复制配置模板并修改实际值（Oracle/MinIO/JWT等）
cp .env.example .env

# 编辑.env文件（根据实际环境配置）
# 关键配置项：DATABASE_ASYNC_URL、MINIO_ACCESS_KEY、JWT_SECRET_KEY、SENTRY_DSN
```
#### ③ 安装项目依赖（自动创建<span style="color:#4299e1; font-weight:bold">.venv虚拟环境</span>）
```shell
poetry install
```
#### ④ 数据库迁移（首次启动，<span style="color:#e53e3e; font-weight:bold">必执行</span>）
```shell
# 初始化迁移（仅首次）
poetry run alembic init alembic

# 生成迁移脚本（替换注释为实际说明）
poetry run alembic revision --autogenerate -m "初始化用户/题库表"

# 执行迁移（同步到Oracle数据库）
poetry run alembic upgrade head
```
#### ③ 启动后端服务（开发 / 生产环境二选一）
#### 开发环境（热重载， 推荐）
```shell
# 方式1：使用justfile快捷命令（推荐）
poetry run just run

# 方式2：直接运行uvicorn
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```
#### 生产环境（Gunicorn 多进程，稳定）
```shell
# 赋予启动脚本执行权限（仅首次）
chmod +x start.sh

# 执行启动脚本
./start.sh
```

#### ✅ 验证启动
* 健康检查：访问 http://localhost:8000/healthcheck ，返回 `{"status":"ok","environment":"local","version":"1.0.0","database":"ok","service":"effective-brushing-backend"}` 即成功
* API 文档：访问 http://localhost:8000/docs 查看 Swagger 文档
* ReDoc 文档：访问 http://localhost:8000/redoc 查看结构化文档

### 2. 移动端前端启动（Flutter）
#### 进入移动端目录
```shell
cd D:\MyProject\effective-brushing\frontend\mobile
```

#### ① 安装Flutter依赖（<span style="color:#e53e3e; font-weight:bold">必执行</span>）
```shell
flutter pub get
```

#### ② 启动模拟器/连接真机后运行（<span style="color:#4299e1; font-weight:bold">核心命令</span>）
```shell
flutter run
```

#### 📦 可选：打包生产环境APK
```shell
flutter build apk --release
```

### 3. Web 前端启动（Vue 3 ）
#### 进入Web目录
```shell
cd D:\MyProject\effective-brushing\frontend\web
```

#### ① 安装npm依赖
```shell
npm install
```

#### ② 启动开发环境（热重载，<span style="color:#4299e1; font-weight:bold">核心命令</span>）
```shell
npm run dev
```

#### 📦 生产环境打包
```shell
npm run build
```
---

## 📝 开发规范（重点强调）
### 1. 后端规范（Poetry+FastAPI+SQLAlchemy）
- <span style="color:#4299e1; font-weight:bold">依赖管理</span>：仅通过`pyproject.toml`添加依赖，执行`poetry add 依赖名`，禁止手动修改`poetry.lock`
- <span style="color:#4299e1; font-weight:bold">代码风格</span>：使用`Ruff`格式化代码（命令：`poetry run ruff format src/`），校验代码（`poetry run ruff check src/ --fix`）
- <span style="color:#4299e1; font-weight:bold">数据库规范</span>：
  * 模型修改后必须执行`alembic revision --autogenerate`生成迁移脚本，禁止直接修改数据库
  * 批量操作 / 跨表操作必须使用事务（`src/core/database.py`的`transaction()`上下文管理器）
  * 禁止硬编码 SQL，全部使用 SQLAlchemy ORM
- <span style="color:#4299e1; font-weight:bold">异常处理</span>：业务异常统一抛出`src/core/exceptions.py`中的自定义异常，禁止直接抛`HTTPException`
- <span style="color:#4299e1; font-weight:bold">测试要求</span>：新增接口必须补充单元测试，测试文件放在`backend/tests/`目录，代码覆盖率≥80%
- <span style="color:#4299e1; font-weight:bold">配置规范</span>：敏感信息（Oracle/MinIO/JWT 密钥）必须写在`backend/.env`文件，禁止硬编码到代码中

### 2. 前端规范（Flutter/Vue）
- **Flutter 规范**：遵循 Dart 官方编码规范，组件按「页面组件/通用组件/业务组件」拆分，文件命名统一为`xxx_widget.dart`
- **Vue/React 规范**：遵循 ESLint 代码规范，提交代码前必须执行`npm run lint`修复格式问题，组件采用按需引入方式

## ⚠ 重要注意事项（核心提醒）
1. <span style="color:#e53e3e; font-weight:bold">敏感配置保护</span>：`backend/.env`文件包含Oracle/MinIO/JWT 密钥等敏感信息，切勿提交到Git（已加入.gitignore，需确认配置生效）
2. <span style="color:#e53e3e; font-weight:bold">环境前置要求</span>：启动后端服务前，需确保Oracle数据库服务、MinIO文件存储服务已正常运行，且执行过数据库迁移
3. <span style="color:#e53e3e; font-weight:bold">Flutter 日志管理</span>：生产环境日志自动写入`backend/logs/`目录，需定期清理，避免磁盘占满
4. <span style="color:#e53e3e; font-weight:bold">Flutter 环境配置</span>：移动端开发需提前配置Android/iOS开发环境（参考<a href="https://docs.flutter.dev/" target="_blank">Flutter官方文档</a>）
5. <span style="color:#e53e3e; font-weight:bold">离线数据同步</span>：APP端离线练习数据同步时，需保证前端字段与后端接口返回字段完全一致，避免数据解析异常
6. <span style="color:#e53e3e; font-weight:bold">生产环境监控</span>：已集成 Sentry 监控，需配置SENTRY_DSN，实时监控服务异常
<div align="center">
  <hr style="width: 50%; margin: 20px auto; border: 1px solid #eee;">
  <p>© 2025 Effective Brushing | 高效刷题APP · 专注提升刷题效率</p>
</div>