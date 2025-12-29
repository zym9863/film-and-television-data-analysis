<script lang="ts">
  import { api, type RoiData } from '$lib/api';
  import { Card, Loading } from '$lib/components';
  import { BarChart, ScatterPlot } from '$lib/charts';
  import { formatCurrency } from '$utils';
  
  let roiData: RoiData | null = $state(null);
  let scatterData: Array<{x: number; y: number; label: string}> = $state([]);
  let loading = $state(true);
  let error: string | null = $state(null);
  
  async function loadData() {
    try {
      loading = true;
      error = null;
      
      const [roiRes, scatterRes] = await Promise.all([
        api.getRoi(),
        api.getScatter('budget', 'revenue', 300)
      ]);
      
      roiData = roiRes;
      scatterData = scatterRes.map(d => ({
        x: d.budget,
        y: d.revenue,
        label: d.title,
        size: Math.max(3, Math.min(10, d.vote_average))
      }));
    } catch (e) {
      error = e instanceof Error ? e.message : '加载数据失败';
    } finally {
      loading = false;
    }
  }
  
  $effect(() => {
    loadData();
  });
  
  // 派生数据
  let genreRoiData = $derived(
    roiData?.by_genre?.slice(0, 15).map(g => ({
      label: g.genre,
      value: g.mean_roi,
      color: g.mean_roi >= 0 ? '#10b981' : '#ef4444'
    })) || []
  );
  
  let budgetRoiData = $derived(
    roiData?.by_budget_range?.map(b => ({
      label: b.budget_range,
      value: b.mean_roi,
      color: b.mean_roi >= 0 ? '#10b981' : '#ef4444'
    })) || []
  );
</script>

<div class="roi-page">
  <div class="page-header">
    <h1>💰 ROI 投资回报分析</h1>
    <p>电影投资回报率深度分析</p>
  </div>
  
  {#if loading}
    <Loading size="lg" />
  {:else if error}
    <div class="error-message">
      <p>❌ {error}</p>
      <button onclick={loadData}>重试</button>
    </div>
  {:else}
    <!-- ROI 统计概览 -->
    <div class="roi-stats">
      <div class="stat-item">
        <div class="stat-value">{roiData?.overview?.statistics?.mean?.toFixed(1)}%</div>
        <div class="stat-label">平均ROI</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{roiData?.overview?.statistics?.median?.toFixed(1)}%</div>
        <div class="stat-label">中位数ROI</div>
      </div>
      <div class="stat-item">
        <div class="stat-value positive">{roiData?.overview?.statistics?.profitable_count}</div>
        <div class="stat-label">盈利电影</div>
      </div>
      <div class="stat-item">
        <div class="stat-value negative">{roiData?.overview?.statistics?.loss_count}</div>
        <div class="stat-label">亏损电影</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{roiData?.overview?.statistics?.profitable_rate?.toFixed(1)}%</div>
        <div class="stat-label">盈利率</div>
      </div>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-grid">
      <Card title="📊 预算 vs 票房" subtitle="散点图展示预算与票房的关系">
        <ScatterPlot 
          data={scatterData}
          width={550}
          height={400}
          xLabel="预算 (Budget)"
          yLabel="票房 (Revenue)"
          formatX={(d) => formatCurrency(d)}
          formatY={(d) => formatCurrency(d)}
          showTrendLine
        />
      </Card>
      
      <Card title="🎭 类型ROI对比" subtitle="各电影类型的平均投资回报率">
        <BarChart 
          data={genreRoiData}
          width={550}
          height={400}
          horizontal
          xLabel="平均ROI (%)"
          formatValue={(d) => `${d.toFixed(0)}%`}
        />
      </Card>
      
      <Card title="💵 预算区间ROI" subtitle="不同预算规模的投资回报率">
        <BarChart 
          data={budgetRoiData}
          width={550}
          height={400}
          xLabel="预算区间"
          yLabel="平均ROI (%)"
          formatValue={(d) => `${d.toFixed(0)}%`}
        />
      </Card>
      
      <Card title="🏆 高ROI电影榜" subtitle="投资回报率最高的10部电影">
        <div class="movie-table">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>电影</th>
                <th>预算</th>
                <th>票房</th>
                <th>ROI</th>
              </tr>
            </thead>
            <tbody>
              {#each (roiData?.overview?.top_roi_movies || []).slice(0, 10) as movie, i}
                <tr>
                  <td class="rank">{i + 1}</td>
                  <td class="title">{movie.title}</td>
                  <td>{formatCurrency(movie.budget)}</td>
                  <td>{formatCurrency(movie.revenue)}</td>
                  <td class="roi positive">{movie.roi.toFixed(0)}%</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  {/if}
</div>

<style>
  .roi-page {
    padding: 24px;
    max-width: 1400px;
    margin: 0 auto;
  }
  
  .page-header {
    margin-bottom: 32px;
  }
  
  .page-header h1 {
    font-size: 28px;
    font-weight: 700;
    color: #111827;
    margin: 0;
  }
  
  .page-header p {
    font-size: 15px;
    color: #6b7280;
    margin: 8px 0 0;
  }
  
  .roi-stats {
    display: flex;
    gap: 24px;
    margin-bottom: 32px;
    padding: 24px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    flex-wrap: wrap;
  }
  
  .stat-item {
    flex: 1;
    min-width: 120px;
    text-align: center;
  }
  
  .stat-value {
    font-size: 32px;
    font-weight: 700;
    color: #111827;
  }
  
  .stat-value.positive {
    color: #10b981;
  }
  
  .stat-value.negative {
    color: #ef4444;
  }
  
  .stat-label {
    font-size: 13px;
    color: #6b7280;
    margin-top: 4px;
  }
  
  .charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
    gap: 24px;
  }
  
  .error-message {
    text-align: center;
    padding: 40px;
    color: #ef4444;
  }
  
  .error-message button {
    margin-top: 16px;
    padding: 8px 24px;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
  
  .movie-table {
    overflow-x: auto;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }
  
  th, td {
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
  }
  
  th {
    font-weight: 600;
    color: #6b7280;
    background: #f9fafb;
  }
  
  .rank {
    font-weight: 700;
    color: #6b7280;
  }
  
  .title {
    font-weight: 500;
    max-width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .roi {
    font-weight: 700;
  }
  
  .roi.positive {
    color: #10b981;
  }
</style>
