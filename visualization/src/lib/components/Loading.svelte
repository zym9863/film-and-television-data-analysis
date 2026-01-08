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
    padding: 60px;
    gap: 20px;
  }
  
  .loader.sm {
    padding: 30px;
    gap: 14px;
  }
  
  .loader.lg {
    padding: 80px;
    gap: 24px;
  }
  
  .spinner {
    width: 48px;
    height: 48px;
    border: 5px solid rgba(59, 130, 246, 0.15);
    border-top-color: #3b82f6;
    border-right-color: #2563eb;
    border-radius: 50%;
    animation: spin 1s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
  }
  
  .sm .spinner {
    width: 28px;
    height: 28px;
    border-width: 3px;
  }
  
  .lg .spinner {
    width: 64px;
    height: 64px;
    border-width: 6px;
  }
  
  .loader-text {
    font-size: 15px;
    font-weight: 600;
    color: #6b7280;
    letter-spacing: 0.5px;
    animation: pulse 2s ease-in-out infinite;
  }
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
  
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.6;
    }
  }
</style>
