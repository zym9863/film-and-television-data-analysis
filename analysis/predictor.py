"""
票房预测模型模块
使用机器学习算法进行票房预测
"""

from typing import Optional, Tuple
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from .data_loader import DataLoader

warnings.filterwarnings('ignore')


class BoxOfficePredictor:
    """票房预测器"""
    
    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self._df: Optional[pd.DataFrame] = None
        self._models: dict = {}
        self._scaler: Optional[StandardScaler] = None
        self._mlb: Optional[MultiLabelBinarizer] = None
        self._feature_names: list = []
        self._is_trained: bool = False
        self._evaluation_results: dict = {}
    
    @property
    def df(self) -> pd.DataFrame:
        """延迟加载数据"""
        if self._df is None:
            self._df = self.loader.load_merged()
        return self._df
    
    def prepare_features(self) -> Tuple[pd.DataFrame, pd.Series]:
        """准备特征矩阵和目标变量"""
        df = self.df[self.df['has_financial_data']].copy()
        
        # 基础数值特征
        numeric_features = ['budget', 'popularity', 'runtime', 'vote_average', 
                           'vote_count', 'release_year', 'release_month']
        
        # 过滤可用特征
        available_numeric = [f for f in numeric_features if f in df.columns]
        
        # 移除缺失值
        df = df.dropna(subset=available_numeric + ['revenue'])
        
        # 创建特征DataFrame
        X = df[available_numeric].copy()
        
        # 添加派生特征
        X['budget_log'] = np.log1p(df['budget'])
        X['popularity_log'] = np.log1p(df['popularity'])
        X['vote_count_log'] = np.log1p(df['vote_count'])
        
        # 类型特征（One-Hot编码）
        if 'genre_names' in df.columns:
            self._mlb = MultiLabelBinarizer()
            genre_encoded = self._mlb.fit_transform(df['genre_names'])
            genre_df = pd.DataFrame(
                genre_encoded,
                columns=[f'genre_{g}' for g in self._mlb.classes_],
                index=df.index
            )
            X = pd.concat([X, genre_df], axis=1)
        
        # 类型数量
        X['genre_count'] = df['genre_names'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        
        # 目标变量
        y = df['revenue']
        
        self._feature_names = list(X.columns)
        
        return X, y
    
    def train_models(self, test_size: float = 0.2, random_state: int = 42) -> dict:
        """训练多个预测模型并比较"""
        X, y = self.prepare_features()
        
        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # 标准化
        self._scaler = StandardScaler()
        X_train_scaled = self._scaler.fit_transform(X_train)
        X_test_scaled = self._scaler.transform(X_test)
        
        # 对数变换目标变量（票房分布是偏态的）
        y_train_log = np.log1p(y_train)
        y_test_log = np.log1p(y_test)
        
        # 定义模型
        models = {
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(alpha=1.0),
            'Random Forest': RandomForestRegressor(
                n_estimators=100, max_depth=15, 
                min_samples_split=5, random_state=random_state, n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingRegressor(
                n_estimators=100, max_depth=5,
                learning_rate=0.1, random_state=random_state
            )
        }
        
        results = {}
        
        for name, model in models.items():
            # 训练
            model.fit(X_train_scaled, y_train_log)
            
            # 预测
            y_pred_log = model.predict(X_test_scaled)
            y_pred = np.expm1(y_pred_log)  # 还原
            
            # 评估指标
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # 对数空间的R2（更适合偏态分布）
            r2_log = r2_score(y_test_log, y_pred_log)
            
            # 交叉验证
            cv_scores = cross_val_score(model, X_train_scaled, y_train_log, cv=5, scoring='r2')
            
            results[name] = {
                'rmse': float(rmse),
                'mae': float(mae),
                'r2': float(r2),
                'r2_log': float(r2_log),
                'cv_r2_mean': float(cv_scores.mean()),
                'cv_r2_std': float(cv_scores.std())
            }
            
            # 保存模型
            self._models[name] = model
        
        self._is_trained = True
        self._evaluation_results = results
        
        # 保存最佳模型
        best_model_name = max(results, key=lambda x: results[x]['r2_log'])
        self._best_model_name = best_model_name
        
        return {
            'model_comparison': results,
            'best_model': best_model_name,
            'feature_count': len(self._feature_names),
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def get_feature_importance(self, model_name: str = 'Random Forest') -> list:
        """获取特征重要性"""
        if not self._is_trained:
            self.train_models()
        
        if model_name not in self._models:
            model_name = 'Random Forest'
        
        model = self._models[model_name]
        
        # 获取特征重要性
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_)
        else:
            return []
        
        # 创建特征重要性DataFrame
        feature_importance = pd.DataFrame({
            'feature': self._feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        return feature_importance.to_dict('records')
    
    def predict(self, movie_data: dict, model_name: str = None) -> dict:
        """预测单部电影票房"""
        if not self._is_trained:
            self.train_models()
        
        if model_name is None:
            model_name = self._best_model_name
        
        model = self._models[model_name]
        
        # 构建特征向量
        features = {}
        
        # 数值特征
        numeric_features = ['budget', 'popularity', 'runtime', 'vote_average', 
                           'vote_count', 'release_year', 'release_month']
        
        for f in numeric_features:
            features[f] = movie_data.get(f, 0)
        
        # 派生特征
        features['budget_log'] = np.log1p(features.get('budget', 0))
        features['popularity_log'] = np.log1p(features.get('popularity', 0))
        features['vote_count_log'] = np.log1p(features.get('vote_count', 0))
        
        # 类型特征
        genres = movie_data.get('genres', [])
        features['genre_count'] = len(genres)
        
        if self._mlb is not None:
            genre_encoded = self._mlb.transform([genres])
            for i, g in enumerate(self._mlb.classes_):
                features[f'genre_{g}'] = genre_encoded[0][i]
        
        # 创建特征DataFrame
        X = pd.DataFrame([features])
        
        # 确保列顺序一致
        for col in self._feature_names:
            if col not in X.columns:
                X[col] = 0
        
        X = X[self._feature_names]
        
        # 标准化
        X_scaled = self._scaler.transform(X)
        
        # 预测
        y_pred_log = model.predict(X_scaled)
        y_pred = np.expm1(y_pred_log)[0]
        
        # 计算ROI预测
        budget = movie_data.get('budget', 0)
        predicted_roi = ((y_pred - budget) / budget * 100) if budget > 0 else 0
        
        return {
            'predicted_revenue': float(y_pred),
            'predicted_roi': float(predicted_roi),
            'model_used': model_name,
            'input_features': movie_data
        }
    
    def get_prediction_insights(self) -> dict:
        """获取预测模型洞察"""
        if not self._is_trained:
            self.train_models()
        
        # 特征重要性
        feature_importance = self.get_feature_importance()
        
        # 模型对比
        model_comparison = self._evaluation_results
        
        # 最佳预测变量
        top_features = feature_importance[:10] if feature_importance else []
        
        return {
            'model_comparison': model_comparison,
            'best_model': self._best_model_name,
            'top_features': top_features,
            'all_features': feature_importance
        }
    
    def batch_predict(self, movies_data: list, model_name: str = None) -> list:
        """批量预测多部电影"""
        results = []
        for movie in movies_data:
            pred = self.predict(movie, model_name)
            results.append(pred)
        return results
