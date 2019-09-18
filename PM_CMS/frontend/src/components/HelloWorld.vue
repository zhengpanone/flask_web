<template>
<div>

</div>
</template>

<script>
import * as d3 from 'd3'
const data = [99, 71, 78, 25, 36, 92]
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'

    }
  },
  mounted () {
    const svg = d3.select(this.$el)
      .append('svg')
      .attr('width', 500)
      .attr('height', 270)
      .append('g')
      .attr('transform', 'translate(0,10)')
    const x = d3.scaleLinear().range([0, 430])
    const y = d3.scaleLinear().range([210, 0])
    d3.axisLeft().scale(x)
    d3.axisTop().scale(y)
    x.domain(d3.extent(data, (d, i) => i))
    y.domain([0, d3.max(data, d => d)])
    const createPath = d3.line()
      .x((d, i) => x(i))
      .y(d => y(d))
    svg.append('path').attr('d', createPath(data))
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped >
svg{
  margin: 25px;
}
  stroke{
    background: #76bf8a;
  }
</style>
