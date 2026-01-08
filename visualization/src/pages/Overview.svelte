<script lang="ts">
  import { api, type OverviewStats, type RoiData, type GenreData } from '$lib/api';
  import { Card, StatCard, Loading } from '$lib/components';
  import { BarChart, PieChart } from '$lib/charts';
  import { formatCurrency } from '$utils';
  
  let overview: OverviewStats | null = $state(null);
  let roiData: RoiData | null = $state(null);
  let genreData: GenreData | null = $state(null);
  let loading = $state(true);
  let error: string | null = $state(null);
  
  async function loadData() {
    try {
      loading = true;
      error = null;
      
      const [overviewRes, roiRes, genreRes] = await Promise.all([
        api.getOverview(),
        api.getRoi(),
        api.getGenres()
      ]);
      
      overview = overviewRes;
      roiData = roiRes;
      genreData = genreRes;
    } catch (e) {
      error = e instanceof Error ? e.message : '加载数据失败';
      console.error('Failed to load data:', e);
    } finally {
      loading = false;
    }
  }
  
  $effect(() => {
    loadData();
  });
  
  // 计算派生数据
  let genreBarData = $derived(
    genreData?.genre_statistics?.slice(0, 10).map(g => ({
      label: g.genre,
      value: g.count
    })) || []
  );
  
  let genrePieData = $derived(
    genreData?.genre_statistics?.slice(0, 8).map(g => ({
      label: g.genre,
      value: g.total_revenue
    })) || []
  );
  
  let roiDistributionData = $derived(
    roiData?.overview?.distribution 
      ? Object.entries(roiData.overview.distribution).map(([label, value]) => ({
          label,
          value: value as number
        }))
      : []
  );
</script>

<div class="overview-page">
  <div class="page-header">
    <h1>📊 TMDB 影视数据分析</h1>
    <p>基于TMDB 5000电影数据集的综合分析仪表板</p>
  </div>
  
  {#if loading}
    <Loading size="lg" />
  {:else if error}
    <div class="error-message">
      <p>❌ {error}</p>
      <button onclick={loadData}>重试</button>
    </div>
  {:else}
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <StatCard 
        value={overview?.total_movies || 0} 
        label="电影总数" 
        icon="🎬" 
      />
      <StatCard 
        value={overview?.movies_with_financial_data || 0} 
        label="有财务数据" 
        icon="💰" 
      />
      <StatCard 
        value={overview?.budget?.mean || 0} 
        label="平均预算" 
        format="currency"
        icon="📈" 
      />
      <StatCard 
        value={overview?.revenue?.mean || 0} 
        label="平均票房" 
        format="currency"
        icon="🎯" 
      />
      <StatCard 
        value={roiData?.overview?.statistics?.profitable_rate || 0} 
        label="盈利率" 
        format="percent"
        icon="✅" 
      />
      <StatCard 
        value={overview?.vote_average?.mean || 0} 
        label="平均评分" 
        icon="⭐" 
      />
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-grid">
      <Card title="🎭 电影类型分布" subtitle="Top 10 类型数量统计">
        <BarChart 
          data={genreBarData} 
          width={500} 
          height={350}
          xLabel="类型"
          yLabel="数量"
        />
      </Card>
      
      <Card title="💵 类型票房占比" subtitle="Top 8 类型总票房分布">
        <PieChart 
          data={genrePieData}
          width={450}
          height={350}
          innerRadius={60}
        />
      </Card>
      
      <Card title="📊 ROI 分布" subtitle="投资回报率区间分布">
        <BarChart 
          data={roiDistributionData}
          width={500}
          height={350}
          horizontal
          formatValue={(d) => d.toString()}
          yLabel="电影数量"
        />
      </Card>
      
      <Card title="🏆 高ROI电影 Top 5" subtitle="投资回报率最高的电影">
        <div class="movie-list">
          {#each (roiData?.overview?.top_roi_movies || []).slice(0, 5) as movie, i}
            <div class="movie-item">
              <span class="rank">#{i + 1}</span>
              <div class="movie-info">
                <div class="movie-title">{movie.title}</div>
                <div class="movie-meta">
                  {movie.release_year} · {movie.genre_names.slice(0, 2).join(', ')}
                </div>
              </div>
              <div class="movie-roi" class:positive={movie.roi > 0}>
                {movie.roi.toFixed(0)}%
              </div>
            </div>
          {/each}
        </div>
      </Card>
    </div>
  {/if}
</div>

<style>
  .overview-page {
    padding: 32px;
    max-width: 1400px;
    margin: 0 auto;
    animation: fadeIn 0.6s ease-in-out;
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .page-header {
    margin-bottom: 36px;
    padding: 28px 32px;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.8) 100%);
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border-left: 5px solid #3b82f6;
  }
  
  .page-header h1 {
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -0.5px;
  }
  
  .page-header p {
    font-size: 15px;
    color: #6b7280;
    margin: 10px 0 0;
    font-weight: 500;
    line-height: 1.6;
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-bottom: 36px;
  }
  
  .charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    gap: 28px;
  }
  
  .error-message {
    text-align: center;
    padding: 60px 40px;
    color: #ef4444;
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }
  
  .error-message button {
    margin-top: 20px;
    padding: 12px 32px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    font-size: 14px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  }
  
  .error-message button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
  }
  
  .movie-list {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  
  .movie-item {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 16px 20px;
    background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
    border-radius: 12px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-left: 4px solid transparent;
  }
  
  .movie-item:hover {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border-left-color: #3b82f6;
    transform: translateX(8px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }
  
  .rank {
    font-size: 16px;
    font-weight: 800;
    color: #6b7280;
    width: 36px;
    text-align: center;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .movie-info {
    flex: 1;
  }
  
  .movie-title {
    font-size: 15px;
    font-weight: 700;
    color: #111827;
    letter-spacing: 0.2px;
  }
  
  .movie-meta {
    font-size: 12px;
    color: #6b7280;
    margin-top: 4px;
    font-weight: 500;
  }
  
  .movie-roi {
    font-size: 18px;
    font-weight: 800;
    color: #10b981;
    padding: 8px 16px;
    background: rgba(16, 185, 129, 0.1);
    border-radius: 8px;
    letter-spacing: 0.3px;
  }
  
  .movie-roi.positive {
    color: #059669;
    background: rgba(16, 185, 129, 0.1);
  }
</style>
