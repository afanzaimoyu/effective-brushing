# Effective Brushing API 设计文档

> 版本: V1.1
> 更新时间: 2026-01-01
> 语言: 中文 (Chinese)

本文档详细定义了 **Effective Brushing** 项目的 API 接口，包括 **后端 REST API** 和 **前端本地 API**（支持离线优先架构）。

---

## 🟢 第一部分：后端 API (Backend REST API)

### 1. 概述 (Overview)

*   **Base URL**: `https://api.effective-brushing.com/api/v1` (生产环境示例)
*   **协议**: HTTPS
*   **数据格式**: JSON
*   **鉴权方式**: HTTP Header `Authorization: Bearer <token>`

#### 1.1 通用响应格式 (Common Response)

所有接口（除部分文件下载外）均返回以下标准结构：

```json
{
  "code": 0,          // 0: 成功, 非0: 错误码
  "message": "success", // 提示信息
  "data": { ... }     // 业务数据
}
```

#### 1.2 常用错误码 (Error Codes)

| Code | Message | 说明 |
| :--- | :--- | :--- |
| 40101 | Unauthorized | Token 无效或过期 |
| 40001 | Invalid Parameter | 参数校验失败 |
| 50000 | Internal Server Error | 服务器内部错误 |

---

### 2. 鉴权模块 (Authentication)

#### 2.1 微信登录 / 注册
*   **POST** `/auth/login`
*   **描述**: 使用微信小程序/App 的 Code 换取 JWT Token。如果用户不存在，则自动注册。
*   **请求参数**:
    ```json
    {
      "code": "06123abc...",  // 微信授权临时票据
      "platform": "wechat_mini" // 平台标识: wechat_mini, android, ios
    }
    ```
*   **响应**:
    ```json
    {
      "token": "eyJhbGciOi...",  // JWT Access Token
      "expires_in": 7200,        // 过期时间(秒)
      "is_new_user": false       // 是否新注册用户
    }
    ```

#### 2.2 获取当前用户信息
*   **GET** `/auth/me`
*   **响应**:
    ```json
    {
      "user_id": "u_123456",
      "nickname": "StudentA",
      "avatar_url": "https://..."
    }
    ```

---

### 3. 题库管理 (Question Banks)

#### 3.1 上传题库
*   **POST** `/banks`
*   **Content-Type**: `multipart/form-data`
*   **描述**: 上传题库文件（txt/excel）。
*   **参数**:
    *   `file`: 文件流 (Required, Max 20MB)
    *   `name`: 题库名称 (Optional, 默认文件名)
*   **响应**:
    ```json
    {
      "bank_id": "b_987654",
      "name": "2025考研政治",
      "question_count": 1000,
      "import_status": "processing" // 异步处理中，后续通过轮询或推送更新
    }
    ```

#### 3.2 获取题库列表
*   **GET** `/banks`
*   **参数**:
    *   `page`: 页码 (Default: 1)
    *   `page_size`: 每页数量 (Default: 20)
    *   `keyword`: 搜索关键词 (Optional)
*   **响应**:
    ```json
    {
      "list": [
        {
          "bank_id": "b_987654",
          "name": "2025考研政治",
          "question_count": 1000,
          "created_at": "2025-12-26T10:00:00Z"
        }
      ],
      "total": 1
    }
    ```

#### 3.3 删除题库
*   **DELETE** `/banks/{bank_id}`
*   **描述**: 逻辑删除题库，同时删除关联的云端答题记录（需慎重）。

#### 3.4 获取题库题目（用于下载/同步）
*   **GET** `/banks/{bank_id}/questions`
*   **描述**: 获取该题库下的所有题目数据，用于客户端本地缓存。
*   **响应**:
    ```json
    {
       "bank_id": "b_987654",
       "questions": [
          {
             "id": "q_1001",
             "type": "single", // single, multiple, true_false
             "stem": "题目内容...",
             "options": ["A. 选项1", "B. 选项2"],
             "answer": "A",
             "analysis": "解析内容...",
             "md5": "a1b2..."
          }
       ]
    }
    ```

---

### 3.A 单题管理 (Single Question Management)
> 补充需求：支持手动录入与编辑

#### 3.A.1 新增单题
*   **POST** `/banks/{bank_id}/questions`
*   **参数**:
    ```json
    {
      "type": "single",
      "stem": "题目内容...",
      "options": ["A", "B"],
      "answer": "A",
      "analysis": "解析..."
    }
    ```
*   **响应**: `{"id": "q_new_01", ...}`

#### 3.A.2 编辑题目
*   **PUT** `/questions/{question_id}`
*   **参数**: 同新增

#### 3.A.3 删除题目
*   **DELETE** `/questions/{question_id}`

