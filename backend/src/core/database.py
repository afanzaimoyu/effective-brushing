# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2025/12/26 14:26
# @File    : database.py
# @Project : effective-brushing
# @Author  : FLZ
# @Desc    : 异步oracle数据连接
# @Version : 0.01
# --------------------------------------
"""
异步数据库操作工具（适配 MySQL 8.0+ + SQLAlchemy 2.0+）
封装通用 CRUD 操作、事务管理、连接池管理，提供统一异常处理和日志


# 1. 简单查询（自动管理连接）
async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    query = select(User).where(User.id == user_id)
    return await fetch_one(query)

# 2. 事务操作（批量插入）
async def batch_create_questions(questions: List[Dict[str, Any]]) -> None:
    async with transaction() as conn:
        for q in questions:
            insert_query = insert(Question).values(**q)
            await execute(insert_query, conn)  # 事务内不立即提交

# 3. 插入并返回主键（Oracle RETURNING）
async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    insert_query = insert(User).values(**user_data).returning(User.id, User.name)
    return await execute_insert_returning(insert_query)

# 4. FastAPI接口调用（依赖注入）
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection

@app.get("/users/{user_id}")
async def get_user_api(
    user_id: int,
    conn: AsyncConnection = Depends(get_db_connection)
) -> Dict[str, Any]:
    user = await fetch_one(select(User).where(User.id == user_id), conn)
    if not user:
        raise NotFound(resource_type="用户")
    return user
"""
import logging
from typing import Any, AsyncGenerator, Dict, List, Optional, TypeVar, Union, overload
from contextlib import asynccontextmanager

from sqlalchemy import (
    Delete,
    Insert,
    MetaData,
    Select,
    Update,
    exc as sa_exc,
)
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.engine import CursorResult, Row
from sqlalchemy.sql import Executable

# 修正导入路径（适配项目结构）
from src.core.config import settings
from src.core.exceptions import (
    DatabaseError,
    ResourceNotFound,
    ServiceUnavailable,
)

# 补充缺失的命名规范常量（若src.constants不存在，直接定义）
DB_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# 类型别名（简化注解）
QueryType = Union[Select, Insert, Update, Delete]
T = TypeVar("T")

# 日志配置
logger = logging.getLogger(__name__)

# ===================== 核心配置：引擎/元数据/会话工厂 =====================
# Oracle 异步引擎配置（适配 Oracle 特有的连接参数）
# MySQL 异步引擎配置
engine: AsyncEngine = create_async_engine(
    url=str(settings.DATABASE_ASYNC_URL),
    # 连接池配置（生产级优化）
    pool_size=getattr(settings, "DATABASE_POOL_SIZE", 10),
    max_overflow=getattr(settings, "DATABASE_MAX_OVERFLOW", 20),
    pool_recycle=getattr(settings, "DATABASE_POOL_TTL", 3600),
    pool_pre_ping=getattr(settings, "DATABASE_POOL_PRE_PING", True),
    pool_timeout=30,
    # 开发环境打印SQL
    echo=settings.ENVIRONMENT.is_local,
)

# 元数据（统一命名规范）
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

# 会话工厂（可选：若使用 ORM Session）
AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,  # 避免commit后对象过期
)


# ===================== 私有工具函数（内部使用） =====================
async def _safe_execute(
        connection: AsyncConnection,
        query: Executable,
        commit: bool = False,
) -> CursorResult:
    """
    安全执行SQL查询，捕获并封装数据库异常
    :param connection: 异步连接对象
    :param query: SQLAlchemy 查询对象
    :param commit: 是否执行commit
    :return: 执行结果游标
    :raises DatabaseError: 数据库执行异常
    """
    try:
        # 开发环境打印SQL（便于调试）
        if settings.ENVIRONMENT.is_local:
            logger.debug(f"执行SQL: {query}")

        result = await connection.execute(query)

        if commit:
            await connection.commit()
            logger.debug(f"SQL执行并提交成功: {query}")

        return result

    except sa_exc.OperationalError as e:
        # 连接失败/网络异常（服务不可用）
        logger.error(f"数据库连接异常: {str(e)} | SQL: {query}", exc_info=True)
        raise ServiceUnavailable(detail="数据库连接失败，请稍后重试") from e
    except sa_exc.IntegrityError as e:
        # 主键冲突/外键约束等（业务异常）
        logger.error(f"数据库完整性异常: {str(e)} | SQL: {query}", exc_info=True)
        raise DatabaseError(detail="数据校验失败，违反数据库约束") from e
    except sa_exc.SQLAlchemyError as e:
        # 其他SQL异常（通用数据库错误）
        logger.error(f"数据库执行异常: {str(e)} | SQL: {query}", exc_info=True)
        raise DatabaseError(detail="数据库操作失败") from e
    except Exception as e:
        # 未知异常
        logger.critical(f"数据库未知异常: {str(e)} | SQL: {query}", exc_info=True)
        raise DatabaseError(detail="服务器内部数据库错误") from e


def _row_to_dict(row: Row) -> Dict[str, Any]:
    """
    将SQLAlchemy Row对象转换为字典（兼容不同版本）
    :param row: 查询结果行对象
    :return: 字典格式的行数据
    """
    try:
        # SQLAlchemy 2.0+ 原生支持 _asdict()
        return row._asdict()
    except AttributeError:
        # 兼容旧版本
        return dict(row)


# ===================== 通用查询/执行函数（基础CRUD） =====================
@overload
async def fetch_one(
        query: Select,
        connection: Optional[AsyncConnection] = None,
        commit_after: bool = False,
) -> Optional[Dict[str, Any]]: ...


