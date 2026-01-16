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
    background: linear-gradient(150deg, rgba(26, 22, 19, 0.98), rgba(16, 13, 11, 0.98));
    border-radius: 16px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-soft);
    position: relative;
    overflow: hidden;
  }

  .stat-card::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(260px 120px at 0% 0%, rgba(121, 210, 197, 0.2), transparent 70%);
    opacity: 0.5;
    pointer-events: none;
  }
  
  .stat-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: grid;
    place-items: center;
    font-size: 20px;
    color: var(--accent);
    background: rgba(209, 164, 90, 0.2);
    box-shadow: inset 0 0 0 1px rgba(209, 164, 90, 0.4);
    z-index: 1;
  }
  
  .stat-content {
    flex: 1;
    position: relative;
    z-index: 1;
  }
  
  .stat-value {
    font-size: 26px;
    font-weight: 700;
    color: var(--text);
    font-family: var(--font-display);
    line-height: 1.2;
  }
  
  .stat-label {
    font-size: 12px;
    color: var(--muted);
    margin-top: 4px;
  }
  
  .stat-trend {
    font-size: 12px;
    font-weight: 600;
    margin-top: 4px;
    letter-spacing: 0.4px;
  }
  
  .stat-trend.positive {
    color: var(--positive);
  }
  
  .stat-trend.negative {
    color: var(--negative);
  }
</style>
