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
      <div class="logo-mark">🎬</div>
      <div class="logo-text">
        <span class="logo-title">影视数据分析</span>
        <span class="logo-subtitle">CINEMA INTEL</span>
      </div>
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
      <div class="source-tag">Data Studio</div>
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
    line-height: 1.6;
  }
  
  .app {
    display: flex;
    min-height: 100vh;
    position: relative;
  }
  
  .sidebar {
    width: 260px;
    background: linear-gradient(180deg, #14110e 0%, #0c0a08 100%);
    color: var(--text);
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 100;
    border-right: 1px solid rgba(209, 164, 90, 0.14);
    box-shadow: 20px 0 50px rgba(0, 0, 0, 0.35);
  }
  
  .sidebar::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(400px 220px at 15% 0%, rgba(209, 164, 90, 0.25), transparent 70%);
    pointer-events: none;
  }
  
  .logo {
    padding: 24px 22px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    border-bottom: 1px solid rgba(209, 164, 90, 0.15);
    position: relative;
    z-index: 1;
  }
  
  .logo-mark {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: rgba(209, 164, 90, 0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: var(--shadow-soft);
  }
  
  .logo-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  
  .logo-title {
    font-family: var(--font-display);
    font-size: 18px;
    letter-spacing: 0.5px;
  }
  
  .logo-subtitle {
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
  }
  
  .nav-list {
    list-style: none;
    padding: 18px 14px;
    flex: 1;
    position: relative;
    z-index: 1;
  }
  
  .nav-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border: 1px solid transparent;
    background: transparent;
    color: var(--muted);
    font-size: 14px;
    font-weight: 500;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    margin-bottom: 6px;
    position: relative;
  }
  
  .nav-item::before {
    content: "";
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    width: 3px;
    height: 18px;
    border-radius: 4px;
    background: var(--accent);
    opacity: 0;
  }
  
  .nav-item:hover {
    border-color: rgba(209, 164, 90, 0.25);
    color: var(--text);
  }
  
  .nav-item.active {
    background: rgba(209, 164, 90, 0.14);
    border-color: rgba(209, 164, 90, 0.35);
    color: var(--text);
    box-shadow: var(--shadow-soft);
  }
  
  .nav-item.active::before {
    opacity: 1;
  }
  
  .nav-icon {
    font-size: 18px;
  }
  
  .sidebar-footer {
    padding: 16px 20px 22px;
    border-top: 1px solid rgba(209, 164, 90, 0.16);
    display: flex;
    flex-direction: column;
    gap: 10px;
    position: relative;
    z-index: 1;
  }
  
  .data-source {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .source-label {
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .source-value {
    font-size: 13px;
    font-weight: 600;
    color: var(--text);
  }
  
  .source-tag {
    align-self: flex-start;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid rgba(209, 164, 90, 0.3);
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--accent);
  }
  
  .main-content {
    flex: 1;
    margin-left: 260px;
    min-height: 100vh;
    padding: 28px 32px 40px;
    position: relative;
  }
  
  @media (max-width: 960px) {
    .app {
      flex-direction: column;
    }
    
    .sidebar {
      position: relative;
      width: 100%;
      height: auto;
    }
    
    .main-content {
      margin-left: 0;
      padding: 24px 18px 32px;
    }
  }
</style>
