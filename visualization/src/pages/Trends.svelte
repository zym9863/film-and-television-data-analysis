<script lang="ts">
  import { api, type TrendsData } from '$lib/api';
  import { Card, Loading } from '$lib/components';
  import { LineChart, BarChart } from '$lib/charts';
  import { formatCurrency } from '$utils';
  
  let trendsData: TrendsData | null = $state(null);
  let loading = $state(true);
  let error: string | null = $state(null);
  
  async function loadData() {
    try {
      loading = true;
      error = null;
      trendsData = await api.getTrends();
    } catch (e) {
      error = e instanceof Error ? e.message : '加载数据失败';
    } finally {
      loading = false;
    }
  }
  
  $effect(() => {
    loadData();
  });
  
  // 派生数据 - 年度电影数量
  let yearlyCountData = $derived(
    trendsData?.yearly?.filter(y => y.year >= 1990)?.map(y => ({
      x: y.year,
      y: y.movie_count
    })) || []
  );
  
  // 年度平均票房
  let yearlyRevenueData = $derived(
    trendsData?.yearly?.filter(y => y.year >= 1990 && y.avg_revenue > 0)?.map(y => ({
      x: y.year,
      y: y.avg_revenue
    })) || []
  );
  
  // 年度平均评分
  let yearlyRatingData = $derived(
    trendsData?.yearly?.filter(y => y.year >= 1990)?.map(y => ({
      x: y.year,
      y: y.avg_rating
    })) || []
  );
  
  // 月度发行数据
  let monthlyData = $derived(
    trendsData?.monthly?.map(m => ({
      label: m.month_name,
      value: m.avg_revenue
    })) || []
  );
  
  // 月度ROI数据
  let monthlyRoiData = $derived(
    trendsData?.monthly?.map(m => ({
      label: m.month_name,
      value: m.avg_roi,
      color: m.avg_roi >= 0 ? '#10b981' : '#ef4444'
    })) || []
  );
</script>

<div class="trends-page">
  <div class="page-header">
    <h1>📈 时间趋势分析</h1>
    <p>电影产业的历史发展趋势</p>
  </div>
  
  {#if loading}
    <Loading size="lg" />
  {:else if error}
    <div class="error-message">
      <p>❌ {error}</p>
      <button onclick={loadData}>重试</button>
    </div>
  {:else}
    <div class="charts-grid">
      <Card title="🎬 年度电影产量" subtitle="1990-2017年电影发行数量趋势">
        <LineChart 
          data={yearlyCountData}
          width={600}
          height={350}
          xLabel="年份"
          yLabel="电影数量"
          showArea
        />
      </Card>
      
      <Card title="💵 年度平均票房" subtitle="1990-2017年平均票房变化">
        <LineChart 
          data={yearlyRevenueData}
          width={600}
          height={350}
          xLabel="年份"
          yLabel="平均票房"
          formatY={(d) => formatCurrency(d)}
          showArea
        />
      </Card>
      
      <Card title="⭐ 年度平均评分" subtitle="1990-2017年电影评分趋势">
        <LineChart 
          data={yearlyRatingData}
          width={600}
          height={350}
          xLabel="年份"
          yLabel="平均评分"
          formatY={(d) => d.toFixed(1)}
        />
      </Card>
      
      <Card title="📅 月度发行规律" subtitle="不同月份的平均票房表现">
        <BarChart 
          data={monthlyData}
          width={600}
          height={350}
          xLabel="月份"
          yLabel="平均票房"
          formatValue={(d) => formatCurrency(d)}
        />
      </Card>
      
      <Card title="📊 月度ROI分析" subtitle="不同月份发行电影的平均投资回报率">
        <BarChart 
          data={monthlyRoiData}
          width={600}
          height={350}
          xLabel="月份"
          yLabel="平均ROI (%)"
          formatValue={(d) => `${d.toFixed(0)}%`}
        />
      </Card>
      
      <Card title="📋 年度数据表" subtitle="详细年度统计数据">
        <div class="data-table">
          <table>
            <thead>
              <tr>
                <th>年份</th>
                <th>电影数</th>
                <th>平均预算</th>
                <th>平均票房</th>
                <th>平均评分</th>
              </tr>
            </thead>
            <tbody>
              {#each (trendsData?.yearly || []).filter(y => y.year >= 2000).reverse().slice(0, 10) as year}
                <tr>
                  <td class="year">{year.year}</td>
                  <td>{year.movie_count}</td>
                  <td>{formatCurrency(year.avg_budget)}</td>
                  <td>{formatCurrency(year.avg_revenue)}</td>
                  <td>{year.avg_rating.toFixed(1)}</td>
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
  .trends-page {
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
  
  .charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(580px, 1fr));
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
  
  .data-table {
    overflow-x: auto;
    max-height: 300px;
    overflow-y: auto;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }
  
  th, td {
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
  }
  
  th {
    font-weight: 600;
    color: #6b7280;
    background: #f9fafb;
    position: sticky;
    top: 0;
  }
  
  .year {
    font-weight: 600;
  }
</style>
