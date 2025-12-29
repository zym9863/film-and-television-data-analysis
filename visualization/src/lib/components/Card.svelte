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
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
    overflow: hidden;
  }
  
  .card-header {
    padding: 16px 20px;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .card-title {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: #111827;
  }
  
  .card-subtitle {
    margin: 4px 0 0;
    font-size: 13px;
    color: #6b7280;
  }
  
  .card-body {
    padding: 20px;
  }
</style>
