<script lang="ts">
  import { api, type CorrelationData, type PersonStats } from '$lib/api';
  import { Card, Loading, Tabs } from '$lib/components';
  import { HeatmapChart, BarChart } from '$lib/charts';
  import { formatCurrency } from '$utils';
  
  let correlations: CorrelationData | null = $state(null);
  let directors: PersonStats[] = $state([]);
  let actors: PersonStats[] = $state([]);
  let companies: PersonStats[] = $state([]);
  let loading = $state(true);
  let error: string | null = $state(null);
  let activeTab = $state('directors');
  
  const tabs = [
    { id: 'directors', label: '导演', icon: '🎬' },
    { id: 'actors', label: '演员', icon: '🌟' },
    { id: 'companies', label: '制作公司', icon: '🏢' },
    { id: 'correlations', label: '相关性', icon: '🔗' }
  ];
  
  async function loadData() {
    try {
      loading = true;
      error = null;
      
      const [corrRes, dirRes, actRes, compRes] = await Promise.all([
        api.getCorrelations(),
        api.getDirectors(15),
        api.getActors(15),
        api.getCompanies(15)
      ]);
      
      correlations = corrRes;
      directors = dirRes;
      actors = actRes;
      companies = compRes;
    } catch (e) {
      error = e instanceof Error ? e.message : '加载数据失败';
    } finally {
      loading = false;
    }
  }
  
  $effect(() => {
    loadData();
  });
  
  // 相关性热力图数据
  let heatmapData = $derived(() => {
    if (!correlations?.correlation_matrix) return [];
    
    const result: Array<{x: string; y: string; value: number}> = [];
    const vars = correlations.variables;
    
    for (const x of vars) {
      for (const y of vars) {
        result.push({
          x: x,
          y: y,
          value: correlations.correlation_matrix[x][y]
        });
      }
    }
    
    return result;
  });
  
  // 导演票房数据
  let directorRevenueData = $derived(
    directors.slice(0, 10).map(d => ({
      label: (d as {director?: string}).director || 'Unknown',
      value: d.total_revenue
    }))
  );
  
  // 演员票房数据
  let actorRevenueData = $derived(
    actors.slice(0, 10).map(a => ({
      label: (a as {actor?: string}).actor || 'Unknown',
      value: a.total_revenue
    }))
  );
  
  // 公司票房数据
  let companyRevenueData = $derived(
    companies.slice(0, 10).map(c => ({
      label: (c as {company?: string}).company || 'Unknown',
      value: c.total_revenue
    }))
  );
</script>