@overload
async def fetch_one(
        query: Union[Insert, Update],
        connection: Optional[AsyncConnection] = None,
        commit_after: bool = False,
) -> Optional[Dict[str, Any]]: ...


async def fetch_one(
        query: QueryType,
        connection: Optional[AsyncConnection] = None,
        commit_after: bool = False,
) -> Optional[Dict[str, Any]]:
    """
    执行查询并返回第一条结果（无结果返回None）
    修复原版本rowcount不准确的问题（Select语句rowcount=-1）

    :param query: SQLAlchemy查询对象（Select/Insert/Update）
    :param connection: 外部连接（用于事务），None则自动创建连接
    :param commit_after: 是否执行commit（仅Insert/Update有效）
    :return: 第一条结果的字典，无结果返回None
    """
    use_external_conn = connection is not None
    conn = connection if use_external_conn else await engine.connect()

    try:
        result = await _safe_execute(conn, query, commit_after)
        row = result.first()
        return _row_to_dict(row) if row is not None else None
    finally:
        # 仅关闭自动创建的连接，外部连接由调用方管理
        if not use_external_conn:
            await conn.close()


@overload
async def fetch_all(
        query: Select,
        connection: Optional[AsyncConnection] = None,
        commit_after: bool = False,
) -> List[Dict[str, Any]]: ...


@overload
async def fetch_all(
        query: Union[Insert, Update],
        connection: Optional[AsyncConnection] = None,
        commit_after: bool = False,
) -> List[Dict[str, Any]]: ...


async def fetch_all(
        query: QueryType,
        connection: Optional[AsyncConnection] = None,
        commit_after: bool = False,
) -> List[Dict[str, Any]]:
    """
    执行查询并返回所有结果（无结果返回空列表）

    :param query: SQLAlchemy查询对象
    :param connection: 外部连接
    :param commit_after: 是否执行commit
    :return: 结果列表（字典格式）
    """
    use_external_conn = connection is not None
    conn = connection if use_external_conn else await engine.connect()

    try:
        result = await _safe_execute(conn, query, commit_after)
        rows = result.all()
        return [_row_to_dict(row) for row in rows] if rows else []
    finally:
        if not use_external_conn:
            await conn.close()


async def execute(
        query: Union[Insert, Update, Delete],
        connection: Optional[AsyncConnection] = None,
        commit_after: bool = False,
) -> CursorResult:
    """
    执行增/删/改操作（补充支持Delete语句）

    :param query: SQLAlchemy增/删/改对象
    :param connection: 外部连接
    :param commit_after: 是否执行commit
    :return: 执行结果游标
    """
    use_external_conn = connection is not None
    conn = connection if use_external_conn else await engine.connect()

    try:
        result = await _safe_execute(conn, query, commit_after)
        return result
    finally:
        if not use_external_conn:
            await conn.close()


async def execute_insert_returning(
        query: Insert,
        connection: Optional[AsyncConnection] = None,
        commit_after: bool = True,
) -> Optional[Dict[str, Any]]:
    """
    执行插入操作并返回新增记录
    适用于需要获取自增主键的场景

    :param query: 包含returning子句的Insert对象
    :param connection: 外部连接
    :param commit_after: 默认提交（插入操作通常需要立即提交）
    :return: 新增记录的字典（含主键）
    """
    return await fetch_one(query, connection, commit_after)


# ===================== 事务管理（核心增强） =====================
@asynccontextmanager
async def transaction() -> AsyncGenerator[AsyncConnection, None]:
    """
    异步事务上下文管理器（自动提交/回滚）
    使用方式：
    async with transaction() as conn:
        await execute(query1, conn)
        await execute(query2, conn)
    """
    conn = await engine.connect()
    trans = None

    try:
        trans = await conn.begin()  # 开启事务
        yield conn  # 传递连接给业务逻辑
        await trans.commit()  # 无异常则提交
        logger.debug("数据库事务提交成功")
    except Exception as e:
        if trans:
            await trans.rollback()  # 异常则回滚
            logger.error(f"数据库事务回滚: {str(e)}", exc_info=True)
        raise  # 重新抛出异常，让上层处理
    finally:
        await conn.close()  # 无论成败，关闭连接


# ===================== 连接池/引擎管理（生产级必备） =====================
async def check_database_connection() -> bool:
    """
    检查数据库连接是否可用（启动时健康检查）
    :return: 连接正常返回True，否则抛出异常
    """
    try:
        async with engine.connect() as conn:
            # MySQL 健康检查
            from sqlalchemy import text
            result = await conn.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as e:
        logger.critical(f"数据库连接检查失败: {str(e)}", exc_info=True)
        raise ServiceUnavailable(detail="数据库连接失败，服务无法启动") from e


async def close_database_engine() -> None:
    """
    关闭数据库引擎（应用退出时清理资源）
    """
    if engine:
        await engine.dispose()
        logger.info("数据库引擎已关闭，连接池释放完成")


# ===================== 依赖注入函数（供FastAPI使用） =====================
async def get_db_connection() -> AsyncGenerator[AsyncConnection, None]:
    """
    FastAPI依赖注入：获取数据库连接（自动关闭）
    使用方式：
    @app.get("/")
    async def get_data(conn: AsyncConnection = Depends(get_db_connection)):
        return await fetch_all(query, conn)
    """
    conn = await engine.connect()
    try:
        yield conn
    finally:
        await conn.close()


async def get_db_session() -> AsyncGenerator[AsyncSessionFactory, None]:
    """
    FastAPI依赖注入：获取ORM Session（若使用ORM）
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
# Oracle测试语句