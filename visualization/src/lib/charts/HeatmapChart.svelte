<script lang="ts">
  import * as d3 from 'd3';
  
  interface HeatmapData {
    x: string;
    y: string;
    value: number;
  }
  
  interface Props {
    data: HeatmapData[];
    width?: number;
    height?: number;
    marginTop?: number;
    marginRight?: number;
    marginBottom?: number;
    marginLeft?: number;
    colorRange?: [string, string, string];
  }
  
  let {
    data,
    width = 500,
    height = 500,
    marginTop = 30,
    marginRight = 80,
    marginBottom = 80,
    marginLeft = 100,
    colorRange = ['#ef4444', '#fef3c7', '#10b981']
  }: Props = $props();
  
  let svgElement: SVGSVGElement;
  let tooltipElement: HTMLDivElement;
  
  $effect(() => {
    if (!svgElement || !data || data.length === 0) return;
    
    d3.select(svgElement).selectAll('*').remove();
    
    const svg = d3.select(svgElement);
    const innerWidth = width - marginLeft - marginRight;
    const innerHeight = height - marginTop - marginBottom;
    
    const g = svg.append('g')
      .attr('transform', `translate(${marginLeft},${marginTop})`);
    
    // 获取唯一的x和y值
    const xLabels = [...new Set(data.map(d => d.x))];
    const yLabels = [...new Set(data.map(d => d.y))];
    
    // 比例尺
    const x = d3.scaleBand()
      .domain(xLabels)
      .range([0, innerWidth])
      .padding(0.05);
    
    const y = d3.scaleBand()
      .domain(yLabels)
      .range([0, innerHeight])
      .padding(0.05);
    
    // 颜色比例尺
    const valueExtent = d3.extent(data, d => d.value) as [number, number];
    const colorScale = d3.scaleLinear<string>()
      .domain([valueExtent[0], 0, valueExtent[1]])
      .range(colorRange);
    
    // X轴
    g.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .attr('transform', 'rotate(-45)')
      .style('text-anchor', 'end')
      .style('font-size', '10px');
    
    // Y轴
    g.append('g')
      .call(d3.axisLeft(y))
      .selectAll('text')
      .style('font-size', '10px');
    
    // 热力图格子
    g.selectAll('.cell')
      .data(data)
      .join('rect')
      .attr('class', 'cell')
      .attr('x', d => x(d.x) || 0)
      .attr('y', d => y(d.y) || 0)
      .attr('width', x.bandwidth())
      .attr('height', y.bandwidth())
      .attr('fill', d => colorScale(d.value))
      .attr('rx', 2)
      .style('cursor', 'pointer')
      .on('mouseover', function(event, d) {
        d3.select(this).style('stroke', '#000').style('stroke-width', 2);
        
        if (tooltipElement) {
          tooltipElement.style.display = 'block';
          tooltipElement.style.left = `${event.pageX + 10}px`;
          tooltipElement.style.top = `${event.pageY - 10}px`;
          tooltipElement.innerHTML = `
            <strong>${d.x} vs ${d.y}</strong><br/>
            Correlation: ${d.value.toFixed(3)}
          `;
        }
      })
      .on('mouseout', function() {
        d3.select(this).style('stroke', 'none');
        if (tooltipElement) {
          tooltipElement.style.display = 'none';
        }
      });
    
    // 数值标签
    g.selectAll('.label')
      .data(data)
      .join('text')
      .attr('class', 'label')
      .attr('x', d => (x(d.x) || 0) + x.bandwidth() / 2)
      .attr('y', d => (y(d.y) || 0) + y.bandwidth() / 2)
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .style('font-size', '9px')
      .style('fill', d => Math.abs(d.value) > 0.5 ? 'white' : '#333')
      .text(d => d.value.toFixed(2));
    
    // 颜色图例
    const legendWidth = 20;
    const legendHeight = innerHeight;
    
    const legendScale = d3.scaleLinear()
      .domain(valueExtent)
      .range([legendHeight, 0]);
    
    const legendAxis = d3.axisRight(legendScale).ticks(5);
    
    const legend = svg.append('g')
      .attr('transform', `translate(${width - marginRight + 20},${marginTop})`);
    
    // 渐变
    const defs = svg.append('defs');
    const gradient = defs.append('linearGradient')
      .attr('id', 'heatmap-gradient')
      .attr('x1', '0%')
      .attr('y1', '100%')
      .attr('x2', '0%')
      .attr('y2', '0%');
    
    gradient.append('stop')
      .attr('offset', '0%')
      .attr('stop-color', colorRange[0]);
    
    gradient.append('stop')
      .attr('offset', '50%')
      .attr('stop-color', colorRange[1]);
    
    gradient.append('stop')
      .attr('offset', '100%')
      .attr('stop-color', colorRange[2]);
    
    legend.append('rect')
      .attr('width', legendWidth)
      .attr('height', legendHeight)
      .style('fill', 'url(#heatmap-gradient)');
    
    legend.append('g')
      .attr('transform', `translate(${legendWidth},0)`)
      .call(legendAxis)
      .selectAll('text')
      .style('font-size', '10px');
  });
</script>

<div class="heatmap-container">
  <svg bind:this={svgElement} {width} {height}></svg>
  <div 
    bind:this={tooltipElement} 
    class="tooltip"
    style="display: none; position: fixed; pointer-events: none;"
  ></div>
</div>

<style>
  .heatmap-container {
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
