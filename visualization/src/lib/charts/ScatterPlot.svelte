<script lang="ts">
  import * as d3 from 'd3';
  
  interface ScatterData {
    x: number;
    y: number;
    label?: string;
    category?: string;
    size?: number;
  }
  
  interface Props {
    data: ScatterData[];
    width?: number;
    height?: number;
    marginTop?: number;
    marginRight?: number;
    marginBottom?: number;
    marginLeft?: number;
    xLabel?: string;
    yLabel?: string;
    formatX?: (d: number) => string;
    formatY?: (d: number) => string;
    showTrendLine?: boolean;
  }
  
  let {
    data,
    width = 600,
    height = 400,
    marginTop = 30,
    marginRight = 30,
    marginBottom = 50,
    marginLeft = 80,
    xLabel = '',
    yLabel = '',
    formatX = (d: number) => d.toLocaleString(),
    formatY = (d: number) => d.toLocaleString(),
    showTrendLine = true
  }: Props = $props();
  
  let svgElement: SVGSVGElement;
  let tooltipElement: HTMLDivElement;
  
  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6366f1'];
  
  $effect(() => {
    if (!svgElement || !data || data.length === 0) return;
    
    d3.select(svgElement).selectAll('*').remove();
    
    const svg = d3.select(svgElement);
    const innerWidth = width - marginLeft - marginRight;
    const innerHeight = height - marginTop - marginBottom;
    
    const g = svg.append('g')
      .attr('transform', `translate(${marginLeft},${marginTop})`);
    
    // 比例尺
    const xExtent = d3.extent(data, d => d.x) as [number, number];
    const yExtent = d3.extent(data, d => d.y) as [number, number];
    
    const x = d3.scaleLinear()
      .domain([0, xExtent[1] * 1.05])
      .range([0, innerWidth]);
    
    const y = d3.scaleLinear()
      .domain([0, yExtent[1] * 1.05])
      .range([innerHeight, 0]);
    
    // 网格线
    g.append('g')
      .attr('class', 'grid')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).tickSize(-innerHeight).tickFormat(() => ''))
      .selectAll('line')
      .style('stroke', '#e5e7eb')
      .style('stroke-dasharray', '3,3');
    
    g.append('g')
      .attr('class', 'grid')
      .call(d3.axisLeft(y).tickSize(-innerWidth).tickFormat(() => ''))
      .selectAll('line')
      .style('stroke', '#e5e7eb')
      .style('stroke-dasharray', '3,3');
    
    // X轴
    g.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).ticks(6).tickFormat(d => formatX(d as number)))
      .selectAll('text')
      .style('font-size', '11px');
    
    // Y轴
    g.append('g')
      .call(d3.axisLeft(y).ticks(6).tickFormat(d => formatY(d as number)))
      .selectAll('text')
      .style('font-size', '11px');
    
    // 趋势线
    if (showTrendLine && data.length > 1) {
      const xMean = d3.mean(data, d => d.x) || 0;
      const yMean = d3.mean(data, d => d.y) || 0;
      
      let num = 0;
      let den = 0;
      for (const d of data) {
        num += (d.x - xMean) * (d.y - yMean);
        den += (d.x - xMean) ** 2;
      }
      
      const slope = den !== 0 ? num / den : 0;
      const intercept = yMean - slope * xMean;
      
      const x1 = xExtent[0];
      const x2 = xExtent[1];
      const y1 = slope * x1 + intercept;
      const y2 = slope * x2 + intercept;
      
      g.append('line')
        .attr('x1', x(x1))
        .attr('y1', y(y1))
        .attr('x2', x(x2))
        .attr('y2', y(y2))
        .style('stroke', '#ef4444')
        .style('stroke-width', 2)
        .style('stroke-dasharray', '5,5')
        .style('opacity', 0.7);
    }
    
    // 散点
    const categories = [...new Set(data.map(d => d.category).filter(Boolean))];
    const colorScale = d3.scaleOrdinal<string>()
      .domain(categories as string[])
      .range(colors);
    
    g.selectAll('.dot')
      .data(data)
      .join('circle')
      .attr('class', 'dot')
      .attr('cx', d => x(d.x))
      .attr('cy', d => y(d.y))
      .attr('r', d => d.size || 5)
      .style('fill', d => d.category ? colorScale(d.category) : colors[0])
      .style('opacity', 0.7)
      .style('cursor', 'pointer')
      .on('mouseover', function(event, d) {
        d3.select(this)
          .style('opacity', 1)
          .attr('r', (d.size || 5) + 2);
        
        if (tooltipElement) {
          tooltipElement.style.display = 'block';
          tooltipElement.style.left = `${event.pageX + 10}px`;
          tooltipElement.style.top = `${event.pageY - 10}px`;
          tooltipElement.innerHTML = `
            <strong>${d.label || 'Data Point'}</strong><br/>
            X: ${formatX(d.x)}<br/>
            Y: ${formatY(d.y)}
          `;
        }
      })
      .on('mouseout', function(_, d) {
        d3.select(this)
          .style('opacity', 0.7)
          .attr('r', d.size || 5);
        
        if (tooltipElement) {
          tooltipElement.style.display = 'none';
        }
      });
    
    // X轴标签
    if (xLabel) {
      svg.append('text')
        .attr('x', width / 2)
        .attr('y', height - 5)
        .attr('text-anchor', 'middle')
        .style('font-size', '13px')
        .style('fill', '#666')
        .text(xLabel);
    }
    
    // Y轴标签
    if (yLabel) {
      svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', 15)
        .attr('text-anchor', 'middle')
        .style('font-size', '13px')
        .style('fill', '#666')
        .text(yLabel);
    }
  });
</script>

<div class="scatter-container">
  <svg bind:this={svgElement} {width} {height}></svg>
  <div 
    bind:this={tooltipElement} 
    class="tooltip"
    style="display: none; position: fixed; pointer-events: none;"
  ></div>
</div>

<style>
  .scatter-container {
    position: relative;
  }
  
  .tooltip {
    background: rgba(0, 0, 0, 0.85);
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    z-index: 1000;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }
</style>
