<script lang="ts">
  import type { Snippet } from 'svelte';
  
  interface Props {
    title: string;
    subtitle?: string;
    children: Snippet;
  }
  
  let { title, subtitle = '', children }: Props = $props();
</script>

<div class="card">
  <div class="card-header">
    <h3 class="card-title">{title}</h3>
    {#if subtitle}
      <p class="card-subtitle">{subtitle}</p>
    {/if}
  </div>
  <div class="card-body">
    {@render children()}
  </div>
</div>

<style>
  .card {
    background: var(--bg-surface);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--color-primary-200);
  }
  
  .card-header {
    padding: 20px 24px;
    border-bottom: 1px solid var(--border-color);
    background: var(--color-gray-50);
  }
  
  .card-title {
    margin: 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
  }
  
  .card-subtitle {
    margin: 4px 0 0;
    font-size: 0.875rem;
    color: var(--text-secondary);
  }
  
  .card-body {
    padding: 24px;
  }
</style>
