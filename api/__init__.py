"""
FastAPI 服务模块
提供影视数据分析API接口
"""

from .app import app, run_server

__all__ = ["app", "run_server"]
