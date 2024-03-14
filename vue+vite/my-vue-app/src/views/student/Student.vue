<template>
  <el-container>
    <el-header>
      <div class="l-content">
        <el-button size="small" palin @click="handleCollapse">
          <el-icon :size="20">
            <Menu />
          </el-icon>
        </el-button>
        <h3>Welcome!</h3>
      </div>
      <div class="r-content">
        <el-dropdown>
          <span class="el-dropdown-link">
            <img class="user" :src="getImgSrc()" alt="" />
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item  @click="handleLogout" >退出</el-dropdown-item>
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
          <el-collapse-item  @click="openNotification" name="1">
            <template #title>
              学业预警通知<el-icon class="header-icon">
              <info-filled />
            </el-icon>
            </template>
            <div v-for="item in panelData.academicWarning">{{ item }}
            </div>
          </el-collapse-item>
          <el-collapse-item title="晚归预警通知" name="2">
            <div v-for="item in panelData.lateWarning">{{ item }}
            </div>
          </el-collapse-item>
          <el-collapse-item title="心理预警通知" name="3">
            <div v-for="item in panelData.mentalWarning">{{ item }}
            </div>
          </el-collapse-item>
          <el-collapse-item title="贫困预警通知" name="4">
            <div v-for="item in panelData.povertyWarning">{{ item }}
            </div>
          </el-collapse-item>
          <el-collapse-item title="思政预警通知" name="5">
            <div v-for="item in panelData.politicsWarning">{{ item }}
            </div>
          </el-collapse-item>
          <el-collapse-item title="防诈预警通知" name="6">
            <div v-for="item in panelData.cheatWarning">{{ item }}
            </div>
          </el-collapse-item>
          <!-- 折叠面板内容 -->
        </el-collapse>

        <el-carousel :interval="4000" type="card" height="150px">
          <el-carousel-item v-for="(item, index) in carouselItems" :key="index">
            <h3>{{ item.title }}</h3>
          </el-carousel-item>
        </el-carousel>
      </div>
      <div class="right">
        <el-calendar style="height: 500px;width: 600px;margin-right: 20px" >
          <template #date-cell="{ data }">
            <p :class="data.isSelected ? 'is-selected' : ''">
              {{ data.day.split('-').slice(1).join('-') }}
              {{ data.isSelected ? '✔️' : '' }}
            </p>
          </template>
        </el-calendar>
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
import api from '../../api/mockData/axios.js';
import router from "../../router/index.js";
import { ElNotification } from 'element-plus';
export default {

  methods :{
    handleLogout(){
      router.push('/login')
    }
  },
  // data() {
  //   return {
  //     panelData: [], // 后端获取的数据
  //   };
  // },
  setup(){
    const openNotification = () => {
      ElNotification({
        title: 'Warning',
        message: 'This is a warning message',
        type: 'warning',
      });
    }
    const carouselItems = ref([
      { title: 'Academy'},
      { title: 'Late' },
      { title: 'Cheat' },
      { title: 'Politics' },
      { title: 'Poverty' },
      { title: 'Mental'},
      { title: 'Total'},
    ]);
    const uid = localStorage.getItem('uid');
    const panelData = ref({});
    const fetchPanelContent = async (uid) => {
      try {
        const response = await api.get(`/api/precaution/late/student?uid=${uid}`);
        console.log(response.data.data);
        const data = response.data.data;
        const academicWarning = []; // 学业预警
        const lateWarning = []; // 晚归预警
        const mentalWarning = []; // 心理预警
        const povertyWarning = []; // 贫困预警
        const cheatWarning = []; // 防诈预警
        const politicsWarning = []; // 思政预警
        data.forEach((item) => {
          console.log(item.precaution_type)
          switch (item.precaution_type) {
            case 4 :
              academicWarning.push(item.msg);
              break;
            case 0 :
              lateWarning.push(item.msg);
              break;
            case 5 :
              mentalWarning.push(item.msg);
              break;
            case 2 :
              povertyWarning.push(item.msg);
              break;
            case 1 :
              cheatWarning.push(item.msg);
              break;
            case 3 :
              politicsWarning.push(item.msg);
              break;
            default:
              break;
          }
        });
        panelData.value = {
          academicWarning,
          lateWarning,
          mentalWarning,
          povertyWarning,
          cheatWarning,
          politicsWarning,
        };
      } catch (error) {
        console.error('Failed to fetch panel content:', error);
        panelData.value = {
          academicWarning: [],
          lateWarning: [],
          mentalWarning: [],
          povertyWarning: [],
          cheatWarning:[],
          politicsWarning:[],
        };
      }
    };
// 通过 fetchPanelContent 函数获取折叠面板内容
    const getPanelContent = async (uid) => {
      const data = await fetchPanelContent(uid);
      // 将折叠面板内容存储到 state 中
      store.commit('updatePanelContent', data);
    };
// 在组件初始化时获取折叠面板内容
    onMounted(() => {
      //替换成实际的uid
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
      getImgSrc,
      panelData,
      carouselItems,
      openNotification
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
    left: 180px; /* 将折叠面板显示在右侧 */
    width: calc(60% - 180px); /* 设置宽度为除去左侧菜单栏的剩余空间 */
    height: calc(100% - 64px); /* 设置高度为除去头部的剩余空间 */
    overflow: auto; /* 添加滚动条 */
    padding: 20px; /* 添加内边距 */
  }


  .el-collapse {
    background-color: #f0f0f0; /* 设置折叠面板背景色 */
    border-radius: 10px; /* 设置边框圆角 */
  }

  .el-carousel__item h3 {
    color: #475669;
    opacity: 0.75;
    line-height: 150px;
    margin: 0px;
    text-align: center;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n + 1) {
    background-color: #d3dce6;
  }
  .right {
    position: absolute;
    top: 64px; /* 与折叠面板顶部对齐 */
    right: 30px; /* 固定在页面右侧 */
    width: calc(50% - 180px); /* 设置宽度为右侧40%的空间，减去折叠面板的宽度 */
    height: calc(100% - 64px); /* 设置高度为除去头部的剩余空间 */
    overflow: auto; /* 添加滚动条 */
    padding: 20px; /* 添加内边距 */
  }

.is-selected {
  color: #1989fa;
}


//.warning-item {
//  display: flex;
//  justify-content: space-between;
//}
</style>
