/**
 * 工具函数模块
 */

/**
 * 格式化数字为货币格式
 */
export function formatCurrency(value: number, decimals = 0): string {
  if (value >= 1e9) {
    return `$${(value / 1e9).toFixed(decimals)}B`;
  } else if (value >= 1e6) {
    return `$${(value / 1e6).toFixed(decimals)}M`;
  } else if (value >= 1e3) {
    return `$${(value / 1e3).toFixed(decimals)}K`;
  }
  return `$${value.toFixed(decimals)}`;
}

/**
 * 格式化百分比
 */
export function formatPercent(value: number, decimals = 1): string {
  return `${value.toFixed(decimals)}%`;
}

/**
 * 格式化数字（带千分位）
 */
export function formatNumber(value: number, decimals = 0): string {
  return value.toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

/**
 * 颜色比例尺
 */
export const colors = {
  primary: '#3b82f6',
  secondary: '#10b981',
  warning: '#f59e0b',
  danger: '#ef4444',
  info: '#6366f1',
  
  // 渐变色
  gradient: [
    '#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', 
    '#d946ef', '#ec4899', '#f43f5e', '#ef4444'
  ],
  
  // 类型颜色
  genres: [
    '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6366f1',
    '#ec4899', '#14b8a6', '#f97316', '#8b5cf6', '#06b6d4',
    '#84cc16', '#eab308', '#22c55e', '#a855f7', '#0ea5e9'
  ],
  
  // 正负色
  positive: '#10b981',
  negative: '#ef4444',
};

/**
 * 获取类型颜色
 */
export function getGenreColor(index: number): string {
  return colors.genres[index % colors.genres.length];
}

/**
 * 根据值获取颜色（正负）
 */
export function getValueColor(value: number): string {
  return value >= 0 ? colors.positive : colors.negative;
}

/**
 * 防抖函数
 */
export function debounce<T extends (...args: unknown[]) => unknown>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

/**
 * 计算数据范围
 */
export function getDataRange(data: number[]): { min: number; max: number } {
  return {
    min: Math.min(...data),
    max: Math.max(...data),
  };
}
