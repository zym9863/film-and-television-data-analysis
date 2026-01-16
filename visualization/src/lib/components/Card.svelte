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
    background: linear-gradient(160deg, rgba(27, 23, 20, 0.98), rgba(16, 13, 11, 0.98));
    border-radius: 16px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-soft);
    overflow: hidden;
    position: relative;
  }

  .card::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(420px 180px at 10% -10%, rgba(209, 164, 90, 0.22), transparent 70%);
    opacity: 0.8;
    pointer-events: none;
  }
  
  .card-header {
    padding: 18px 22px 16px;
    border-bottom: 1px solid rgba(209, 164, 90, 0.12);
    position: relative;
    z-index: 1;
  }
  
  .card-title {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: var(--text);
    font-family: var(--font-display);
    letter-spacing: 0.4px;
  }
  
  .card-subtitle {
    margin: 6px 0 0;
    font-size: 12px;
    color: var(--muted);
    letter-spacing: 0.3px;
  }
  
  .card-body {
    padding: 22px;
    position: relative;
    z-index: 1;
  }
</style>
