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
    gap: 20px;
    padding: 24px;
    background: var(--bg-surface);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .stat-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--color-primary-200);
  }
  
  .stat-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    font-size: 28px;
    background: var(--color-primary-50);
    border-radius: var(--radius-xl);
    /* 假设 icon 是 emoji，如果后续变为 SVG 可能需要不同处理，这里先通过 font-size 控制 */
    line-height: 1;
  }
  
  .stat-content {
    flex: 1;
  }
  
  .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
    letter-spacing: -0.02em;
  }
  
  .stat-label {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-secondary);
    margin-top: 4px;
  }
  
  .stat-trend {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 8px;
    padding: 2px 8px;
    border-radius: 9999px;
    background: var(--color-gray-50);
  }
  
  .stat-trend.positive {
    color: var(--color-success);
    background: rgba(16, 185, 129, 0.1);
  }
  
  .stat-trend.negative {
    color: var(--color-danger);
    background: rgba(239, 68, 68, 0.1);
  }
</style>
