<template>
  <el-row class="search" :gutter="60">
    <el-card shadow="hover" style="margin-top: 20px; margin-left: 60px; max-height:700px">
      <el-input
          v-model="input1"
          style="width: 180px; margin-left: 10px;"
          placeholder="Please Input Name"
          :prefix-icon= "Search"
          clearable
      />
      <el-input
          v-model="input2"
          style="width: 180px;  margin-left: 10px;"
          placeholder="Please Input ID"
          :prefix-icon= "Search"
          clearable
      />
      <el-input
          v-model="input3"
          style="width: 180px; margin-left: 10px;"
          placeholder="Please Input College"
          :prefix-icon= "Search"
          clearable
      />
      <el-input
          v-model="input4"
          style="width: 180px; margin-left: 10px;"
          placeholder="Please Input Major"
          :prefix-icon= "Search"
          clearable
      />
      <el-button type="primary" @click="handleSearch" style="margin-left: 350px">搜索</el-button>
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
import {Search} from "@element-plus/icons-vue";
import { reactive } from 'vue';
export default {
  computed: {
    Search() {
      return Search
    }
  },
  setup() {
    let tableData = ref([ ]);

    const input1 = ref('');
    const input2 = ref('');
    const input3 = ref('');
    const input4 = ref('');

    const handleSearch = () => {
      const data = {
        name: input1.value,
        id: input2.value,
        college: input3.value,
        major: input4.value}
      api.post('/api/search/getStudent', data)
          .then(response => {
            console.log(response.data.data)
            tableData.value = response.data.data; // 更新表格数据
            console.log(tableData.value)
          })
          .catch(error => {
            console.error('Error searching data:', error);
          });
    };
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
      input1,
      input2,
      input3,
      input4,
      handleSearch,
    };
  },
};
</script>

<style>
.table-container {
  max-height: 620px;
  overflow-y: auto;
}
</style>
