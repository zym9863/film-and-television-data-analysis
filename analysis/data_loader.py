"""
数据加载与预处理模块
"""

import json
import ast
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


class DataLoader:
    """TMDB电影数据加载器"""
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = Path(data_dir)
        self._movies_df: Optional[pd.DataFrame] = None
        self._credits_df: Optional[pd.DataFrame] = None
        self._merged_df: Optional[pd.DataFrame] = None
    
    def load_movies(self) -> pd.DataFrame:
        """加载电影数据"""
        if self._movies_df is None:
            movies_path = self.data_dir / "tmdb_5000_movies.csv"
            self._movies_df = pd.read_csv(movies_path)
            self._preprocess_movies()
        return self._movies_df
    
    def load_credits(self) -> pd.DataFrame:
        """加载演职人员数据"""
        if self._credits_df is None:
            credits_path = self.data_dir / "tmdb_5000_credits.csv"
            self._credits_df = pd.read_csv(credits_path)
            self._preprocess_credits()
        return self._credits_df
    
    def load_merged(self) -> pd.DataFrame:
        """加载合并后的完整数据"""
        if self._merged_df is None:
            movies = self.load_movies()
            credits = self.load_credits()
            self._merged_df = movies.merge(
                credits[['movie_id', 'cast', 'crew', 'director', 'top_actors']],
                left_on='id',
                right_on='movie_id',
                how='left'
            )
            self._merged_df.drop('movie_id', axis=1, inplace=True)
        return self._merged_df
    
    def _preprocess_movies(self):
        """预处理电影数据"""
        df = self._movies_df
        
        # 解析JSON字段
        json_columns = ['genres', 'keywords', 'production_companies', 
                       'production_countries', 'spoken_languages']
        for col in json_columns:
            df[col] = df[col].apply(self._safe_parse_json)
        
        # 提取类型名称列表
        df['genre_names'] = df['genres'].apply(
            lambda x: [g['name'] for g in x] if isinstance(x, list) else []
        )
        
        # 提取制作公司名称
        df['company_names'] = df['production_companies'].apply(
            lambda x: [c['name'] for c in x] if isinstance(x, list) else []
        )
        
        # 提取主要制作公司
        df['main_company'] = df['company_names'].apply(
            lambda x: x[0] if x else None
        )
        
        # 处理日期
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        df['release_year'] = df['release_date'].dt.year
        df['release_month'] = df['release_date'].dt.month
        
        # 计算ROI (投资回报率)
        df['roi'] = np.where(
            df['budget'] > 0,
            (df['revenue'] - df['budget']) / df['budget'] * 100,
            np.nan
        )
        
        # 标记有效财务数据
        df['has_financial_data'] = (df['budget'] > 0) & (df['revenue'] > 0)
        
        # 提取关键词
        df['keyword_names'] = df['keywords'].apply(
            lambda x: [k['name'] for k in x] if isinstance(x, list) else []
        )
    
    def _preprocess_credits(self):
        """预处理演职人员数据"""
        df = self._credits_df
        
        # 解析JSON字段
        df['cast'] = df['cast'].apply(self._safe_parse_json)
        df['crew'] = df['crew'].apply(self._safe_parse_json)
        
        # 提取导演
        df['director'] = df['crew'].apply(self._extract_director)
        
        # 提取前3位主演
        df['top_actors'] = df['cast'].apply(
            lambda x: [a['name'] for a in x[:3]] if isinstance(x, list) else []
        )
    
    @staticmethod
    def _safe_parse_json(x):
        """安全解析JSON字符串"""
        if pd.isna(x):
            return []
        if isinstance(x, list):
            return x
        try:
            return json.loads(x.replace("'", '"'))
        except (json.JSONDecodeError, AttributeError):
            try:
                return ast.literal_eval(x)
            except (ValueError, SyntaxError):
                return []
    
    @staticmethod
    def _extract_director(crew_list):
        """从剧组列表中提取导演"""
        if not isinstance(crew_list, list):
            return None
        for member in crew_list:
            if member.get('job') == 'Director':
                return member.get('name')
        return None
    
    def get_valid_financial_data(self) -> pd.DataFrame:
        """获取有效财务数据（budget和revenue都大于0）"""
        df = self.load_merged()
        return df[df['has_financial_data']].copy()
    
    def get_summary_stats(self) -> dict:
        """获取数据集摘要统计"""
        df = self.load_movies()
        valid_df = df[df['has_financial_data']]
        
        return {
            'total_movies': len(df),
            'movies_with_financial_data': len(valid_df),
            'year_range': {
                'min': int(df['release_year'].min()) if pd.notna(df['release_year'].min()) else None,
                'max': int(df['release_year'].max()) if pd.notna(df['release_year'].max()) else None
            },
            'budget': {
                'mean': float(valid_df['budget'].mean()),
                'median': float(valid_df['budget'].median()),
                'min': float(valid_df['budget'].min()),
                'max': float(valid_df['budget'].max())
            },
            'revenue': {
                'mean': float(valid_df['revenue'].mean()),
                'median': float(valid_df['revenue'].median()),
                'min': float(valid_df['revenue'].min()),
                'max': float(valid_df['revenue'].max())
            },
            'vote_average': {
                'mean': float(df['vote_average'].mean()),
                'median': float(df['vote_average'].median())
            }
        }
