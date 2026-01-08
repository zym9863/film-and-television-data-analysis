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
  .app {
    display: flex;
    min-height: 100vh;
    background-color: var(--bg-body);
  }
  
  .sidebar {
    width: 260px;
    background: linear-gradient(180deg, var(--color-gray-900) 0%, #1e1b4b 100%);
    color: var(--text-on-dark);
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 100;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.1);
  }
  
  .logo {
    height: 80px;
    padding: 0 24px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }
  
  .logo-icon {
    font-size: 28px;
    filter: drop-shadow(0 0 8px rgba(99, 102, 241, 0.5));
  }
  
  .logo-text {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.01em;
    background: linear-gradient(to right, #ffffff, #a5b4fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .nav-list {
    list-style: none;
    padding: 24px 16px;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .nav-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border: none;
    background: transparent;
    color: var(--color-gray-400);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    text-align: left;
    position: relative;
    overflow: hidden;
  }
  
  .nav-item:hover {
    background: rgba(255, 255, 255, 0.08);
    color: white;
    transform: translateX(4px);
  }
  
  .nav-item.active {
    background: var(--color-primary-600);
    color: white;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
  }
  
  .nav-icon {
    font-size: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
  }
  
  .nav-label {
    font-size: 15px;
    font-weight: 500;
  }
  
  .sidebar-footer {
    padding: 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(0, 0, 0, 0.2);
  }
  
  .data-source {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .source-label {
    font-size: 11px;
    color: var(--color-gray-500);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
  }
  
  .source-value {
    font-size: 13px;
    font-weight: 600;
    color: var(--color-gray-300);
  }
  
  .main-content {
    flex: 1;
    margin-left: 260px;
    padding: 40px;
    min-height: 100vh;
    animation: fadeIn 0.5s ease-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>
