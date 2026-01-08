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
    gap: 6px;
    padding: 6px;
    background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
    border-radius: 12px;
    overflow-x: auto;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
  }
  
  .tab {
    padding: 12px 24px;
    border: none;
    background: transparent;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    color: #6b7280;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 8px;
    position: relative;
  }
  
  .tab:hover {
    color: #374151;
    background: rgba(255, 255, 255, 0.6);
    transform: translateY(-2px);
  }
  
  .tab.active {
    background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
    color: #111827;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12), 0 2px 4px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
  }
  
  .tab.active::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 40%;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
    border-radius: 2px;
  }
  
  .tab-icon {
    font-size: 18px;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
  }
</style>
