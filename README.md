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

---

## 🛠 核心技术栈（附官方文档）
| 模块       | 技术选型                                                                | 官方文档链接                                                                                                                                       |
|------------|---------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| 后端核心   | Python 3.10+ + <a href="https://fastapi.org.cn/" target="_blank">FastAPI</a> | <a href="https://docs.python.org/zh-cn/3/" target="_blank">Python 3.10文档</a>、<a href="https://fastapi.org.cn/" target="_blank">FastAPI文档</a> |
| 依赖管理   | <a href="https://python-poetry.org" target="_blank">Poetry</a>      | <a href="https://python-poetry.org/docs/" target="_blank">Poetry官方文档</a>                                                                     |
| 数据库     | <a href="https://www.oracle.com/technetwork/cn/database/database-technologies/sql/documentation/index.html" target="_blank">Oracle 12c+</a> | <a href="https://www.oracle.com/technetwork/cn/database/database-technologies/sql/documentation/index.html" target="_blank">Oracle 12c文档</a> |
| 文件存储   | <a href="https://min-io.cn/product/overview" target="_blank">MinIO</a> | <a href="https://min-io.cn/docs/minio/kubernetes/upstream/" target="_blank">MinIO Python SDK文档</a>                                           |
| 移动端前端 | <a href="https://flutter.dev/" target="_blank">Flutter 3.16+</a>    | <a href="https://docs.flutter.dev/" target="_blank">Flutter官方文档</a>                                                                          |
| Web管理端  | <a href="https://vuejs.org" target="_blank">Vue 3</a>| <a href="https://vuejs.org/guide/introduction.html" target="_blank">Vue 3文档</a>、<a href="https://react.dev/" target="_blank">React 18文档</a>  |
| 辅助能力   | OCR（百度API）、AI解析（讯飞星火API）| <a href="#" target="_blank">百度OCR文档</a>、<a href="#" target="_blank">讯飞星火API文档</a>                                                            |

---

## 📂 项目目录结构
```markdown
effective-brushing/  # 项目根目录
├── backend/          # Python后端（Poetry管理）
│   ├── src/          # 核心代码（Poetry推荐src布局）
│   │   ├── brushing/ # 业务包（API/配置/模型/工具）
│   │   └── main.py   # FastAPI入口文件
│   ├── tests/        # 单元测试/接口测试
│   ├── pyproject.toml # Poetry依赖配置
│   ├── poetry.lock   # 依赖锁定文件
│   └── .env          # 敏感配置（Oracle/MinIO密钥）
├── frontend/         # 前端代码（前后端分离）
│   ├── mobile/       # Flutter移动端APP
│   │   ├── lib/      # Flutter核心代码
│   │   └── assets/   # 静态资源（图片/字体）
│   └── web/          # 可选：Vue/React管理后台
│       ├── src/      # Web核心代码
│       └── public/   # Web静态资源
├── docs/             # 开发文档
│   ├── prd/          # 产品需求文档
│   ├── tdd/          # 技术设计文档
│   ├── db_design/    # Oracle数据库设计
│   └── charts/       # 架构图/ER图/流程图
├── .gitignore        # Git忽略规则
└── README.md         # 项目总览文档
```

---


## ⚡ 快速启动指南（关键步骤高亮）
### 1. 后端启动（Poetry环境，核心步骤）

#### 进入后端目录（替换为你的实际路径）
```shell
cd D:\MyProject\effective-brushing\backend
```
#### ① 安装Poetry（首次使用，<span style="color:#e53e3e; font-weight:bold">必执行</span>）
```shell

```

#### ② 安装项目依赖（自动创建<span style="color:#4299e1; font-weight:bold">.venv虚拟环境</span>）
```shell
poetry install
```

#### ③ 启动后端服务（两种方式，推荐方式1）
- 方式1：使用Poetry自定义脚本（简化启动）
```python
poetry run start
```

- 方式2：直接运行uvicorn（灵活配置）
```python
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### ✅ 验证启动：访问 http://localhost:8000/health ，返回 {"status":"ok"} 即成功

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
### 1. 后端规范（Poetry+FastAPI）
- <span style="color:#4299e1; font-weight:bold">依赖管理</span>：仅通过`pyproject.toml`添加依赖，执行`poetry add 依赖名`，禁止手动修改`poetry.lock`
- <span style="color:#4299e1; font-weight:bold">代码风格</span>：使用`black`格式化代码（命令：`poetry run black src/`），保证代码格式统一
- <span style="color:#4299e1; font-weight:bold">测试要求</span>：新增接口必须补充单元测试，测试文件放在`backend/tests/`目录，代码覆盖率≥80%
- <span style="color:#4299e1; font-weight:bold">配置规范</span>：敏感信息（Oracle/MinIO密钥）必须写在`backend/.env`文件，禁止硬编码到代码中

### 2. 前端规范（Flutter/Vue）
- **Flutter 规范**：遵循 Dart 官方编码规范，组件按「页面组件/通用组件/业务组件」拆分，文件命名统一为`xxx_widget.dart`
- **Vue/React 规范**：遵循 ESLint 代码规范，提交代码前必须执行`npm run lint`修复格式问题，组件采用按需引入方式

## ⚠ 重要注意事项（核心提醒）
1. <span style="color:#e53e3e; font-weight:bold">敏感配置保护</span>：`backend/.env`文件包含Oracle/MinIO密钥等敏感信息，切勿提交到Git（已加入.gitignore，需确认配置生效）
2. <span style="color:#e53e3e; font-weight:bold">环境前置要求</span>：启动后端服务前，需确保Oracle数据库服务、MinIO文件存储服务已正常运行
3. <span style="color:#e53e3e; font-weight:bold">Flutter 环境配置</span>：移动端开发需提前配置Android/iOS开发环境（参考<a href="https://docs.flutter.dev/" target="_blank">Flutter官方文档</a>）
4. <span style="color:#e53e3e; font-weight:bold">离线数据同步</span>：APP端离线练习数据同步时，需保证前端字段与后端接口返回字段完全一致，避免数据解析异常

<div align="center">
  <hr style="width: 50%; margin: 20px auto; border: 1px solid #eee;">
  <p>© 2025 Effective Brushing | 高效刷题APP · 专注提升刷题效率</p>
</div>