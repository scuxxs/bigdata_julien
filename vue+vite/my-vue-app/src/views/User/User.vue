<template>
  <div style="width: 100%;height: 1000px; display: flex;">
    <div class="right">
    <div style="width: 100%;height: 750px" id="main" ref="major"></div>
    </div>
    <div class="left">
    <div class="left-top" style=" width: 600px;height: 350px" id="lineChart" ref="lineChart"></div>
    <div class="left-bottom" style="width: 600px;height: 400px" id="pieChart" ref="pieChart"></div>
    </div>
    </div>
</template>

<script>
import * as echarts from 'echarts';


export default {
  mounted() {
    var chartDom = this.$refs.major;
    var myChart = echarts.init(chartDom);
    var option;
// There should not be negative values in rawData
    const rawData = [
      [100, 302, 301, 334, 390, 330, 320],
      [320, 132, 101, 134, 90, 230, 210],
      [220, 182, 191, 234, 290, 330, 310],
      [150, 212, 201, 154, 190, 330, 410],
      [820, 832, 901, 934, 1290, 1330, 1320]
    ];
    const totalData = [];
    for (let i = 0; i < rawData[0].length; ++i) {
      let sum = 0;
      for (let j = 0; j < rawData.length; ++j) {
        sum += rawData[j][i];
      }
      totalData.push(sum);
    }
    const grid = {
      left: 100,
      right: 100,
      top: 50,
      bottom: 50
    };
    const gridWidth = myChart.getWidth() - grid.left - grid.right;
    const gridHeight = myChart.getHeight() - grid.top - grid.bottom;
    const categoryWidth = gridWidth / rawData[0].length;
    const barWidth = categoryWidth * 0.6;
    const barPadding = (categoryWidth - barWidth) / 2;
    const series = [
      'Direct',
      'Mail Ad',
      'Affiliate Ad',
      'Video Ad',
      'Search Engine'
    ].map((name, sid) => {
      return {
        name,
        type: 'bar',
        stack: 'total',
        barWidth: '60%',
        label: {
          show: true,
          formatter: (params) => Math.round(params.value * 1000) / 10 + '%'
        },
        data: rawData[sid].map((d, did) =>
            totalData[did] <= 0 ? 0 : d / totalData[did]
        )
      };
    });
    const color = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de'];
    const elements = [];
    for (let j = 1, jlen = rawData[0].length; j < jlen; ++j) {
      const leftX = grid.left + categoryWidth * j - barPadding;
      const rightX = leftX + barPadding * 2;
      let leftY = grid.top + gridHeight;
      let rightY = leftY;
      for (let i = 0, len = series.length; i < len; ++i) {
        const points = [];
        const leftBarHeight = (rawData[i][j - 1] / totalData[j - 1]) * gridHeight;
        points.push([leftX, leftY]);
        points.push([leftX, leftY - leftBarHeight]);
        const rightBarHeight = (rawData[i][j] / totalData[j]) * gridHeight;
        points.push([rightX, rightY - rightBarHeight]);
        points.push([rightX, rightY]);
        points.push([leftX, leftY]);
        leftY -= leftBarHeight;
        rightY -= rightBarHeight;
        elements.push({
          type: 'polygon',
          shape: {
            points
          },
          style: {
            fill: color[i],
            opacity: 0.25
          }
        });
      }
    }
    option = {
      legend: {
        selectedMode: false
      },
      grid,
      yAxis: {
        type: 'value'
      },
      xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      },
      series,
      graphic: {
        elements
      }
    };
    option && myChart.setOption(option);
    var lineChartDom = this.$refs.lineChart;
    var lineChart = echarts.init(lineChartDom);

    const data = [["2000-06-05", 116], ["2000-06-06", 129], ["2000-06-07", 135], ["2000-06-08", 86], ["2000-06-09", 73], ["2000-06-10", 85], ["2000-06-11", 73], ["2000-06-12", 68], ["2000-06-13", 92], ["2000-06-14", 130], ["2000-06-15", 245], ["2000-06-16", 139], ["2000-06-17", 115], ["2000-06-18", 111], ["2000-06-19", 309], ["2000-06-20", 206], ["2000-06-21", 137], ["2000-06-22", 128], ["2000-06-23", 85], ["2000-06-24", 94], ["2000-06-25", 71], ["2000-06-26", 106], ["2000-06-27", 84], ["2000-06-28", 93], ["2000-06-29", 85], ["2000-06-30", 73], ["2000-07-01", 83], ["2000-07-02", 125], ["2000-07-03", 107], ["2000-07-04", 82], ["2000-07-05", 44], ["2000-07-06", 72], ["2000-07-07", 106], ["2000-07-08", 107], ["2000-07-09", 66], ["2000-07-10", 91], ["2000-07-11", 92], ["2000-07-12", 113], ["2000-07-13", 107], ["2000-07-14", 131], ["2000-07-15", 111], ["2000-07-16", 64], ["2000-07-17", 69], ["2000-07-18", 88], ["2000-07-19", 77], ["2000-07-20", 83], ["2000-07-21", 111], ["2000-07-22", 57], ["2000-07-23", 55], ["2000-07-24", 60]]; // Your data array here
    const dateList = data.map(function (item) {
      return item[0];
    });
    const valueList = data.map(function (item) {
      return item[1];
    });

    var lineOption = {
      visualMap: [
        {
          show: false,
          type: 'continuous',
          seriesIndex: 0,
          min: 0,
          max: 400
        },],
      title: {
        text: 'Gradient along the y axis'
      },
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        data: dateList
      },
      yAxis: {},
      series: [{
        type: 'line',
        showSymbol: false,
        data: valueList
      }]
    };
    lineOption && lineChart.setOption(lineOption);
    var pieChartDom = this.$refs.pieChart;
    var pieChart = echarts.init(pieChartDom);
    var pieOption;

    pieOption = {
      legend: {
        top: 'bottom'
      },
      toolbox: {
        show: true,
        feature: {
          mark: { show: true },
          dataView: { show: true, readOnly: false },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      series: [
        {
          name: 'Nightingale Chart',
          type: 'pie',
          radius: [35, 150],
          center: ['50%', '50%'],
          roseType: 'area',
          itemStyle: {
            borderRadius: 8
          },
          data: [
            { value: 40, name: 'rose 1' },
            { value: 38, name: 'rose 2' },
            { value: 32, name: 'rose 3' },
            { value: 30, name: 'rose 4' },
            { value: 28, name: 'rose 5' },
            { value: 26, name: 'rose 6' },
            { value: 22, name: 'rose 7' },
            { value: 18, name: 'rose 8' }
          ]
        }
      ]
    };

    pieOption&& pieChart.setOption(pieOption);

  }
};
</script>

<style scoped>
.right{
  width: 600px;
  height: 750px;
}
.left
{
  .left-top{
    width:600px ;
    height: 350px;
  }
  .left-bottom{
    width: 600px;
    height: 400px;
  }

}

</style>
