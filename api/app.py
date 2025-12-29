"""
FastAPI 应用主入口
提供RESTful API服务
"""

from contextlib import asynccontextmanager
from typing import Optional

import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from analysis import DataLoader, MovieAnalyzer, BoxOfficePredictor


# 全局实例
data_loader: Optional[DataLoader] = None
analyzer: Optional[MovieAnalyzer] = None
predictor: Optional[BoxOfficePredictor] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global data_loader, analyzer, predictor
    
    # 启动时加载数据
    print("正在加载数据...")
    data_loader = DataLoader()
    data_loader.load_merged()  # 预加载数据
    analyzer = MovieAnalyzer(data_loader)
    predictor = BoxOfficePredictor(data_loader)
    print("数据加载完成！")
    
    yield
    
    # 关闭时清理
    print("服务关闭")


# 创建应用
app = FastAPI(
    title="TMDB 影视数据分析 API",
    description="基于TMDB 5000电影数据集的分析API，提供ROI分析、票房预测、类型分析等功能",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Pydantic 模型 ====================

class PredictionRequest(BaseModel):
    """票房预测请求"""
    budget: float
    popularity: float = 10.0
    runtime: float = 120.0
    vote_average: float = 6.0
    vote_count: int = 100
    release_year: int = 2024
    release_month: int = 6
    genres: list[str] = []


class PredictionResponse(BaseModel):
    """票房预测响应"""
    predicted_revenue: float
    predicted_roi: float
    model_used: str


# ==================== API 路由 ====================

@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "TMDB 影视数据分析 API",
        "version": "1.0.0",
        "endpoints": {
            "overview": "/api/overview",
            "roi": "/api/roi",
            "genres": "/api/genres",
            "trends": "/api/trends",
            "directors": "/api/directors",
            "actors": "/api/actors",
            "companies": "/api/companies",
            "correlations": "/api/correlations",
            "prediction": "/api/prediction",
            "scatter": "/api/scatter"
        }
    }


@app.get("/api/overview")
async def get_overview():
    """获取数据集概览"""
    try:
        summary = data_loader.get_summary_stats()
        return {
            "success": True,
            "data": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/roi")
async def get_roi_analysis():
    """获取ROI分析结果"""
    try:
        roi_data = analyzer.analyze_roi()
        roi_by_genre = analyzer.analyze_roi_by_genre()
        roi_by_budget = analyzer.analyze_roi_by_budget_range()
        
        return {
            "success": True,
            "data": {
                "overview": roi_data,
                "by_genre": roi_by_genre,
                "by_budget_range": roi_by_budget
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/genres")
async def get_genre_analysis():
    """获取电影类型分析"""
    try:
        genre_data = analyzer.analyze_genres()
        return {
            "success": True,
            "data": genre_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/trends")
async def get_trends():
    """获取时间趋势分析"""
    try:
        yearly = analyzer.analyze_yearly_trends()
        monthly = analyzer.analyze_monthly_patterns()
        
        return {
            "success": True,
            "data": {
                "yearly": yearly,
                "monthly": monthly
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/directors")
async def get_directors(top_n: int = Query(default=20, ge=5, le=50)):
    """获取导演分析"""
    try:
        directors = analyzer.analyze_directors(top_n=top_n)
        return {
            "success": True,
            "data": directors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/actors")
async def get_actors(top_n: int = Query(default=20, ge=5, le=50)):
    """获取演员分析"""
    try:
        actors = analyzer.analyze_actors(top_n=top_n)
        return {
            "success": True,
            "data": actors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/companies")
async def get_companies(top_n: int = Query(default=20, ge=5, le=50)):
    """获取制作公司分析"""
    try:
        companies = analyzer.analyze_production_companies(top_n=top_n)
        return {
            "success": True,
            "data": companies
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/correlations")
async def get_correlations():
    """获取相关性分析"""
    try:
        correlations = analyzer.analyze_correlations()
        return {
            "success": True,
            "data": correlations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/scatter")
async def get_scatter_data(
    x: str = Query(default="budget", description="X轴变量"),
    y: str = Query(default="revenue", description="Y轴变量"),
    limit: int = Query(default=500, ge=50, le=2000)
):
    """获取散点图数据"""
    try:
        scatter = analyzer.get_scatter_data(x_var=x, y_var=y, limit=limit)
        return {
            "success": True,
            "data": scatter
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/prediction/train")
async def train_prediction_model():
    """训练票房预测模型"""
    try:
        results = predictor.train_models()
        return {
            "success": True,
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/prediction/insights")
async def get_prediction_insights():
    """获取预测模型洞察"""
    try:
        insights = predictor.get_prediction_insights()
        return {
            "success": True,
            "data": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/prediction/predict")
async def predict_box_office(request: PredictionRequest):
    """预测电影票房"""
    try:
        prediction = predictor.predict({
            'budget': request.budget,
            'popularity': request.popularity,
            'runtime': request.runtime,
            'vote_average': request.vote_average,
            'vote_count': request.vote_count,
            'release_year': request.release_year,
            'release_month': request.release_month,
            'genres': request.genres
        })
        
        return {
            "success": True,
            "data": prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """运行服务器"""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
