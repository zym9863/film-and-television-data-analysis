"""
电影数据分析模块
包含各类统计分析方法
"""

from collections import Counter
from typing import Optional

import numpy as np
import pandas as pd

from .data_loader import DataLoader


class MovieAnalyzer:
    """电影数据分析器"""
    
    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self._df: Optional[pd.DataFrame] = None
    
    @property
    def df(self) -> pd.DataFrame:
        """延迟加载数据"""
        if self._df is None:
            self._df = self.loader.load_merged()
        return self._df
    
    # ==================== ROI 分析 ====================
    
    def analyze_roi(self) -> dict:
        """ROI投资回报率综合分析"""
        valid_df = self.df[self.df['has_financial_data']].copy()
        
        # 基础统计
        roi_stats = {
            'mean': float(valid_df['roi'].mean()),
            'median': float(valid_df['roi'].median()),
            'std': float(valid_df['roi'].std()),
            'min': float(valid_df['roi'].min()),
            'max': float(valid_df['roi'].max()),
            'profitable_count': int((valid_df['roi'] > 0).sum()),
            'loss_count': int((valid_df['roi'] <= 0).sum()),
            'profitable_rate': float((valid_df['roi'] > 0).mean() * 100)
        }
        
        # ROI分布区间
        roi_bins = [-float('inf'), -50, 0, 100, 500, 1000, float('inf')]
        roi_labels = ['亏损>50%', '亏损0-50%', '盈利0-100%', '盈利100-500%', '盈利500-1000%', '盈利>1000%']
        valid_df['roi_category'] = pd.cut(valid_df['roi'], bins=roi_bins, labels=roi_labels)
        roi_distribution = valid_df['roi_category'].value_counts().to_dict()
        roi_distribution = {str(k): int(v) for k, v in roi_distribution.items()}
        
        # 高ROI电影Top10
        top_roi = valid_df.nlargest(10, 'roi')[
            ['title', 'budget', 'revenue', 'roi', 'release_year', 'genre_names']
        ].to_dict('records')
        
        # 低ROI电影Top10
        bottom_roi = valid_df.nsmallest(10, 'roi')[
            ['title', 'budget', 'revenue', 'roi', 'release_year', 'genre_names']
        ].to_dict('records')
        
        return {
            'statistics': roi_stats,
            'distribution': roi_distribution,
            'top_roi_movies': top_roi,
            'bottom_roi_movies': bottom_roi
        }
    
    def analyze_roi_by_genre(self) -> list:
        """按类型分析ROI"""
        valid_df = self.df[self.df['has_financial_data']].copy()
        
        # 展开类型
        genre_roi = []
        for _, row in valid_df.iterrows():
            for genre in row['genre_names']:
                genre_roi.append({
                    'genre': genre,
                    'roi': row['roi'],
                    'budget': row['budget'],
                    'revenue': row['revenue']
                })
        
        genre_df = pd.DataFrame(genre_roi)
        
        # 按类型聚合
        result = genre_df.groupby('genre').agg({
            'roi': ['mean', 'median', 'std', 'count'],
            'budget': 'mean',
            'revenue': 'mean'
        }).reset_index()
        
        result.columns = ['genre', 'mean_roi', 'median_roi', 'std_roi', 'count', 'avg_budget', 'avg_revenue']
        result = result.sort_values('mean_roi', ascending=False)
        
        return result.to_dict('records')
    
    def analyze_roi_by_budget_range(self) -> list:
        """按预算区间分析ROI"""
        valid_df = self.df[self.df['has_financial_data']].copy()
        
        # 定义预算区间（单位：百万美元）
        budget_bins = [0, 1e6, 10e6, 50e6, 100e6, 200e6, float('inf')]
        budget_labels = ['<1M', '1-10M', '10-50M', '50-100M', '100-200M', '>200M']
        
        valid_df['budget_range'] = pd.cut(valid_df['budget'], bins=budget_bins, labels=budget_labels)
        
        result = valid_df.groupby('budget_range', observed=True).agg({
            'roi': ['mean', 'median', 'count'],
            'revenue': 'mean'
        }).reset_index()
        
        result.columns = ['budget_range', 'mean_roi', 'median_roi', 'count', 'avg_revenue']
        
        return result.to_dict('records')
    
    # ==================== 类型分析 ====================
    
    def analyze_genres(self) -> dict:
        """电影类型综合分析"""
        df = self.df
        
        # 统计所有类型出现次数
        all_genres = []
        for genres in df['genre_names']:
            all_genres.extend(genres)
        genre_counts = Counter(all_genres)
        
        # 类型组合分析
        df['genre_combo'] = df['genre_names'].apply(lambda x: ', '.join(sorted(x)) if x else 'Unknown')
        combo_counts = df['genre_combo'].value_counts().head(20).to_dict()
        
        # 按类型统计票房和评分
        genre_stats = []
        valid_df = df[df['has_financial_data']]
        for genre in genre_counts.keys():
            genre_movies = valid_df[valid_df['genre_names'].apply(lambda x: genre in x)]
            if len(genre_movies) > 0:
                genre_stats.append({
                    'genre': genre,
                    'count': genre_counts[genre],
                    'avg_revenue': float(genre_movies['revenue'].mean()),
                    'total_revenue': float(genre_movies['revenue'].sum()),
                    'avg_budget': float(genre_movies['budget'].mean()),
                    'avg_rating': float(genre_movies['vote_average'].mean()),
                    'avg_roi': float(genre_movies['roi'].mean())
                })
        
        genre_stats = sorted(genre_stats, key=lambda x: x['count'], reverse=True)
        
        return {
            'genre_counts': dict(genre_counts.most_common()),
            'genre_combinations': combo_counts,
            'genre_statistics': genre_stats
        }
    
    # ==================== 时间趋势分析 ====================
    
    def analyze_yearly_trends(self) -> list:
        """年度趋势分析"""
        df = self.df[self.df['release_year'].notna()].copy()
        df['release_year'] = df['release_year'].astype(int)
        
        # 过滤有效年份范围
        df = df[(df['release_year'] >= 1980) & (df['release_year'] <= 2017)]
        
        # 分别处理全部数据和有财务数据的数据
        yearly_all = df.groupby('release_year').agg({
            'id': 'count',
            'vote_average': 'mean',
            'popularity': 'mean',
            'runtime': 'mean'
        }).reset_index()
        yearly_all.columns = ['year', 'movie_count', 'avg_rating', 'avg_popularity', 'avg_runtime']
        
        # 有财务数据的年度统计
        valid_df = df[df['has_financial_data']]
        yearly_financial = valid_df.groupby('release_year').agg({
            'budget': ['mean', 'sum'],
            'revenue': ['mean', 'sum'],
            'roi': 'mean'
        }).reset_index()
        yearly_financial.columns = ['year', 'avg_budget', 'total_budget', 'avg_revenue', 'total_revenue', 'avg_roi']
        
        # 合并
        result = yearly_all.merge(yearly_financial, on='year', how='left')
        result = result.fillna(0)
        
        return result.to_dict('records')
    
    def analyze_monthly_patterns(self) -> list:
        """月度发行规律分析"""
        df = self.df[self.df['release_month'].notna()].copy()
        valid_df = df[df['has_financial_data']]
        
        monthly = valid_df.groupby('release_month').agg({
            'id': 'count',
            'revenue': 'mean',
            'budget': 'mean',
            'roi': 'mean',
            'vote_average': 'mean'
        }).reset_index()
        
        monthly.columns = ['month', 'movie_count', 'avg_revenue', 'avg_budget', 'avg_roi', 'avg_rating']
        
        # 添加月份名称
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly['month_name'] = monthly['month'].apply(lambda x: month_names[int(x)-1])
        
        return monthly.to_dict('records')
    
    # ==================== 导演和演员分析 ====================
    
    def analyze_directors(self, top_n: int = 20) -> list:
        """导演分析"""
        df = self.df[self.df['director'].notna()].copy()
        valid_df = df[df['has_financial_data']]
        
        director_stats = valid_df.groupby('director').agg({
            'id': 'count',
            'revenue': ['sum', 'mean'],
            'budget': ['sum', 'mean'],
            'vote_average': 'mean',
            'roi': 'mean'
        }).reset_index()
        
        director_stats.columns = ['director', 'movie_count', 'total_revenue', 'avg_revenue',
                                  'total_budget', 'avg_budget', 'avg_rating', 'avg_roi']
        
        # 至少2部电影的导演
        director_stats = director_stats[director_stats['movie_count'] >= 2]
        director_stats = director_stats.nlargest(top_n, 'total_revenue')
        
        return director_stats.to_dict('records')
    
    def analyze_actors(self, top_n: int = 20) -> list:
        """演员分析"""
        valid_df = self.df[self.df['has_financial_data']].copy()
        
        # 展开演员
        actor_data = []
        for _, row in valid_df.iterrows():
            for actor in row.get('top_actors', []):
                actor_data.append({
                    'actor': actor,
                    'revenue': row['revenue'],
                    'budget': row['budget'],
                    'roi': row['roi'],
                    'vote_average': row['vote_average']
                })
        
        if not actor_data:
            return []
        
        actor_df = pd.DataFrame(actor_data)
        
        actor_stats = actor_df.groupby('actor').agg({
            'revenue': ['count', 'sum', 'mean'],
            'budget': ['sum', 'mean'],
            'vote_average': 'mean',
            'roi': 'mean'
        }).reset_index()
        
        actor_stats.columns = ['actor', 'movie_count', 'total_revenue', 'avg_revenue',
                               'total_budget', 'avg_budget', 'avg_rating', 'avg_roi']
        
        # 至少3部电影的演员
        actor_stats = actor_stats[actor_stats['movie_count'] >= 3]
        actor_stats = actor_stats.nlargest(top_n, 'total_revenue')
        
        return actor_stats.to_dict('records')
    
    # ==================== 制作公司分析 ====================
    
    def analyze_production_companies(self, top_n: int = 20) -> list:
        """制作公司分析"""
        valid_df = self.df[self.df['has_financial_data']].copy()
        
        # 展开公司
        company_data = []
        for _, row in valid_df.iterrows():
            for company in row.get('company_names', []):
                company_data.append({
                    'company': company,
                    'revenue': row['revenue'],
                    'budget': row['budget'],
                    'roi': row['roi'],
                    'vote_average': row['vote_average']
                })
        
        if not company_data:
            return []
        
        company_df = pd.DataFrame(company_data)
        
        company_stats = company_df.groupby('company').agg({
            'revenue': ['count', 'sum', 'mean'],
            'budget': ['sum', 'mean'],
            'vote_average': 'mean',
            'roi': 'mean'
        }).reset_index()
        
        company_stats.columns = ['company', 'movie_count', 'total_revenue', 'avg_revenue',
                                  'total_budget', 'avg_budget', 'avg_rating', 'avg_roi']
        
        # 至少5部电影的公司
        company_stats = company_stats[company_stats['movie_count'] >= 5]
        company_stats = company_stats.nlargest(top_n, 'total_revenue')
        
        return company_stats.to_dict('records')
    
    # ==================== 相关性分析 ====================
    
    def analyze_correlations(self) -> dict:
        """数值变量相关性分析"""
        valid_df = self.df[self.df['has_financial_data']].copy()
        
        # 选择数值列
        numeric_cols = ['budget', 'revenue', 'roi', 'runtime', 'popularity', 
                       'vote_average', 'vote_count', 'release_year']
        
        # 过滤有效列
        available_cols = [col for col in numeric_cols if col in valid_df.columns]
        
        # 计算相关矩阵
        corr_matrix = valid_df[available_cols].corr()
        
        # 转换为可序列化格式
        correlations = []
        for i, col1 in enumerate(corr_matrix.columns):
            for j, col2 in enumerate(corr_matrix.columns):
                if i < j:  # 只取上三角
                    correlations.append({
                        'var1': col1,
                        'var2': col2,
                        'correlation': float(corr_matrix.loc[col1, col2])
                    })
        
        # 排序返回
        correlations = sorted(correlations, key=lambda x: abs(x['correlation']), reverse=True)
        
        # 完整矩阵
        matrix = {col: {col2: float(corr_matrix.loc[col, col2]) 
                       for col2 in corr_matrix.columns} 
                 for col in corr_matrix.columns}
        
        return {
            'top_correlations': correlations[:10],
            'correlation_matrix': matrix,
            'variables': list(corr_matrix.columns)
        }
    
    # ==================== 散点图数据 ====================
    
    def get_scatter_data(self, x_var: str = 'budget', y_var: str = 'revenue', 
                         limit: int = 500) -> list:
        """获取散点图数据"""
        valid_df = self.df[self.df['has_financial_data']].copy()
        
        # 选择列
        columns = [x_var, y_var, 'title', 'release_year', 'genre_names', 'vote_average']
        available_cols = [col for col in columns if col in valid_df.columns]
        
        result = valid_df[available_cols].dropna(subset=[x_var, y_var])
        
        # 限制数量（按revenue排序取top）
        if len(result) > limit:
            result = result.nlargest(limit, y_var if y_var in result.columns else x_var)
        
        return result.to_dict('records')
