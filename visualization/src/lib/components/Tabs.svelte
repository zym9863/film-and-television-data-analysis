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
    gap: 8px;
    padding: 6px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 999px;
    border: 1px solid var(--border);
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.04);
    overflow-x: auto;
  }
  
  .tab {
    padding: 10px 18px;
    border: 1px solid transparent;
    background: transparent;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 500;
    color: var(--muted);
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  
  .tab:hover {
    color: var(--text);
    border-color: rgba(209, 164, 90, 0.25);
  }
  
  .tab.active {
    background: linear-gradient(135deg, #e7c685, #d1a45a);
    color: #1b1309;
    box-shadow: var(--shadow-soft);
    border-color: rgba(209, 164, 90, 0.6);
    font-weight: 600;
  }
  
  .tab-icon {
    font-size: 15px;
  }
</style>
