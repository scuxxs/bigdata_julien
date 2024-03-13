<template>
  <el-row class="search" :gutter="60">
    <el-card shadow="hover" style="margin-top: 20px; margin-left: 40px; max-height:700px">
      <div class="table-container" style="overflow-y: auto;">
        <el-table :data="pagedTableData"  style="width: 100%">
          <el-table-column
              v-for="(val, key) in tableLabel"
              :key="key"
              :prop="key"
              :label="val"
              width="108"
          >
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </el-row>
  <el-pagination
      :page-size="10"
      :pager-count="11"
      layout="prev, pager, next"
      :total="tableData.length"
      background
      @current-change="handleCurrentChange"
  ></el-pagination>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import api from '../../api/mockData/axios.js';

export default {
  setup() {
    let tableData = ref([]);
    const tableLabel = {
      name: '姓名',
      id: 'ID',
      college: '学院',
      major: '专业',
      late_level: '迟到预警',
      cheat_level: '防诈预警',
      poverty_level: '贫困预警',
      politics_level: '思政预警',
      academy_level: '学术预警',
      mental_level: '心理预警',
      total_grade: '总成绩',
    };

    const pagedTableData = ref([]);
    const currentPage = ref(1);

    onMounted(() => {
      api.get('/api/search/all')
          .then(response => {
            tableData.value = response.data.data;
            console.log(response.data.data);
          })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    });

    const handleCurrentChange = (val) => {
      currentPage.value = val;
      const startIndex = (val - 1) * 10;
      const endIndex = startIndex + 10;
      pagedTableData.value = tableData.value.slice(startIndex, endIndex);
    };

    return {
      tableData,
      tableLabel,
      pagedTableData,
      handleCurrentChange,
    };
  },
};
</script>

<style>
.table-container {
  height: 100%;
  overflow-y: auto;
}
</style>
