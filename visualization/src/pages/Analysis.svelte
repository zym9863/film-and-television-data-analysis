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

  let topDirector = $derived(() => directors[0]);
  let topActor = $derived(() => actors[0]);
  let topCompany = $derived(() => companies[0]);
  let topCorrelation = $derived(() => correlations?.top_correlations?.[0]);
</script>

<div class="analysis-page">
  <div class="page-hero">
    <div class="hero-main">
      <div class="hero-eyebrow">Cinema Intel · Deep Dive</div>
      <h1>🔍 深度分析</h1>
      <p>导演、演员、制作公司与核心变量之间的关系洞察。</p>
      <div class="hero-tags">
        <span class="tag">导演样本 {directors.length}</span>
        <span class="tag">演员样本 {actors.length}</span>
        <span class="tag">公司样本 {companies.length}</span>
        {#if topCorrelation()}
          <span class="tag accent">最强相关 {topCorrelation()!.var1} ↔ {topCorrelation()!.var2}</span>
        {/if}
      </div>
    </div>
    <div class="hero-metrics">
      <div class="metric-card">
        <div class="metric-label">票房冠军导演</div>
        <div class="metric-value">{topDirector()?.director ?? '—'}</div>
        <div class="metric-sub">{topDirector() ? formatCurrency(topDirector()!.total_revenue) : '—'}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">票房冠军演员</div>
        <div class="metric-value">{topActor()?.actor ?? '—'}</div>
        <div class="metric-sub">{topActor() ? formatCurrency(topActor()!.total_revenue) : '—'}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">最强公司引擎</div>
        <div class="metric-value">{topCompany()?.company ?? '—'}</div>
        <div class="metric-sub">{topCompany() ? formatCurrency(topCompany()!.total_revenue) : '—'}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">最强相关系数</div>
        <div class="metric-value mono" class:positive={topCorrelation() && topCorrelation()!.correlation > 0} class:negative={topCorrelation() && topCorrelation()!.correlation < 0}>
          {topCorrelation() ? topCorrelation()!.correlation.toFixed(3) : '—'}
        </div>
        <div class="metric-sub">{topCorrelation() ? `${topCorrelation()!.var1} ↔ ${topCorrelation()!.var2}` : '—'}</div>
      </div>
    </div>
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
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .page-hero {
    display: grid;
    grid-template-columns: minmax(320px, 1.2fr) minmax(260px, 1fr);
    gap: 20px;
    align-items: stretch;
  }

  .hero-main {
    padding: 24px;
    border-radius: 20px;
    background: linear-gradient(150deg, rgba(29, 24, 21, 0.98), rgba(12, 10, 9, 0.98));
    border: 1px solid var(--border);
    box-shadow: var(--shadow-soft);
    position: relative;
    overflow: hidden;
  }

  .hero-main::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(360px 200px at 0% 0%, rgba(209, 164, 90, 0.35), transparent 70%);
    opacity: 0.8;
    pointer-events: none;
  }

  .hero-eyebrow {
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 8px;
  }

  .hero-main h1 {
    font-size: 30px;
    font-weight: 700;
    margin: 0 0 8px;
    color: var(--text);
    font-family: var(--font-display);
    letter-spacing: 0.6px;
  }

  .hero-main p {
    margin: 0 0 18px;
    color: var(--muted);
    font-size: 14px;
  }

  .hero-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    position: relative;
    z-index: 1;
  }

  .tag {
    padding: 6px 12px;
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 12px;
    color: var(--muted);
    background: rgba(255, 255, 255, 0.04);
  }

  .tag.accent {
    color: #1b1309;
    background: linear-gradient(135deg, #f0d7a7, #d1a45a);
    border-color: rgba(209, 164, 90, 0.6);
    font-weight: 600;
  }

  .hero-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
  }

  .metric-card {
    padding: 16px 18px;
    border-radius: 16px;
    background: linear-gradient(160deg, rgba(24, 20, 18, 0.98), rgba(15, 12, 10, 0.98));
    border: 1px solid rgba(209, 164, 90, 0.2);
    box-shadow: var(--shadow-soft);
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .metric-label {
    font-size: 11px;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: var(--muted);
  }

  .metric-value {
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
  }

  .metric-value.mono {
    font-family: var(--font-mono);
    font-size: 20px;
  }

  .metric-sub {
    font-size: 12px;
    color: var(--muted);
  }
  
  .tabs-container {
    margin-top: 4px;
  }
  
  .section-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(520px, 1fr));
    gap: 24px;
  }
  
  .error-message {
    text-align: center;
    padding: 40px;
    color: var(--negative);
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 122, 122, 0.35);
    border-radius: 16px;
  }
  
  .error-message button {
    margin-top: 16px;
    padding: 8px 24px;
    background: linear-gradient(135deg, #f0d7a7, #d1a45a);
    color: #1b1309;
    border: none;
    border-radius: 999px;
    cursor: pointer;
    font-weight: 600;
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
    color: var(--text);
  }
  
  th, td {
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }
  
  th {
    font-weight: 600;
    color: var(--muted);
    background: rgba(209, 164, 90, 0.08);
    position: sticky;
    top: 0;
  }

  tbody tr:hover {
    background: rgba(255, 255, 255, 0.03);
  }
  
  .rank {
    font-weight: 600;
    color: var(--muted);
  }
  
  .name {
    font-weight: 500;
    max-width: 180px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .positive {
    color: var(--positive);
  }
  
  .negative {
    color: var(--negative);
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
    background: rgba(255, 255, 255, 0.04);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
  }
  
  .corr-rank {
    font-size: 12px;
    font-weight: 600;
    color: var(--muted);
    width: 28px;
  }
  
  .corr-vars {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .var {
    font-size: 12px;
    font-weight: 500;
    padding: 4px 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.08);
  }
  
  .arrow {
    color: var(--muted);
  }
  
  .corr-value {
    font-size: 15px;
    font-weight: 700;
    font-family: var(--font-mono);
  }

  @media (max-width: 1100px) {
    .page-hero {
      grid-template-columns: 1fr;
    }
  }
</style>
