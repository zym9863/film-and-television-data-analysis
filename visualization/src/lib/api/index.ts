/**
 * API 客户端模块
 * 与 FastAPI 后端通信
 */

const API_BASE_URL = 'http://localhost:8000';

export interface ApiResponse<T> {
  success: boolean;
  data: T;
}

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }
  
  const result: ApiResponse<T> = await response.json();
  
  if (!result.success) {
    throw new Error('API returned unsuccessful response');
  }
  
  return result.data;
}

// ==================== API 类型定义 ====================

export interface OverviewStats {
  total_movies: number;
  movies_with_financial_data: number;
  year_range: { min: number; max: number };
  budget: { mean: number; median: number; min: number; max: number };
  revenue: { mean: number; median: number; min: number; max: number };
  vote_average: { mean: number; median: number };
}

export interface RoiStatistics {
  mean: number;
  median: number;
  std: number;
  min: number;
  max: number;
  profitable_count: number;
  loss_count: number;
  profitable_rate: number;
}

export interface RoiMovie {
  title: string;
  budget: number;
  revenue: number;
  roi: number;
  release_year: number;
  genre_names: string[];
}

export interface RoiData {
  overview: {
    statistics: RoiStatistics;
    distribution: Record<string, number>;
    top_roi_movies: RoiMovie[];
    bottom_roi_movies: RoiMovie[];
  };
  by_genre: Array<{
    genre: string;
    mean_roi: number;
    median_roi: number;
    std_roi: number;
    count: number;
    avg_budget: number;
    avg_revenue: number;
  }>;
  by_budget_range: Array<{
    budget_range: string;
    mean_roi: number;
    median_roi: number;
    count: number;
    avg_revenue: number;
  }>;
}

export interface GenreData {
  genre_counts: Record<string, number>;
  genre_combinations: Record<string, number>;
  genre_statistics: Array<{
    genre: string;
    count: number;
    avg_revenue: number;
    total_revenue: number;
    avg_budget: number;
    avg_rating: number;
    avg_roi: number;
  }>;
}

export interface YearlyTrend {
  year: number;
  movie_count: number;
  avg_rating: number;
  avg_popularity: number;
  avg_runtime: number;
  avg_budget: number;
  total_budget: number;
  avg_revenue: number;
  total_revenue: number;
  avg_roi: number;
}

export interface MonthlyPattern {
  month: number;
  month_name: string;
  movie_count: number;
  avg_revenue: number;
  avg_budget: number;
  avg_roi: number;
  avg_rating: number;
}

export interface TrendsData {
  yearly: YearlyTrend[];
  monthly: MonthlyPattern[];
}

export interface PersonStats {
  director?: string;
  actor?: string;
  company?: string;
  movie_count: number;
  total_revenue: number;
  avg_revenue: number;
  total_budget: number;
  avg_budget: number;
  avg_rating: number;
  avg_roi: number;
}

export interface CorrelationData {
  top_correlations: Array<{ var1: string; var2: string; correlation: number }>;
  correlation_matrix: Record<string, Record<string, number>>;
  variables: string[];
}

export interface ScatterPoint {
  budget: number;
  revenue: number;
  title: string;
  release_year: number;
  genre_names: string[];
  vote_average: number;
}

export interface ModelComparison {
  [modelName: string]: {
    rmse: number;
    mae: number;
    r2: number;
    r2_log: number;
    cv_r2_mean: number;
    cv_r2_std: number;
  };
}

export interface FeatureImportance {
  feature: string;
  importance: number;
}

export interface PredictionInsights {
  model_comparison: ModelComparison;
  best_model: string;
  top_features: FeatureImportance[];
  all_features: FeatureImportance[];
}

export interface PredictionRequest {
  budget: number;
  popularity?: number;
  runtime?: number;
  vote_average?: number;
  vote_count?: number;
  release_year?: number;
  release_month?: number;
  genres?: string[];
}

export interface PredictionResult {
  predicted_revenue: number;
  predicted_roi: number;
  model_used: string;
  input_features: PredictionRequest;
}

// ==================== API 函数 ====================

export const api = {
  /** 获取数据集概览 */
  getOverview: () => fetchApi<OverviewStats>('/api/overview'),
  
  /** 获取ROI分析 */
  getRoi: () => fetchApi<RoiData>('/api/roi'),
  
  /** 获取类型分析 */
  getGenres: () => fetchApi<GenreData>('/api/genres'),
  
  /** 获取时间趋势 */
  getTrends: () => fetchApi<TrendsData>('/api/trends'),
  
  /** 获取导演分析 */
  getDirectors: (topN = 20) => fetchApi<PersonStats[]>(`/api/directors?top_n=${topN}`),
  
  /** 获取演员分析 */
  getActors: (topN = 20) => fetchApi<PersonStats[]>(`/api/actors?top_n=${topN}`),
  
  /** 获取制作公司分析 */
  getCompanies: (topN = 20) => fetchApi<PersonStats[]>(`/api/companies?top_n=${topN}`),
  
  /** 获取相关性分析 */
  getCorrelations: () => fetchApi<CorrelationData>('/api/correlations'),
  
  /** 获取散点图数据 */
  getScatter: (x = 'budget', y = 'revenue', limit = 500) => 
    fetchApi<ScatterPoint[]>(`/api/scatter?x=${x}&y=${y}&limit=${limit}`),
  
  /** 训练预测模型 */
  trainModel: () => fetchApi<{ model_comparison: ModelComparison; best_model: string }>('/api/prediction/train'),
  
  /** 获取预测洞察 */
  getPredictionInsights: () => fetchApi<PredictionInsights>('/api/prediction/insights'),
  
  /** 预测票房 */
  predict: (data: PredictionRequest) => 
    fetchApi<PredictionResult>('/api/prediction/predict', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

export default api;
