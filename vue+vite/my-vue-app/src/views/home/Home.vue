<template>
  <el-row class="home" :gutter="20">
    <el-col :span="8" style="margin-top: 20px">
      <el-card shadow="hover">
        <div class="user">
          <img src="../../assets/images/user.png" alt=""/>
          <div class="user-info">
            <p class="name">Admin</p>
            <p class="role">管理员</p>
          </div>
        </div>
        <div class="login-info">
          <p>上次登录时间<span>2024-3-9</span></p>
          <p>上次登录地点<span>成都</span></p>
        </div>
      </el-card>

      <el-card shadow="hover" style="margin-top: 20px" height="450px">
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

    </el-col>
      <el-col :span="16" style="margin-top: 20px">
    </el-col>
<!--    <div class="num">
      <el-card :body-style="{display:'flex',padding:0}">
        //传入数据

      </el-card>
    </div>-->
  </el-row>
</template>
<script>
import axios from "axios";
import {defineComponent,getCurrentInstance,onMounted,ref} from "vue";
export default defineComponent({
  setup(){

    const {proxy}= getCurrentInstance();
    let tableData = ref([]);
    const tableLabel={
      name:'课程',
      todayBuy:'今日购买',
      monthBuy:'本月购买',
      totalBuy:'总购买',

    }
    const getTableList =async ()=>{
      //url模拟数据调用
       await axios.get("/home/getData").then((res)=>{
         tableData.value = res.data.data.tableData;
        // console.log(res);

       });
    };
    onMounted(()=>{
      getTableList()
    });
    return{
      tableData,
      tableLabel,
    }
  },
});
</script>
<style lang="less" scoped>
.home {
  .user {
    display: flex;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 1px solid #ccc;
    margin-bottom: 20px;

    img {
      width: 150px;
      height: 150px;
      border-radius: 50%;
      margin-right: 40px;
    }
  }

  .login-info {
    p {
      line-height: 30px;
      font-size: 14px;
      color: #999;

      span {
        color: #666;
        margin-left: 60px;
      }
    }
  }

/*  .num{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    .el-card{
      width: 32%;
      margin-bottom: 20px;
    }
}*/
}
</style>


<script setup>
</script>