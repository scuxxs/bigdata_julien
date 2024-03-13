<template>
  <div class="mb-4">
    <el-button  type="info" @click="goTo('/warning')" round>学业预警</el-button>
    <el-button   type="warning" @click="goTo('/latewarning')" round>迟到预警 </el-button>
    <el-button   type="info" @click="goTo('/mentalwarning')" round>心理预警</el-button>
    <el-button  type="info" @click="goTo('/povertywarning')" round>贫困预警</el-button>
    <el-button  type="info" @click="goTo('/politicswarning')" round>思政预警</el-button>
    <el-button type="info" @click="goTo('/cheatwarning')" round>防诈预警</el-button>
  </div>
  <el-row class="search" :gutter="40">
    <el-col :span="12">
      <el-card shadow="hover" style=" margin-left: 40px; max-height:700px">
        <div class="table-container" style="overflow-y: auto;">
          <el-table :data="pagedTableData"  style="width: 100%" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" />
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
      <el-pagination
          :page-size="10"
          :pager-count="11"
          layout="prev, pager, next"
          :total="tableData.length"
          background
          @current-change="handleCurrentChange"
      ></el-pagination>
    </el-col>
    <el-col :span="12">
      <el-card shadow="hover" style="margin-left: 40px;">
        <div class="announcement">
          <h3>通知栏</h3>
          <el-input
              v-model="textarea"
              style="width: 350px ; margin-top: 15px"
              :rows="2"
              type="textarea"
              placeholder="Please input"
          />
          <el-button type="primary" @click="submitData" round>通知</el-button>
        </div>
        <el-card style="max-width: 480px">
          <template #header>Yummy hamburger</template>
          <img
              src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
              style="width: 100%"
          />
        </el-card>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import api from '../../api/mockData/axios.js';
export default {
  data() {
    return {
      textarea: ''
    };
  },
  methods: {
    goTo(route) {
      this.$router.push(route);
    },
    submitData() {
      const data = {
        precautionType:1,
        msg: this.textarea,
        studentList: this.selectedRows,
      };
      // 向后端发送数据，可以使用 axios 或其他 HTTP 请求库
      api.post('/api/precaution/late', data)
          .then(response => {
            alert(response.data.msg)
            // 处理成功响应
          })
          .catch(error => {
            // 处理错误响应
          });
    },
    handleSelectionChange(selection) {
      this.selectedRows = selection;
      // 在这里可以访问this.selectedRows来获取选中的行数据
      console.log(this.selectedRows);
    },
  },
  setup() {
    const selectedRows = ref([]);
    let tableData = ref([]);
    const tableLabel = {
      name: '姓名',
      id: 'ID',
      college: '学院',
      major: '专业',
      late_level: '迟到预警',
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
      selectedRows,
    };
  },
};
</script>


<style>
.table-container {
  height: 90%;
  overflow-y: auto;
}
</style>
