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
                 'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif;
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ebf0 100%);
    color: #111827;
    line-height: 1.6;
  }
  
  .app {
    display: flex;
    min-height: 100vh;
  }
  
  .sidebar {
    width: 260px;
    background: linear-gradient(180deg, #1e3a8a 0%, #1e293b 50%, #0f172a 100%);
    color: white;
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 100;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  }
  
  .logo {
    padding: 28px 24px;
    display: flex;
    align-items: center;
    gap: 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(255, 255, 255, 0.05);
  }
  
  .logo-icon {
    font-size: 32px;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
    animation: pulse 3s ease-in-out infinite;
  }
  
  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }
  
  .logo-text {
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }
  
  .nav-list {
    list-style: none;
    padding: 20px 14px;
    flex: 1;
  }
  
  .nav-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.75);
    font-size: 14px;
    font-weight: 500;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-align: left;
    margin-bottom: 6px;
    position: relative;
    overflow: hidden;
  }
  
  .nav-item::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 3px;
    background: linear-gradient(to bottom, #3b82f6, #2563eb);
    transform: scaleY(0);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .nav-item:hover {
    background: rgba(255, 255, 255, 0.15);
    color: white;
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }
  
  .nav-item:hover::before {
    transform: scaleY(1);
  }
  
  .nav-item.active {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.9) 0%, rgba(37, 99, 235, 0.8) 100%);
    color: white;
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
    transform: translateX(4px);
  }
  
  .nav-item.active::before {
    transform: scaleY(1);
  }
  
  .nav-icon {
    font-size: 20px;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
  }
  
  .sidebar-footer {
    padding: 20px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(0, 0, 0, 0.15);
  }
  
  .data-source {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    border-left: 3px solid #3b82f6;
  }
  
  .source-label {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.6);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
  }
  
  .source-value {
    font-size: 14px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    letter-spacing: 0.3px;
  }
  
  .main-content {
    flex: 1;
    margin-left: 260px;
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ebf0 100%);
  }
</style>
