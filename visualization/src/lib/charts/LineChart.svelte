<script lang="ts">
  import * as d3 from 'd3';
  
  interface LineData {
    x: number | string;
    y: number;
    series?: string;
  }
  
  interface Props {
    data: LineData[];
    width?: number;
    height?: number;
    marginTop?: number;
    marginRight?: number;
    marginBottom?: number;
    marginLeft?: number;
    xLabel?: string;
    yLabel?: string;
    formatY?: (d: number) => string;
    showArea?: boolean;
    multiSeries?: boolean;
  }
  
  let {
    data,
    width = 600,
    height = 400,
    marginTop = 30,
    marginRight = 100,
    marginBottom = 50,
    marginLeft = 80,
    xLabel = '',
    yLabel = '',
    formatY = (d: number) => d.toLocaleString(),
    showArea = false,
    multiSeries = false
  }: Props = $props();
  
  let svgElement: SVGSVGElement;
  
  const colors = ['#d1a45a', '#79d2c5', '#f0d7a7', '#ff7a7a', '#8ab4f8', '#c58bd3'];
  const axisTextColor = 'rgba(247, 242, 233, 0.65)';
  const axisLineColor = 'rgba(247, 242, 233, 0.18)';
  const gridLineColor = 'rgba(247, 242, 233, 0.12)';
  
  $effect(() => {
    if (!svgElement || !data || data.length === 0) return;
    
    d3.select(svgElement).selectAll('*').remove();
    
    const svg = d3.select(svgElement);
    const innerWidth = width - marginLeft - marginRight;
    const innerHeight = height - marginTop - marginBottom;
    
    const g = svg.append('g')
      .attr('transform', `translate(${marginLeft},${marginTop})`);
    
    // 处理数据
    const xValues = [...new Set(data.map(d => d.x))];
    const isNumericX = typeof xValues[0] === 'number';
    
    // X比例尺
    let x: d3.ScaleLinear<number, number> | d3.ScalePoint<string>;
    if (isNumericX) {
      const xExtent = d3.extent(data, d => d.x as number) as [number, number];
      x = d3.scaleLinear()
        .domain(xExtent)
        .range([0, innerWidth]);
    } else {
      x = d3.scalePoint()
        .domain(xValues as string[])
        .range([0, innerWidth]);
    }
    
    // Y比例尺
    const yMax = d3.max(data, d => d.y) || 0;
    const y = d3.scaleLinear()
      .domain([0, yMax * 1.1])
      .range([innerHeight, 0]);
    
    // 网格线
    g.append('g')
      .attr('class', 'grid')
      .call(d3.axisLeft(y).tickSize(-innerWidth).tickFormat(() => ''))
      .selectAll('line')
      .style('stroke', gridLineColor)
      .style('stroke-dasharray', '3,3');
    
    // X轴
    const xAxis = isNumericX 
      ? d3.axisBottom(x as d3.ScaleLinear<number, number>).ticks(10)
      : d3.axisBottom(x as d3.ScalePoint<string>);
    
    const xAxisGroup = g.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(xAxis)
      ;
    
    xAxisGroup.selectAll('text')
      .style('font-size', '11px')
      .style('fill', axisTextColor);
    
    xAxisGroup.selectAll('path, line')
      .style('stroke', axisLineColor);
    
    // Y轴
    const yAxisGroup = g.append('g')
      .call(d3.axisLeft(y).ticks(6).tickFormat(d => formatY(d as number)));
    
    yAxisGroup.selectAll('text')
      .style('font-size', '11px')
      .style('fill', axisTextColor);
    
    yAxisGroup.selectAll('path, line')
      .style('stroke', axisLineColor);
    
    // 线条生成器
    const line = d3.line<LineData>()
      .x(d => {
        if (isNumericX) {
          return (x as d3.ScaleLinear<number, number>)(d.x as number);
        }
        return (x as d3.ScalePoint<string>)(d.x as string) || 0;
      })
      .y(d => y(d.y))
      .curve(d3.curveMonotoneX);
    
    if (multiSeries) {
      // 多系列
      const series = d3.group(data, d => d.series || 'default');
      const colorScale = d3.scaleOrdinal<string>()
        .domain([...series.keys()])
        .range(colors);
      
      let i = 0;
      series.forEach((seriesData, seriesName) => {
        const sortedData = [...seriesData].sort((a, b) => {
          if (typeof a.x === 'number') return a.x - (b.x as number);
          return String(a.x).localeCompare(String(b.x));
        });
        
        // 面积
        if (showArea) {
          const area = d3.area<LineData>()
            .x(d => {
              if (isNumericX) {
                return (x as d3.ScaleLinear<number, number>)(d.x as number);
              }
              return (x as d3.ScalePoint<string>)(d.x as string) || 0;
            })
            .y0(innerHeight)
            .y1(d => y(d.y))
            .curve(d3.curveMonotoneX);
          
          g.append('path')
            .datum(sortedData)
            .attr('fill', colorScale(seriesName))
            .attr('fill-opacity', 0.1)
            .attr('d', area);
        }
        
        // 线条
        g.append('path')
          .datum(sortedData)
          .attr('fill', 'none')
          .attr('stroke', colorScale(seriesName))
          .attr('stroke-width', 2.5)
          .attr('d', line);
        
        // 图例
        g.append('rect')
          .attr('x', innerWidth + 10)
          .attr('y', i * 20)
          .attr('width', 12)
          .attr('height', 12)
          .attr('fill', colorScale(seriesName));
        
        g.append('text')
          .attr('x', innerWidth + 28)
          .attr('y', i * 20 + 10)
          .style('font-size', '11px')
          .style('fill', axisTextColor)
          .text(seriesName);
        
        i++;
      });
    } else {
      // 单系列
      const sortedData = [...data].sort((a, b) => {
        if (typeof a.x === 'number') return a.x - (b.x as number);
        return String(a.x).localeCompare(String(b.x));
      });
      
      // 面积
      if (showArea) {
        const area = d3.area<LineData>()
          .x(d => {
            if (isNumericX) {
              return (x as d3.ScaleLinear<number, number>)(d.x as number);
            }
            return (x as d3.ScalePoint<string>)(d.x as string) || 0;
          })
          .y0(innerHeight)
          .y1(d => y(d.y))
          .curve(d3.curveMonotoneX);
        
        g.append('path')
          .datum(sortedData)
          .attr('fill', colors[0])
          .attr('fill-opacity', 0.1)
          .attr('d', area);
      }
      
      // 线条
      g.append('path')
        .datum(sortedData)
        .attr('fill', 'none')
        .attr('stroke', colors[0])
        .attr('stroke-width', 2.5)
        .attr('d', line);
      
      // 点
      g.selectAll('.dot')
        .data(sortedData)
        .join('circle')
        .attr('class', 'dot')
        .attr('cx', d => {
          if (isNumericX) {
            return (x as d3.ScaleLinear<number, number>)(d.x as number);
          }
          return (x as d3.ScalePoint<string>)(d.x as string) || 0;
        })
        .attr('cy', d => y(d.y))
        .attr('r', 4)
        .style('fill', colors[0])
        .style('stroke', 'rgba(11, 10, 8, 0.85)')
        .style('stroke-width', 2);
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