<div class="analysis-page">
  <div class="page-header">
    <h1>🔍 深度分析</h1>
    <p>导演、演员、制作公司及变量相关性分析</p>
  </div>
  
  <div class="tabs-container">
    <Tabs {tabs} {activeTab} onTabChange={(id) => activeTab = id} />
  </div>
  
  {#if loading}
    <Loading size="lg" />
  {:else if error}
    <div class="error-message">
      <p>❌ {error}</p>
      <button onclick={loadData}>重试</button>
    </div>
  {:else}
    <div class="tab-content">
      {#if activeTab === 'directors'}
        <div class="section-grid">
          <Card title="🎬 票房最高导演 Top 10" subtitle="按总票房排名">
            <BarChart 
              data={directorRevenueData}
              width={550}
              height={400}
              horizontal
              formatValue={(d) => formatCurrency(d)}
              xLabel="总票房"
            />
          </Card>
          
          <Card title="📋 导演详细数据" subtitle="Top 15 导演统计">
            <div class="data-table">
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>导演</th>
                    <th>作品数</th>
                    <th>总票房</th>
                    <th>平均票房</th>
                    <th>平均评分</th>
                  </tr>
                </thead>
                <tbody>
                  {#each directors as dir, i}
                    <tr>
                      <td class="rank">{i + 1}</td>
                      <td class="name">{(dir as {director?: string}).director}</td>
                      <td>{dir.movie_count}</td>
                      <td>{formatCurrency(dir.total_revenue)}</td>
                      <td>{formatCurrency(dir.avg_revenue)}</td>
                      <td>{dir.avg_rating.toFixed(1)}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
        
      {:else if activeTab === 'actors'}
        <div class="section-grid">
          <Card title="🌟 票房最高演员 Top 10" subtitle="按总票房排名">
            <BarChart 
              data={actorRevenueData}
              width={550}
              height={400}
              horizontal
              formatValue={(d) => formatCurrency(d)}
              xLabel="总票房"
            />
          </Card>
          
          <Card title="📋 演员详细数据" subtitle="Top 15 演员统计">
            <div class="data-table">
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>演员</th>
                    <th>作品数</th>
                    <th>总票房</th>
                    <th>平均票房</th>
                    <th>平均评分</th>
                  </tr>
                </thead>
                <tbody>
                  {#each actors as act, i}
                    <tr>
                      <td class="rank">{i + 1}</td>
                      <td class="name">{(act as {actor?: string}).actor}</td>
                      <td>{act.movie_count}</td>
                      <td>{formatCurrency(act.total_revenue)}</td>
                      <td>{formatCurrency(act.avg_revenue)}</td>
                      <td>{act.avg_rating.toFixed(1)}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
        
      {:else if activeTab === 'companies'}
        <div class="section-grid">
          <Card title="🏢 票房最高制作公司 Top 10" subtitle="按总票房排名">
            <BarChart 
              data={companyRevenueData}
              width={550}
              height={400}
              horizontal
              formatValue={(d) => formatCurrency(d)}
              xLabel="总票房"
            />
          </Card>
          
          <Card title="📋 公司详细数据" subtitle="Top 15 制作公司统计">
            <div class="data-table">
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>公司</th>
                    <th>作品数</th>
                    <th>总票房</th>
                    <th>平均票房</th>
                    <th>平均ROI</th>
                  </tr>
                </thead>
                <tbody>
                  {#each companies as comp, i}
                    <tr>
                      <td class="rank">{i + 1}</td>
                      <td class="name">{(comp as {company?: string}).company}</td>
                      <td>{comp.movie_count}</td>
                      <td>{formatCurrency(comp.total_revenue)}</td>
                      <td>{formatCurrency(comp.avg_revenue)}</td>
                      <td class:positive={comp.avg_roi > 0}>{comp.avg_roi.toFixed(0)}%</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
        
      {:else if activeTab === 'correlations'}
        <div class="section-grid">
          <Card title="🔗 变量相关性热力图" subtitle="电影各属性间的相关系数">
            <HeatmapChart 
              data={heatmapData()}
              width={550}
              height={500}
            />
          </Card>
          
          <Card title="📊 强相关变量对" subtitle="相关系数绝对值最大的变量对">
            <div class="correlation-list">
              {#each (correlations?.top_correlations || []).slice(0, 10) as corr, i}
                <div class="corr-item">
                  <span class="corr-rank">#{i + 1}</span>
                  <div class="corr-vars">
                    <span class="var">{corr.var1}</span>
                    <span class="arrow">↔</span>
                    <span class="var">{corr.var2}</span>
                  </div>
                  <span 
                    class="corr-value"
                    class:positive={corr.correlation > 0}
                    class:negative={corr.correlation < 0}
                  >
                    {corr.correlation.toFixed(3)}
                  </span>
                </div>
              {/each}
            </div>
          </Card>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .analysis-page {
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
  
  .tabs-container {
    margin-bottom: 28px;
  }
  
  .section-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
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
  
  .data-table {
    overflow-x: auto;
    max-height: 400px;
    overflow-y: auto;
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
    font-weight: 700;
    color: #6b7280;
    background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
    position: sticky;
    top: 0;
    letter-spacing: 0.3px;
  }
  
  tr:hover {
    background: rgba(59, 130, 246, 0.03);
  }
  
  .rank {
    font-weight: 700;
    color: #6b7280;
  }
  
  .name {
    font-weight: 500;
    max-width: 180px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .positive {
    color: #10b981;
  }
  
  .negative {
    color: #ef4444;
  }
  
  .correlation-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .corr-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 16px;
    background: #f9fafb;
    border-radius: 8px;
  }
  
  .corr-rank {
    font-size: 12px;
    font-weight: 600;
    color: #6b7280;
    width: 28px;
  }
  
  .corr-vars {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .var {
    font-size: 13px;
    font-weight: 500;
    padding: 4px 10px;
    background: white;
    border-radius: 4px;
    border: 1px solid #e5e7eb;
  }
  
  .arrow {
    color: #9ca3af;
  }
  
  .corr-value {
    font-size: 15px;
    font-weight: 700;
  }
</style>
