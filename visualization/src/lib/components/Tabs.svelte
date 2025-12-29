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
    background: #f3f4f6;
    border-radius: 10px;
    overflow-x: auto;
  }
  
  .tab {
    padding: 10px 20px;
    border: none;
    background: transparent;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    color: #6b7280;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  
  .tab:hover {
    color: #374151;
    background: rgba(255, 255, 255, 0.5);
  }
  
  .tab.active {
    background: white;
    color: #111827;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .tab-icon {
    font-size: 16px;
  }
</style>
