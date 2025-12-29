"""
影视数据分析系统主入口
"""

import uvicorn


def main():
    """主函数 - 启动API服务"""
    print("=" * 50)
    print("TMDB 影视数据分析系统")
    print("=" * 50)
    print("\n正在启动API服务...")
    print("API文档: http://localhost:8000/docs")
    print("前端地址: http://localhost:5173")
    print("\n按 Ctrl+C 停止服务\n")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


def run_server():
    """服务器入口点"""
    main()


if __name__ == "__main__":
    main()
