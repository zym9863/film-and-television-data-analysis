<script lang="ts">
  interface Props {
    value: number | string;
    label: string;
    format?: 'number' | 'currency' | 'percent';
    trend?: number;
    icon?: string;
  }
  
  let { value, label, format = 'number', trend, icon }: Props = $props();
  
  function formatValue(val: number | string): string {
    if (typeof val === 'string') return val;
    
    switch (format) {
      case 'currency':
        if (val >= 1e9) return `$${(val / 1e9).toFixed(1)}B`;
        if (val >= 1e6) return `$${(val / 1e6).toFixed(1)}M`;
        if (val >= 1e3) return `$${(val / 1e3).toFixed(1)}K`;
        return `$${val.toFixed(0)}`;
      case 'percent':
        return `${val.toFixed(1)}%`;
      default:
        return val.toLocaleString();
    }
  }
</script>

<div class="stat-card">
  {#if icon}
    <div class="stat-icon">{icon}</div>
  {/if}
  <div class="stat-content">
    <div class="stat-value">{formatValue(value)}</div>
    <div class="stat-label">{label}</div>
    {#if trend !== undefined}
      <div class="stat-trend" class:positive={trend >= 0} class:negative={trend < 0}>
        {trend >= 0 ? '↑' : '↓'} {Math.abs(trend).toFixed(1)}%
      </div>
    {/if}
  </div>
</div>

<style>
  .stat-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .stat-icon {
    font-size: 32px;
    opacity: 0.8;
  }
  
  .stat-content {
    flex: 1;
  }
  
  .stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #111827;
    line-height: 1.2;
  }
  
  .stat-label {
    font-size: 13px;
    color: #6b7280;
    margin-top: 4px;
  }
  
  .stat-trend {
    font-size: 12px;
    font-weight: 600;
    margin-top: 4px;
  }
  
  .stat-trend.positive {
    color: #10b981;
  }
  
  .stat-trend.negative {
    color: #ef4444;
  }
</style>
