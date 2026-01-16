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
  
  const colors = [
    '#d1a45a', '#79d2c5', '#f0d7a7', '#ff7a7a', '#8ab4f8',
    '#c58bd3', '#f2b87a', '#7aa7ff', '#9ad48f', '#f4a3a3'
  ];
  const axisTextColor = 'rgba(247, 242, 233, 0.65)';
  const axisLineColor = 'rgba(247, 242, 233, 0.18)';
  
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
      const xAxis = g.append('g')
        .attr('transform', `translate(0,${innerHeight})`)
        .call(d3.axisBottom(x).ticks(5).tickFormat(d => formatValue(d as number)));
      
      xAxis.selectAll('text')
        .style('font-size', '12px')
        .style('fill', axisTextColor);
      
      xAxis.selectAll('path, line')
        .style('stroke', axisLineColor);
      
      // Y轴
      const yAxis = g.append('g')
        .call(d3.axisLeft(y));
      
      yAxis.selectAll('text')
        .style('font-size', '12px')
        .style('fill', axisTextColor);
      
      yAxis.selectAll('path, line')
        .style('stroke', axisLineColor);
      
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
        .style('fill', axisTextColor)
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
      const xAxis = g.append('g')
        .attr('transform', `translate(0,${innerHeight})`)
        .call(d3.axisBottom(x));
      
      xAxis.selectAll('text')
        .attr('transform', 'rotate(-45)')
        .style('text-anchor', 'end')
        .style('font-size', '11px')
        .style('fill', axisTextColor);
      
      xAxis.selectAll('path, line')
        .style('stroke', axisLineColor);
      
      // Y轴
      const yAxis = g.append('g')
        .call(d3.axisLeft(y).ticks(5).tickFormat(d => formatValue(d as number)));
      
      yAxis.selectAll('text')
        .style('font-size', '12px')
        .style('fill', axisTextColor);
      
      yAxis.selectAll('path, line')
        .style('stroke', axisLineColor);
      
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
        .style('font-size', '12px')
        .style('fill', axisTextColor)
        .text(xLabel);
    }
    
    // Y轴标签
    if (yLabel) {
      svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', 15)
        .attr('text-anchor', 'middle')
        .style('font-size', '12px')
        .style('fill', axisTextColor)
        .text(yLabel);
    }
  });
</script>

<svg bind:this={svgElement} {width} {height}></svg>
