<script lang="ts">
  import * as d3 from 'd3';
  
  interface BarData {
    label: string;
    value: number;
    color?: string;
  }
  
  interface Props {
    data: BarData[];
    width?: number;
    height?: number;
    marginTop?: number;
    marginRight?: number;
    marginBottom?: number;
    marginLeft?: number;
    xLabel?: string;
    yLabel?: string;
    horizontal?: boolean;
    formatValue?: (d: number) => string;
  }
  
  let {
    data,
    width = 600,
    height = 400,
    marginTop = 30,
    marginRight = 30,
    marginBottom = 60,
    marginLeft = 80,
    xLabel = '',
    yLabel = '',
    horizontal = false,
    formatValue = (d: number) => d.toLocaleString()
  }: Props = $props();
  
  let svgElement: SVGSVGElement;
  
  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6366f1', 
                  '#ec4899', '#14b8a6', '#f97316', '#8b5cf6', '#06b6d4'];
  
  $effect(() => {
    if (!svgElement || !data || data.length === 0) return;
    
    // 清除之前的内容
    d3.select(svgElement).selectAll('*').remove();
    
    const svg = d3.select(svgElement);
    const innerWidth = width - marginLeft - marginRight;
    const innerHeight = height - marginTop - marginBottom;
    
    const g = svg.append('g')
      .attr('transform', `translate(${marginLeft},${marginTop})`);
    
    if (horizontal) {
      // 水平条形图
      const x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value) || 0])
        .range([0, innerWidth]);
      
      const y = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([0, innerHeight])
        .padding(0.2);
      
      // X轴
      g.append('g')
        .attr('transform', `translate(0,${innerHeight})`)
        .call(d3.axisBottom(x).ticks(5).tickFormat(d => formatValue(d as number)))
        .selectAll('text')
        .style('font-size', '12px');
      
      // Y轴
      g.append('g')
        .call(d3.axisLeft(y))
        .selectAll('text')
        .style('font-size', '12px');
      
      // 条形
      g.selectAll('.bar')
        .data(data)
        .join('rect')
        .attr('class', 'bar')
        .attr('y', d => y(d.label) || 0)
        .attr('height', y.bandwidth())
        .attr('x', 0)
        .attr('width', 0)
        .attr('fill', (d, i) => d.color || colors[i % colors.length])
        .attr('rx', 4)
        .transition()
        .duration(800)
        .attr('width', d => x(d.value));
      
      // 数值标签
      g.selectAll('.value-label')
        .data(data)
        .join('text')
        .attr('class', 'value-label')
        .attr('y', d => (y(d.label) || 0) + y.bandwidth() / 2)
        .attr('x', d => x(d.value) + 5)
        .attr('dy', '0.35em')
        .style('font-size', '11px')
        .style('fill', '#666')
        .text(d => formatValue(d.value));
        
    } else {
      // 垂直条形图
      const x = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([0, innerWidth])
        .padding(0.2);
      
      const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value) || 0])
        .range([innerHeight, 0]);
      
      // X轴
      g.append('g')
        .attr('transform', `translate(0,${innerHeight})`)
        .call(d3.axisBottom(x))
        .selectAll('text')
        .attr('transform', 'rotate(-45)')
        .style('text-anchor', 'end')
        .style('font-size', '11px');
      
      // Y轴
      g.append('g')
        .call(d3.axisLeft(y).ticks(5).tickFormat(d => formatValue(d as number)))
        .selectAll('text')
        .style('font-size', '12px');
      
      // 条形
      g.selectAll('.bar')
        .data(data)
        .join('rect')
        .attr('class', 'bar')
        .attr('x', d => x(d.label) || 0)
        .attr('width', x.bandwidth())
        .attr('y', innerHeight)
        .attr('height', 0)
        .attr('fill', (d, i) => d.color || colors[i % colors.length])
        .attr('rx', 4)
        .transition()
        .duration(800)
        .attr('y', d => y(d.value))
        .attr('height', d => innerHeight - y(d.value));
    }
    
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

<svg bind:this={svgElement} {width} {height}></svg>
