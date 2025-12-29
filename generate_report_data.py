import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from analysis.analyzer import MovieAnalyzer

# 设置绘图风格
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei'] # 尝试支持中文
plt.rcParams['axes.unicode_minus'] = False

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print("开始数据分析...")
    analyzer = MovieAnalyzer()
    
    # 输出目录
    base_dir = Path("analysis_results")
    data_dir = base_dir / "data"
    charts_dir = base_dir / "charts"
    ensure_dir(data_dir)
    ensure_dir(charts_dir)

    # 1. ROI 分析
    print("正在进行 ROI 分析...")
    roi_data = analyzer.analyze_roi()
    save_json(roi_data, data_dir / "roi_analysis.json")
    
    # 绘图: ROI 分布
    plt.figure(figsize=(10, 6))
    dist_data = roi_data['distribution']
    plt.bar(dist_data.keys(), dist_data.values())
    plt.title('电影 ROI (投资回报率) 分布区间')
    plt.xlabel('ROI 区间')
    plt.ylabel('电影数量')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(charts_dir / "roi_distribution.png")
    plt.close()

    # 2. ROI 按类型分析
    print("正在按类型分析 ROI...")
    roi_by_genre = analyzer.analyze_roi_by_genre()
    save_json(roi_by_genre, data_dir / "roi_by_genre.json")
    
    # 绘图: 各类型平均 ROI Top 10
    genre_df = pd.DataFrame(roi_by_genre).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=genre_df, x='genre', y='mean_roi')
    plt.title('平均投资回报率最高的 10 种电影类型')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(charts_dir / "top_genre_roi.png")
    plt.close()

    # 3. 类型综合分析
    print("正在进行类型综合分析...")
    genre_analysis = analyzer.analyze_genres()
    save_json(genre_analysis, data_dir / "genre_analysis.json")
    
    # 绘图: 类型数量分布 Top 15
    top_genres = dict(list(genre_analysis['genre_counts'].items())[:15])
    plt.figure(figsize=(12, 6))
    plt.bar(top_genres.keys(), top_genres.values())
    plt.title('电影类型数量分布 (Top 15)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(charts_dir / "genre_counts.png")
    plt.close()

    # 4. 年度趋势分析
    print("正在分析年度趋势...")
    yearly_trends = analyzer.analyze_yearly_trends()
    save_json(yearly_trends, data_dir / "yearly_trends.json")
    
    # 绘图: 年度平均收入与预算
    trends_df = pd.DataFrame(yearly_trends)
    plt.figure(figsize=(14, 7))
    plt.plot(trends_df['year'], trends_df['avg_revenue'], label='平均收入', marker='o')
    plt.plot(trends_df['year'], trends_df['avg_budget'], label='平均预算', marker='x')
    plt.title('电影平均预算与收入年度趋势 (1980-2017)')
    plt.xlabel('年份')
    plt.ylabel('金额 (美元)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(charts_dir / "yearly_financial_trends.png")
    plt.close()

    # 5. 预算与收入散点图
    print("生成预算与收入散点图数据...")
    scatter_data = analyzer.get_scatter_data(limit=1000)
    save_json(scatter_data, data_dir / "scatter_budget_revenue.json")
    
    # 绘图
    scatter_df = pd.DataFrame(scatter_data)
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=scatter_df, x='budget', y='revenue', alpha=0.6)
    plt.title('电影预算 vs 票房收入')
    plt.xlabel('预算 (美元)')
    plt.ylabel('收入 (美元)')
    plt.tight_layout()
    plt.savefig(charts_dir / "budget_vs_revenue_scatter.png")
    plt.close()
    
    # 6. 导演分析
    print("正在分析导演数据...")
    directors = analyzer.analyze_directors()
    save_json(directors, data_dir / "director_analysis.json")

    # 绘图: 总票房最高的导演 Top 10
    top_directors = pd.DataFrame(directors).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_directors, x='director', y='total_revenue')
    plt.title('累计票房最高的 10 位导演')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(charts_dir / "top_directors_revenue.png")
    plt.close()

    print(f"分析完成！结果已保存至 {base_dir.absolute()}")

if __name__ == "__main__":
    main()
