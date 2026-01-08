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
    border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 
                0 2px 4px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(229, 231, 235, 0.6);
  }
  
  .card:hover {
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12), 
                0 6px 12px rgba(0, 0, 0, 0.08);
    transform: translateY(-4px);
    border-color: rgba(59, 130, 246, 0.3);
  }
  
  .card-header {
    padding: 20px 24px;
    border-bottom: 1px solid #e5e7eb;
    background: linear-gradient(to right, rgba(59, 130, 246, 0.03), rgba(147, 197, 253, 0.03));
  }
  
  .card-title {
    margin: 0;
    font-size: 17px;
    font-weight: 700;
    color: #111827;
    letter-spacing: 0.2px;
  }
  
  .card-subtitle {
    margin: 6px 0 0;
    font-size: 13px;
    color: #6b7280;
    line-height: 1.5;
  }
  
  .card-body {
    padding: 24px;
  }
</style>
