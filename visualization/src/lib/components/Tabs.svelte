<script lang="ts">
  interface Tab {
    id: string;
    label: string;
    icon?: string;
  }
  
  interface Props {
    tabs: Tab[];
    activeTab: string;
    onTabChange: (tabId: string) => void;
  }
  
  let { tabs, activeTab, onTabChange }: Props = $props();
</script>

<div class="tabs">
  {#each tabs as tab}
    <button 
      class="tab" 
      class:active={activeTab === tab.id}
      onclick={() => onTabChange(tab.id)}
    >
      {#if tab.icon}
        <span class="tab-icon">{tab.icon}</span>
      {/if}
      {tab.label}
    </button>
  {/each}
</div>

<style>
  .tabs {
    display: flex;
    gap: 4px;
    padding: 4px;
    background: var(--color-gray-100);
    border-radius: var(--radius-lg);
    overflow-x: auto;
    /* 隐藏滚动条 */
    scrollbar-width: none; 
    border: 1px solid var(--border-color);
  }
  
  .tabs::-webkit-scrollbar {
    display: none;
  }
  
  .tab {
    padding: 8px 16px;
    border: none;
    background: transparent;
    border-radius: var(--radius-md);
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .tab:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.5);
  }
  
  .tab.active {
    background: var(--bg-surface);
    color: var(--color-primary-600);
    box-shadow: var(--shadow-sm);
    font-weight: 600;
  }
  
  .tab-icon {
    font-size: 1.1em;
  }
</style>