#### 3.A.4 公共题库占位 (Future)
> **Note**: 当前版本仅支持私有题库。以下为预留接口设计思路，暂不实现。
> 未来实现逻辑：
> 1. `t_question_bank` 表增加 `is_public` (0/1) 和 `price` (积分/金额) 字段。
> 2. `GET /banks/market` 接口用于获取公开市场题库。
> 3. 用户下载公开题库时，后端创建一份副本（Copy-on-Write）或建立引用映射。
> *   `POST /banks/{bank_id}/publish` (Future): 发布题库到市场
> *   `POST /banks/market/{bank_id}/fork` (Future): 转存/购买题库到我的列表

---

### 4. 练习与同步 (Practice & Sync)

#### 4.1 随机抽题 (服务端辅助)
*   **POST** `/banks/{bank_id}/random`
*   **描述**: 在服务端进行随机抽题（主要用于在线模式或轻量级客户端）。离线优先模式下，推荐使用前端本地随机算法。
*   **参数**:
    ```json
    {
      "count": 20,
      "filters": { "type": ["single"] }
    }
    ```

#### 4.2 同步答题记录
*   **POST** `/answers/sync`
*   **描述**: 核心同步接口。客户端需上传本地增量的答题记录。
*   **请求参数**:
    ```json
    {
      "records": [
        {
          "local_id": "loc_123",      // 客户端本地ID (用于去重/映射)
          "bank_id": "b_987654",
          "question_id": "q_1001",
          "answer": "A",
          "is_correct": true,
          "duration_ms": 5000,        // 答题耗时
          "answered_at": "2025-12-26T10:05:00Z"
        }
      ]
    }
    ```
*   **响应**:
    ```json
    {
      "success_ids": ["loc_123"], // 成功同步的本地ID列表
      "failed_ids": [],           // 失败列表
      "server_timestamp": 1735200000
    }
    ```

#### 4.3 获取答题统计
*   **GET** `/answers/stats`
*   **参数**: `bank_id` (Optional)
*   **响应**:
    ```json
    {
      "total_answered": 500,
      "correct_rate": 0.85,
      "wrong_count": 75
    }
    ```

---

### 5. 错题本 (Wrong Questions)

#### 5.1 获取错题列表
*   **GET** `/wrong-questions`
*   **参数**:
    *   `bank_id`: 题库ID
    *   `page`: 页码
*   **响应**:
    ```json
    {
      "list": [
        {
          "question_id": "q_1001",
          "wrong_count": 3,
          "last_wrong_at": "..."
        }
      ]
    }
    ```

#### 5.2 移除错题 (标记为已掌握)
*   **DELETE** `/wrong-questions/{question_id}`

---

### 5.A 收藏夹 (Favorites) [P1]

#### 5.A.1 添加/取消收藏
*   **POST** `/favorites/{question_id}`
*   **描述**: 收藏题目（幂等接口）

*   **DELETE** `/favorites/{question_id}`
*   **描述**: 取消收藏

#### 5.A.2 获取收藏列表
*   **GET** `/favorites`
*   **参数**: `page`, `page_size`
*   **响应**: 题目列表结构

### 5.B 模拟考试 (Mock Exams) [P1]

#### 5.B.1 创建考试
*   **POST** `/exams`
*   **参数**:
    ```json
    {
      "name": "考前模拟01",
      "duration_minutes": 60,
      "question_count": 50,
      "source_bank_ids": ["b_001"] // 从指定题库抽题
    }
    ```
*   **响应**:
    ```json
    {
      "exam_id": "e_1001",
      "questions": [...] // 试题快照
    }
    ```

#### 5.B.2 提交试卷
*   **POST** `/exams/{exam_id}/submit`
*   **参数**:
    ```json
    {
       "answers": [{"question_id": "...", "answer": "..."}]
    }
    ```
*   **响应**:
    ```json
    {
      "score": 85,
      "correct_count": 42,
      "wrong_list": ["q_01", "q_05"]
    }
    ```

#### 5.B.3 获取考试记录
*   **GET** `/exams/history`
*   **响应**: 考试历史列表

---

### 6. 统计分析 (Statistics) [P1]

> 用于支持“数据复盘”页面的图表展示 (V1.1)。

#### 6.1 获取刷题趋势
*   **GET** `/stats/trend`
*   **参数**:
    *   `start_date`: 开始日期 (yyyy-MM-dd)
    *   `end_date`: 结束日期
*   **响应**:
    ```json
    {
      "trend": [
        {
          "date": "2025-12-20",
          "total_count": 50,
          "correct_count": 40
        },
        {
          "date": "2025-12-21",
          "total_count": 0,
          "correct_count": 0
        }
      ]
    }
    ```

