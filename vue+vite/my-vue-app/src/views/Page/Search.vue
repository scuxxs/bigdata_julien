<template>
  <el-card shadow="hover" style="margin-top: 20px" height="800px">
  <el-table :data="tableData">
    <el-table-column
        v-for="(val,key) in tableLabel"
        :key="key"
        :prop="key"
        :label="val"
    >
    </el-table-column>
  </el-table>
  </el-card>
  </template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import api from '../../api/mockData/axios.js';
export default {
  setup() {
    const tableData = ref([]);
    const tableLabel={
      name:'姓名',
      id:'ID',
      college:'学院',
      major:'专业',

    }
    onMounted(() => {
      api.get('/api/search/all')
          .then(response => {
            tableData.value = response.data.data;
          })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    });

    return {
      tableData,
      tableLabel
    };
  },
};
</script>
