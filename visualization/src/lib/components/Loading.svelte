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
    border: 4px solid #e5e7eb;
    border-top-color: #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
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
    font-size: 14px;
    color: #6b7280;
  }
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
