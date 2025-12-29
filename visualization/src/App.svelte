<script lang="ts">
  import { Overview, RoiAnalysis, Trends, Prediction, Analysis } from './pages';
  
  type PageId = 'overview' | 'roi' | 'trends' | 'prediction' | 'analysis';
  
  let currentPage: PageId = $state('overview');
  
  const navItems: { id: PageId; label: string; icon: string }[] = [
    { id: 'overview', label: '概览', icon: '📊' },
    { id: 'roi', label: 'ROI分析', icon: '💰' },
    { id: 'trends', label: '趋势分析', icon: '📈' },
    { id: 'prediction', label: '票房预测', icon: '🎯' },
    { id: 'analysis', label: '深度分析', icon: '🔍' },
  ];
</script>

<div class="app">
  <nav class="sidebar">
    <div class="logo">
      <span class="logo-icon">🎬</span>
      <span class="logo-text">影视数据分析</span>
    </div>
    
    <ul class="nav-list">
      {#each navItems as item}
        <li>
          <button 
            class="nav-item" 
            class:active={currentPage === item.id}
            onclick={() => currentPage = item.id}
          >
            <span class="nav-icon">{item.icon}</span>
            <span class="nav-label">{item.label}</span>
          </button>
        </li>
      {/each}
    </ul>
    
    <div class="sidebar-footer">
      <div class="data-source">
        <span class="source-label">数据来源</span>
        <span class="source-value">TMDB 5000</span>
      </div>
    </div>
  </nav>
  
  <main class="main-content">
    {#if currentPage === 'overview'}
      <Overview />
    {:else if currentPage === 'roi'}
      <RoiAnalysis />
    {:else if currentPage === 'trends'}
      <Trends />
    {:else if currentPage === 'prediction'}
      <Prediction />
    {:else if currentPage === 'analysis'}
      <Analysis />
    {/if}
  </main>
</div>

<style>
  :global(*) {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  :global(body) {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
                 'Helvetica Neue', Arial, sans-serif;
    background: #f3f4f6;
    color: #111827;
    line-height: 1.5;
  }
  
  .app {
    display: flex;
    min-height: 100vh;
  }
  
  .sidebar {
    width: 240px;
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    color: white;
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 100;
  }
  
  .logo {
    padding: 24px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .logo-icon {
    font-size: 28px;
  }
  
  .logo-text {
    font-size: 16px;
    font-weight: 600;
  }
  
  .nav-list {
    list-style: none;
    padding: 16px 12px;
    flex: 1;
  }
  
  .nav-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    font-weight: 500;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    margin-bottom: 4px;
  }
  
  .nav-item:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }
  
  .nav-item.active {
    background: rgba(59, 130, 246, 0.8);
    color: white;
  }
  
  .nav-icon {
    font-size: 18px;
  }
  
  .sidebar-footer {
    padding: 16px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .data-source {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .source-label {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .source-value {
    font-size: 13px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
  }
  
  .main-content {
    flex: 1;
    margin-left: 240px;
    min-height: 100vh;
    background: #f3f4f6;
  }
</style>
