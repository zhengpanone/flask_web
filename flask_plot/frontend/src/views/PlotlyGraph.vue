<template>
<div id="tester" style="width:600px;height:250px;">
</div>
</template>

<script>
import Plotly from 'plotly.js-dist/plotly'
export default {
  name: 'PlotlyGraph',
  watch: {
    chart: {
      handler: function () {
        var TESTER = document.getElementById('tester')
        Plotly.plot(TESTER, [{
          x: [1, 2, 3, 4, 5],
          y: [1, 2, 4, 8, 16] }], {
          margin: { t: 0 } })
      }
    }
  }
}
</script>

<style scoped>

</style>
