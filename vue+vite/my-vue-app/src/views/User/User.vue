<template>
  <div style="width: 100%;height: 1000px; display: flex;">
    <div class="right">
      <el-select v-model="Svalue" placeholder="Select" style="width: 240px;margin-left: 60px" @change="handleSelectChange">
        <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            :disabled="item.disabled"
        />
      </el-select>
      <div style="width: 100%;height: 750px" id="main" ref="major"></div>
    </div>
    <div class="left">
      <div class="left-top" style=" width: 600px;height: 350px" id="lineChart" ref="lineChart"></div>
      <div class="left-bottom" style="width: 600px;height: 400px" id="pieChart" ref="pieChart"></div>
    </div>
  </div>
</template>

<script>
import {defineComponent,getCurrentInstance,onMounted,ref} from "vue";
import { createRouter, createWebHistory } from "vue-router";
import api from '../../api/mockData/axios.js';
import * as echarts from 'echarts';
import router from "../../router/index.js";
import {  watch } from 'vue';

try {
  const homerequest = await api.get('/api/home/inithome');
  console.log(homerequest.data.code)
  if(homerequest.data.code === 301){
    router.replace('/login')
  }
  else{
    alert(homerequest.data.msg);
  }
} catch (error) {
  console.error("请求错误:", error.message); // 添加错误处理，打印错误信息
}

export default {
  methods: {
    handleSelectChange(newValue) {
      // 根据选择的值动态跳转到不同的页面
      router.push({ path: `/${newValue}` });
    }
  },
  data() {
    return {
      Svalue: '',
      options: [
        {value: 'Option1', label: 'Option1'},
        {value: 'Option2', label: 'Option2'},
        {value: 'Option3', label: 'Option3'},
        {value: 'Option4', label: 'Option4'},
        {value: 'Option5', label: 'Option5'}
      ],
    }
  },

  mounted() {
    var chartDom = this.$refs.major;
    var myChart = echarts.init(chartDom);
    var option;
    const rawData =  [
      [12, 4, 6, 18, 3, 12, 10],
      [6, 7, 12, 4, 9, 2, 8],
      [2, 11, 19, 2, 2, 13, 3],
      [15, 2, 2, 15, 19, 3, 14],
      [8, 8, 9, 9, 12, 13, 13]
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
      'Level 0',
      'Level 1',
      'Level 2',
      'Level 3',
      'Level 4'
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
        data: ['学业', '防诈', '心理', '思政', '迟到', '贫困']
      },
      series,
      graphic: {
        elements
      }
    };
    option && myChart.setOption(option);
    var lineChartDom = this.$refs.lineChart;
    var lineChart = echarts.init(lineChartDom);

    const data = [["2023-11-26", 13], ["2023-11-27", 11], ["2023-11-28", 11], ["2023-11-29", 30],
      ["2023-11-30", 20], ["2023-12-1", 13], ["2023-12-2", 12], ["2023-12-3", 8], ["2023-12-4", 9],
      ["2023-12-5", 7], ["2023-12-6", 10], ["2023-12-7", 8], ["2023-12-8", 9], ["2023-12-9", 8],
      ["2023-12-10", 7], ["2023-12-11", 8], ["2023-12-11", 12], ["2023-12-12", 10], ["2023-12-13", 8],
      ["2023-12-14", 4], ["2023-12-15", 7], ["2023-12-16", 11], ["2023-12-17", 12], ["2023-12-18", 13], ["2023-12-19", 8], ["2023-12-20",
      7], ["2023-12-21", 8], ["2023-12-22", 7], ["2023-12-23", 6], ["2023-12-24", 9], ["2023-12-25", 13],
      ["2023-12-26", 24], ["2023-12-27", 10], ["2023-12-28", 10], ["2023-12-29", 6],
      ["2023-12-30", 9], ["2023-12-31", 9],]
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
          max: 40,
        },],
      title: {
        text: '人工智能专业'
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
            { value: 8, name: '学业五级人数' },
            { value: 13, name: '迟到五级人数' },
            { value: 13, name: '贫困五级人数' },
            { value: 9, name: '思政五级人数' },
            { value: 9, name: '心理五级人数' },
            { value: 8, name: '防诈五级人数' },
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