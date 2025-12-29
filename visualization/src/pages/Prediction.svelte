<script lang="ts">
  import { api, type PredictionInsights, type PredictionResult } from '$lib/api';
  import { Card, Loading } from '$lib/components';
  import { BarChart } from '$lib/charts';
  import { formatCurrency } from '$utils';
  
  let insights: PredictionInsights | null = $state(null);
  let predictionResult: PredictionResult | null = $state(null);
  let loading = $state(true);
  let predicting = $state(false);
  let error: string | null = $state(null);
  
  // 预测表单数据
  let formData = $state({
    budget: 50000000,
    popularity: 20,
    runtime: 120,
    vote_average: 7.0,
    vote_count: 500,
    release_year: 2024,
    release_month: 6,
    genres: ['Action', 'Adventure']
  });
  
  const availableGenres = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime',
    'Documentary', 'Drama', 'Family', 'Fantasy', 'History',
    'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction',
    'Thriller', 'War', 'Western'
  ];
  
  async function loadData() {
    try {
      loading = true;
      error = null;
      insights = await api.getPredictionInsights();
    } catch (e) {
      error = e instanceof Error ? e.message : '加载数据失败';
    } finally {
      loading = false;
    }
  }
  
  async function predict() {
    try {
      predicting = true;
      predictionResult = await api.predict(formData);
    } catch (e) {
      error = e instanceof Error ? e.message : '预测失败';
    } finally {
      predicting = false;
    }
  }
  
  function toggleGenre(genre: string) {
    if (formData.genres.includes(genre)) {
      formData.genres = formData.genres.filter(g => g !== genre);
    } else {
      formData.genres = [...formData.genres, genre];
    }
  }
  
  $effect(() => {
    loadData();
  });
  
  // 特征重要性数据
  let featureImportanceData = $derived(
    insights?.top_features?.slice(0, 10).map(f => ({
      label: f.feature.replace('genre_', '').replace('_log', ' (log)'),
      value: f.importance * 100
    })) || []
  );
  
  // 模型对比数据
  let modelComparisonData = $derived(
    insights?.model_comparison 
      ? Object.entries(insights.model_comparison).map(([name, metrics]) => ({
          label: name,
          value: metrics.r2_log * 100
        }))
      : []
  );
</script>

