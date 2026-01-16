<script lang="ts">
  interface Props {
    loading?: boolean;
    size?: 'sm' | 'md' | 'lg';
  }
  
  let { loading = true, size = 'md' }: Props = $props();
</script>

{#if loading}
  <div class="loader" class:sm={size === 'sm'} class:lg={size === 'lg'}>
    <div class="spinner"></div>
    <span class="loader-text">加载中...</span>
  </div>
{/if}

<style>
  .loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    gap: 16px;
  }
  
  .loader.sm {
    padding: 20px;
    gap: 12px;
  }
  
  .loader.lg {
    padding: 60px;
    gap: 20px;
  }
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(209, 164, 90, 0.18);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    box-shadow: 0 0 18px rgba(209, 164, 90, 0.35);
  }
  
  .sm .spinner {
    width: 24px;
    height: 24px;
    border-width: 3px;
  }
  
  .lg .spinner {
    width: 56px;
    height: 56px;
    border-width: 5px;
  }
  
  .loader-text {
    font-size: 12px;
    color: var(--muted);
    letter-spacing: 1.5px;
    font-family: var(--font-mono);
    text-transform: uppercase;
  }
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