#### 6.2 获取维度分析 (雷达图/饼图)
*   **GET** `/stats/analysis`
*   **参数**:
    *   `dimension`: 统计维度 (type=按题型, tag=按知识点)
*   **响应**:
    ```json
    {
      "analysis": [
        {
          "key": "single",
          "label": "单选题",
          "total": 100,
          "correct": 80
        },
        {
          "key": "multiple",
          "label": "多选题",
          "total": 50,
          "correct": 30
        }
      ]
    }
    ```

---
---

## 🔵 第二部分：前端本地 API (Frontend Local API)

> **设计说明**: 本项目采用 **Offline First (离线优先)** 策略。前端 UI 层 **不直接调用** 后端 REST API，而是通过 **Repository 层** 与 **Local Database (SQLite)** 交互。网络请求由后台 `SyncService` 异步托管。

### 1. 架构分层 (Architecture)

1.  **UI Layer**: 页面组件 (Pages / Widgets)。
2.  **Service/Repository Layer**: 业务逻辑与数据访问门面。
3.  **Data Source**:
    *   **Local DB**: SQLite (主要数据源)
    *   **Remote API**: 通过 HTTP Client 访问 (仅用于同步/下载)

### 2. 核心 Service 接口定义 (TypeScript/Dart 伪代码)

#### 2.1 AuthService (用户服务)

负责管理用户登录状态及 Token 持久化。

```typescript
interface AuthService {
  // 1. 微信登录并初始化本地用户数据
  // 流程：调用微信 SDK 获取 code -> 调用后端 login API -> 保存 Token -> 初始化本地 DB
  loginWithWeChat(): Promise<User>;

  // 2. 获取当前缓存的用户信息
  getCurrentUser(): User | null;

  // 3. 登出
  logout(): void;
}
```

#### 2.2 QuestionRepository (题库仓储)

UI 层核心依赖，封装了本地查询逻辑。

```typescript
interface QuestionRepository {
  // 1. 获取题库列表
  // 逻辑：优先读本地 LocalBank 表，同时静默请求后端 API 更新元数据
  // 返回：LocalBank 对象包含 downloadStatus (未下载/下载中/已完成)
  getBanks(): Promise<List<LocalBank>>;

  // 2. 下载题库
  // 逻辑：调用后端 /questions 接口 -> 批量插入本地 SQLite -> 更新 LocalBank 状态
  downloadBank(bankId: string, onProgress: (percent) => void): Promise<void>;

  // 3. 随机抽题 (核心刷题接口)
  // 逻辑：直接查询本地 SQLite，基于 Random 算法，高性能
  // 参数：filter (全部/错题/未做)
  getQuestions(bankId: string, count: number, filter: QuestionFilter): Promise<List<Question>>;

  // 4. 提交答案
  // 逻辑：
  //    a. 写入本地 AnswerRecord 表
  //    b. 写入 SyncQueue 表 (标记为 'pending')
  //    c. 触发 SyncService.startSync() (非阻塞)
  saveAnswer(record: AnswerRecord): Promise<void>;
}
```

#### 2.3 SyncService (同步服务)

后台运行的同步引擎，负责保持本地与云端一致。

```typescript
interface SyncService {
  // 1. 触发同步
  // 触发时机：APP启动 / 网络恢复 / 用户手动点击 / saveAnswer 后
  // 流程：
  //    a. 读取 SyncQueue 中 'pending' 的记录
  //    b. 聚合后 POST /answers/sync
  //    c. 成功后删除/更新 SyncQueue 记录
  //    d. (可选) 拉取云端新产生的错题 (多端同步场景)
  startSync(): Promise<SyncResult>;
}

#### 2.4 StatsRepository (统计仓储) [P1]

负责聚合本地数据以支持图表显示。

```typescript
interface StatsRepository {
  // 1. 获取每日做题趋势
  // 逻辑：SQL Group By date(timestamp)
  getDailyTrend(days: number): Promise<List<TrendPoint>>;

  // 2. 获取题型正确率分布
  // 逻辑：SQL Group By questionType from joined tables
  getTypeAnalysis(): Promise<List<TypeStats>>;
}
```

### 3. 本地数据模型 (Local Data Models)

#### 3.1 LocalBank
```typescript
{
  id: string;
  name: string;
  totalQuestions: number;
  downloadStatus: 'none' | 'downloading' | 'downloaded';
  lastSyncTime: number; // 上次同步时间
}
```

#### 3.2 AnswerRecord (本地存储)
```typescript
{
  uuid: string;       // 本地生成的唯一ID (UUID v4)
  questionId: string;
  userAnswer: string;
  isCorrect: boolean;
  timestamp: number;
  syncStatus: 'pending' | 'synced' | 'failed'; // 同步状态标记
}
```