<div class="prediction-page">
  <div class="page-header">
    <h1>🎯 票房预测模型</h1>
    <p>基于机器学习的电影票房预测系统</p>
  </div>
  
  {#if loading}
    <Loading size="lg" />
  {:else if error}
    <div class="error-message">
      <p>❌ {error}</p>
      <button onclick={loadData}>重试</button>
    </div>
  {:else}
    <div class="content-grid">
      <!-- 预测表单 -->
      <Card title="🎬 票房预测器" subtitle="输入电影信息预测票房">
        <form class="prediction-form" onsubmit={(e) => { e.preventDefault(); predict(); }}>
          <div class="form-row">
            <div class="form-group">
              <label for="budget-input">预算 (美元)</label>
              <input 
                id="budget-input"
                type="number" 
                bind:value={formData.budget}
                min="0"
                step="1000000"
              />
            </div>
            <div class="form-group">
              <label for="popularity-input">热度值</label>
              <input 
                id="popularity-input"
                type="number" 
                bind:value={formData.popularity}
                min="0"
                max="1000"
                step="1"
              />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="runtime-input">时长 (分钟)</label>
              <input 
                id="runtime-input"
                type="number" 
                bind:value={formData.runtime}
                min="30"
                max="300"
              />
            </div>
            <div class="form-group">
              <label for="vote-input">预期评分</label>
              <input 
                id="vote-input"
                type="number" 
                bind:value={formData.vote_average}
                min="0"
                max="10"
                step="0.1"
              />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="year-input">发行年份</label>
              <input 
                id="year-input"
                type="number" 
                bind:value={formData.release_year}
                min="2000"
                max="2030"
              />
            </div>
            <div class="form-group">
              <label for="month-select">发行月份</label>
              <select id="month-select" bind:value={formData.release_month}>
                {#each ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'] as month, i}
                  <option value={i + 1}>{month}</option>
                {/each}
              </select>
            </div>
          </div>
          
          <div class="form-group full-width">
            <span class="label-text">电影类型</span>
            <div class="genre-selector">
              {#each availableGenres as genre}
                <button 
                  type="button"
                  class="genre-tag"
                  class:selected={formData.genres.includes(genre)}
                  onclick={() => toggleGenre(genre)}
                >
                  {genre}
                </button>
              {/each}
            </div>
          </div>
          
          <button type="submit" class="submit-btn" disabled={predicting}>
            {predicting ? '预测中...' : '🎯 预测票房'}
          </button>
        </form>
        
        {#if predictionResult}
          <div class="prediction-result">
            <div class="result-item">
              <div class="result-label">预测票房</div>
              <div class="result-value">{formatCurrency(predictionResult.predicted_revenue)}</div>
            </div>
            <div class="result-item">
              <div class="result-label">预测ROI</div>
              <div class="result-value" class:positive={predictionResult.predicted_roi > 0} class:negative={predictionResult.predicted_roi < 0}>
                {predictionResult.predicted_roi.toFixed(1)}%
              </div>
            </div>
            <div class="result-item">
              <div class="result-label">使用模型</div>
              <div class="result-value small">{predictionResult.model_used}</div>
            </div>
          </div>
        {/if}
      </Card>
      
      <!-- 模型性能 -->
      <Card title="📊 模型性能对比" subtitle="不同算法的预测准确度 (R² Score)">
        <BarChart 
          data={modelComparisonData}
          width={500}
          height={300}
          horizontal
          formatValue={(d) => `${d.toFixed(1)}%`}
          xLabel="R² Score (%)"
        />
        
        {#if insights?.best_model}
          <div class="best-model-badge">
            🏆 最佳模型: {insights.best_model}
          </div>
        {/if}
      </Card>
      
      <!-- 特征重要性 -->
      <Card title="🔑 特征重要性" subtitle="影响票房预测的关键因素">
        <BarChart 
          data={featureImportanceData}
          width={500}
          height={350}
          horizontal
          formatValue={(d) => `${d.toFixed(1)}%`}
          xLabel="重要性 (%)"
        />
      </Card>
      
      <!-- 模型详情 -->
      <Card title="📋 模型评估指标" subtitle="各模型的详细性能指标">
        <div class="metrics-table">
          <table>
            <thead>
              <tr>
                <th>模型</th>
                <th>R² (Log)</th>
                <th>RMSE</th>
                <th>MAE</th>
                <th>CV R² Mean</th>
              </tr>
            </thead>
            <tbody>
              {#each Object.entries(insights?.model_comparison || {}) as [name, metrics]}
                <tr class:best={name === insights?.best_model}>
                  <td class="model-name">
                    {name}
                    {#if name === insights?.best_model}
                      <span class="best-badge">Best</span>
                    {/if}
                  </td>
                  <td>{(metrics.r2_log * 100).toFixed(1)}%</td>
                  <td>{formatCurrency(metrics.rmse)}</td>
                  <td>{formatCurrency(metrics.mae)}</td>
                  <td>{(metrics.cv_r2_mean * 100).toFixed(1)}%</td>
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
  .prediction-page {
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
  
  .content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    gap: 24px;
  }
  
  .error-message {
    text-align: center;
    padding: 40px;
    color: #ef4444;
  }
  
  .prediction-form {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  
  .form-group.full-width {
    grid-column: 1 / -1;
  }
  
  .form-group label,
  .form-group .label-text {
    font-size: 13px;
    font-weight: 500;
    color: #374151;
  }
  
  .form-group input,
  .form-group select {
    padding: 10px 14px;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.2s;
  }
  
  .form-group input:focus,
  .form-group select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  .genre-selector {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .genre-tag {
    padding: 6px 12px;
    border: 1px solid #d1d5db;
    border-radius: 20px;
    background: white;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .genre-tag:hover {
    border-color: #3b82f6;
  }
  
  .genre-tag.selected {
    background: #3b82f6;
    border-color: #3b82f6;
    color: white;
  }
  
  .submit-btn {
    padding: 14px 24px;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
    margin-top: 8px;
  }
  
  .submit-btn:hover {
    background: #2563eb;
  }
  
  .submit-btn:disabled {
    background: #9ca3af;
    cursor: not-allowed;
  }
  
  .prediction-result {
    display: flex;
    gap: 24px;
    margin-top: 24px;
    padding: 20px;
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
    border-radius: 12px;
  }
  
  .result-item {
    flex: 1;
    text-align: center;
  }
  
  .result-label {
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 4px;
  }
  
  .result-value {
    font-size: 24px;
    font-weight: 700;
    color: #111827;
  }
  
  .result-value.small {
    font-size: 14px;
  }
  
  .result-value.positive {
    color: #10b981;
  }
  
  .result-value.negative {
    color: #ef4444;
  }
  
  .best-model-badge {
    margin-top: 16px;
    padding: 12px 20px;
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    border-radius: 8px;
    font-weight: 600;
    text-align: center;
  }
  
  .metrics-table {
    overflow-x: auto;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }
  
  th, td {
    padding: 12px 14px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
  }
  
  th {
    font-weight: 600;
    color: #6b7280;
    background: #f9fafb;
  }
  
  tr.best {
    background: #f0fdf4;
  }
  
  .model-name {
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .best-badge {
    font-size: 10px;
    padding: 2px 6px;
    background: #10b981;
    color: white;
    border-radius: 4px;
  }
</style>
