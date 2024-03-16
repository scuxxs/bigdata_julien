
<template>
  <el-header>
    <div class="l-content">
          <el-button size="small" palin @click="handleCollapse">
            <el-icon :size="20">
              <Menu />
            </el-icon>
          </el-button>
    </div>
    <div class="r-content">
      <el-dropdown>
    <span class="el-dropdown-link">
      <img class="user" :src="getImgSrc()" alt="" />
    </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleLogout">退出</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-header>
</template>
<script>

import  {useStore} from "vuex";
import router from "../router/index.js";

export default {
  methods :{
    handleLogout(){
      router.push('/login')
    },
    // goHome(){
    //   router.replace('/home')
    // }
  },
  setup(){
    let store = useStore()
   // const imgSrc =require('../assets/images/user.png')
    const  getImgSrc = () => {
      return new URL("../assets/images/user.png",import.meta.url).href;
    };
    let handleCollapse = ()=>{
      //调用vuex中的mutations
      store.commit("updateIsCollapse")
    }
    return{
     // imgSrc,
      handleCollapse,
      getImgSrc
    };
  },
};
</script>
<style lang="less" scoped>
header{
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  background:#203A43;
}
.r-content{
  .user{
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
}
.l-content{
  display: flex;
  align-items: center;
  .el-button{
    margin-right:20px ;
  }
  h3{
    color:#ffffff;
  }
}
</style>
