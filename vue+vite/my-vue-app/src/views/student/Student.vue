<template>
  <el-container>
    <el-header>
      <div class="l-content">
        <el-button size="small" palin @click="handleCollapse">
          <el-icon :size="20">
            <Menu />
          </el-icon>
        </el-button>
        <h3>首页</h3>
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
    <el-aside :width="$store.state.isCollapse ? '180px' : '64px'">
      <el-menu class="el-menu-vertical-demo" background-color="#545c64"
               text-color="#fff" :collapse="!$store.state.isCollapse"
               :collapse-transition="false">
        <h3 v-show="$store.state.isCollapse">学生界面</h3>
        <h3 v-show="!$store.state.isCollapse">学生</h3>
        <el-menu-item :index="item.path" v-for="item in noChildren()"
                      :key="item.path"
                      @click="clickMenu(item)"
        >
          <component class="icons" :is="item.icon"></component>
          <span>{{item.label}}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main>
      <div class="main-container">
        <el-collapse accordion>
          <el-collapse-item name="1">
            <template #title>
              学业预警<el-icon class="header-icon">
              <info-filled />
            </el-icon>
            </template>
            <div>
            学业预警
            </div>
            <div>
              学业差
            </div>
          </el-collapse-item>
          <el-collapse-item title="迟到预警" name="2">
            <div>
            迟到
            </div>
          </el-collapse-item>
          <el-collapse-item title="心理预警" name="3">
            <div>
            心理
            </div>
          </el-collapse-item>
          <el-collapse-item title="贫困预警" name="4">
            <div>
              Decision making: giving advices about operations is acceptable, but do
              not make decisions for the users;
            </div>
          </el-collapse-item>
          <el-collapse-item title="政治预警" name="5">
            <div>
             政治
            </div>
          </el-collapse-item>
          <el-collapse-item title="防诈预警" name="6">
            <div>
             cheat
            </div>
          </el-collapse-item>
          <!-- 折叠面板内容 -->
        </el-collapse>
      </div>
    </el-main>
  </el-container>
</template>
<script >
import { ref, onMounted } from 'vue';
import { InfoFilled } from '@element-plus/icons-vue'
import  {useStore} from "vuex";
import {useRouter} from 'vue-router'
import axios from "axios";
export default {
  setup(){
    const fetchPanelContent = async (uid) => {
      try {
        const response = await axios.get(`/api/precaution/late/student/${uid}`);
        console.log(response.data.data);
        const panelcontent = response.data.data.map(item => item.msg);
        return panelcontent;
      } catch (error) {
        console.error('Failed to fetch panel content:', error);
        return [];
      }
    };

// 通过 fetchPanelContent 函数获取折叠面板内容
    const getPanelContent = async (uid) => {
      const content = await fetchPanelContent(uid);
      // 将折叠面板内容存储到 state 中
      store.commit('updatePanelContent', content);
    };

// 在组件初始化时获取折叠面板内容
    onMounted(() => {
      const uid = 'student'; // 替换成实际的uid
      getPanelContent(uid);
    });
    let store = useStore()
    // const imgSrc =require('../assets/images/user.png')
    const  getImgSrc = () => {
      return new URL("../../assets/images/user.png",import.meta.url).href;
    };
    let handleCollapse = ()=>{
      //调用vuex中的mutations
      store.commit("updateIsCollapse")
    }
    //修改左侧目录页
    const list =[
      {
        path: '/student',
        name: 'student',
        label: '学生管理',
        icon: 'user',
        url: 'Student/Student'
      },
    ];
    const router =useRouter();
    const noChildren = ()=>{
      return list.filter(item=>!item.children);
    };
    const hasChildren = ()=>{
      return list.filter((item)=>item.children);
    };
    const clickMenu =(item)=>{
      router.push({
        name:item.name,
      });
    };
    return{
      noChildren,
      hasChildren,
      clickMenu,
      handleCollapse,
      getImgSrc
    };
  },
};
</script>


<style lang="less" scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  background: #333;
}

.r-content {
  .user {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
}

.l-content {
  display: flex;
  align-items: center;
  .el-button {
    margin-right: 20px;
  }
  h3 {
    color: #ffffff;
  }
}

.icons {
  width: 20px;
  height: 20px;
}

.el-menu {
  border-right: none;
  h3 {
    line-height: 48px;
    color: #ffffff;
    text-align: center;
  }
}

.main-container {
  position: absolute;
  top: 64px; /* 调整折叠面板距离顶部的位置 */
  right: 0; /* 将折叠面板显示在右侧 */
  width: calc(100% - 180px); /* 设置宽度为除去左侧菜单栏的剩余空间 */
  height: calc(100% - 64px); /* 设置高度为除去头部的剩余空间 */
  overflow: auto; /* 添加滚动条 */
  padding: 15px; /* 添加内边距 */
}

.el-collapse {
  background-color: #f0f0f0; /* 设置折叠面板背景色 */
  border-radius: 5px; /* 设置边框圆角 */
}
</style>
