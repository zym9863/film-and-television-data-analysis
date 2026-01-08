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
    gap: 18px;
    padding: 24px;
    background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
    border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 
                0 2px 4px rgba(0, 0, 0, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(229, 231, 235, 0.6);
    position: relative;
    overflow: hidden;
  }
  
  .stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .stat-card:hover {
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12), 
                0 6px 12px rgba(0, 0, 0, 0.08);
    transform: translateY(-4px);
    border-color: rgba(59, 130, 246, 0.3);
  }
  
  .stat-card:hover::before {
    transform: scaleX(1);
  }
  
  .stat-icon {
    font-size: 36px;
    opacity: 0.9;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
    animation: float 3s ease-in-out infinite;
  }
  
  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
  }
  
  .stat-content {
    flex: 1;
  }
  
  .stat-value {
    font-size: 30px;
    font-weight: 800;
    color: #111827;
    line-height: 1.2;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .stat-label {
    font-size: 13px;
    color: #6b7280;
    margin-top: 6px;
    font-weight: 500;
    letter-spacing: 0.3px;
  }
  
  .stat-trend {
    font-size: 13px;
    font-weight: 700;
    margin-top: 6px;
    padding: 4px 10px;
    border-radius: 6px;
    display: inline-block;
    letter-spacing: 0.3px;
  }
  
  .stat-trend.positive {
    color: #059669;
    background: rgba(16, 185, 129, 0.1);
  }
  
  .stat-trend.negative {
    color: #dc2626;
    background: rgba(239, 68, 68, 0.1);
  }
</style>
