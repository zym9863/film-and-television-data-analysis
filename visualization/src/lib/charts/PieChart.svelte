<script lang="ts">
  import * as d3 from 'd3';
  
  interface PieData {
    label: string;
    value: number;
    color?: string;
  }
  
  interface Props {
    data: PieData[];
    width?: number;
    height?: number;
    innerRadius?: number;
    showLabels?: boolean;
    showLegend?: boolean;
  }
  
  let {
    data,
    width = 400,
    height = 400,
    innerRadius = 0,
    showLabels = true,
    showLegend = true
  }: Props = $props();
  
  let svgElement: SVGSVGElement;
  let tooltipElement: HTMLDivElement;
  
  const colors = [
    '#d1a45a', '#79d2c5', '#f0d7a7', '#ff7a7a', '#8ab4f8',
    '#c58bd3', '#f2b87a', '#7aa7ff', '#9ad48f', '#f4a3a3',
    '#d6b37e', '#8cd6b1', '#f5c784', '#d38cff', '#6fbbe3'
  ];
  
  $effect(() => {
    if (!svgElement || !data || data.length === 0) return;
    
    d3.select(svgElement).selectAll('*').remove();
    
    const svg = d3.select(svgElement);
    const legendWidth = showLegend ? 150 : 0;
    const chartWidth = width - legendWidth;
    const radius = Math.min(chartWidth, height) / 2 - 10;
    
    const g = svg.append('g')
      .attr('transform', `translate(${chartWidth / 2},${height / 2})`);
    
    // 颜色比例尺
    const colorScale = d3.scaleOrdinal<string>()
      .domain(data.map(d => d.label))
      .range(colors);
    
    // 饼图布局
    const pie = d3.pie<PieData>()
      .value(d => d.value)
      .sort(null);
    
    const arc = d3.arc<d3.PieArcDatum<PieData>>()
      .innerRadius(innerRadius)
      .outerRadius(radius);
    
    const labelArc = d3.arc<d3.PieArcDatum<PieData>>()
      .innerRadius(radius * 0.7)
      .outerRadius(radius * 0.7);
    
    // 计算总和
    const total = d3.sum(data, d => d.value);
    
    // 绘制扇形
    const arcs = g.selectAll('.arc')
      .data(pie(data))
      .join('g')
      .attr('class', 'arc');
    
    arcs.append('path')
      .attr('d', arc)
      .attr('fill', d => d.data.color || colorScale(d.data.label))
      .style('cursor', 'pointer')
      .style('stroke', 'rgba(15, 12, 10, 0.85)')
      .style('stroke-width', 1.5)
      .on('mouseover', function(event, d) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('transform', function() {
            const centroid = arc.centroid(d);
            return `translate(${centroid[0] * 0.05},${centroid[1] * 0.05})`;
          });
        
        if (tooltipElement) {
          const percent = ((d.data.value / total) * 100).toFixed(1);
          tooltipElement.style.display = 'block';
          tooltipElement.style.left = `${event.pageX + 10}px`;
          tooltipElement.style.top = `${event.pageY - 10}px`;
          tooltipElement.innerHTML = `
            <strong>${d.data.label}</strong><br/>
            Value: ${d.data.value.toLocaleString()}<br/>
            Percent: ${percent}%
          `;
        }
      })
      .on('mouseout', function() {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('transform', 'translate(0,0)');
        
        if (tooltipElement) {
          tooltipElement.style.display = 'none';
        }
      });
    
    // 标签
    if (showLabels) {
      arcs.append('text')
        .attr('transform', d => `translate(${labelArc.centroid(d)})`)
        .attr('text-anchor', 'middle')
        .style('font-size', '11px')
        .style('fill', '#f7f2e9')
        .style('font-weight', 'bold')
        .style('pointer-events', 'none')
        .text(d => {
          const percent = (d.data.value / total) * 100;
          return percent > 5 ? `${percent.toFixed(0)}%` : '';
        });
    }
    
    // 图例
    if (showLegend) {
      const legend = svg.append('g')
        .attr('transform', `translate(${chartWidth + 10},${20})`);
      
      const legendItems = legend.selectAll('.legend-item')
        .data(data)
        .join('g')
        .attr('class', 'legend-item')
        .attr('transform', (_, i) => `translate(0,${i * 22})`);
      
      legendItems.append('rect')
        .attr('width', 14)
        .attr('height', 14)
        .attr('rx', 3)
        .attr('fill', d => d.color || colorScale(d.label));
      
      legendItems.append('text')
        .attr('x', 20)
        .attr('y', 11)
        .style('font-size', '11px')
        .style('fill', 'rgba(247, 242, 233, 0.7)')
        .text(d => {
          const label = d.label.length > 15 ? d.label.substring(0, 15) + '...' : d.label;
          return label;
        });
    }
  });
</script>

<div class="pie-container">
  <svg bind:this={svgElement} {width} {height}></svg>
  <div 
    bind:this={tooltipElement} 
    class="tooltip"
    style="display: none; position: fixed; pointer-events: none;"
  ></div>
</div>

<style>
  .pie-container {
    position: relative;
  }
  
  .tooltip {
    background: rgba(17, 14, 12, 0.95);
    color: #f7f2e9;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 12px;
    z-index: 1000;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(209, 164, 90, 0.3);
  }
</style>
