
<template>
  <el-header>
    <div class="l-content">
          <el-button size="small">
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
            <el-dropdown-item>个人中心</el-dropdown-item>
            <el-dropdown-item>退出</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-header>
</template>
<script>
export default {
  setup(){
   // const imgSrc =require('../assets/images/user.png')
    const  getImgSrc = () => {
      return new URL("../assets/images/user.png",import.meta.url).href;
    };
    return{
     // imgSrc,
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
}
.r-content{
  .user{
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
}
</style>
