<template>
  <el-aside :width="$store.state.isCollapse ? '180px' : '64px'">
    <el-menu class="el-menu-vertical-demo" background-color="#545c64"
             text-color="#fff" :collapse="!$store.state.isCollapse"
             :collapse-transition="false">
      <h3 v-show="$store.state.isCollapse">学生界面</h3>
      <h3 v-show="!$store.state.isCollapse">界面</h3>
      <el-menu-item :index="item.path" v-for="item in noChildren()"
                    :key="item.path"
                    @click="clickMenu(item)"
      >
        <component class="icons" :is="item.icon"></component>
        <span>{{item.label}}</span>
      </el-menu-item>
      <el-sub-menu :index="item.label" v-for="item in hasChildren()"
                   :key="item.path">
        <template #title>
          <component class="icons" :is="item.icon"></component>
          <span>{{item.label}}</span>
        </template>
        <el-menu-item-group>
          <el-menu-item
              :index="subItem.path"
              v-for="(subItem,subIndex) in item.children"
              :key="subIndex"
              @click="clickMenu(subItem)"
          > <component class="icons" :is="subItem.icon"></component>
            <span>{{subItem.label}}</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-sub-menu>
    </el-menu>
  </el-aside>
</template>
<script >

import {useRouter} from 'vue-router'
import axios from "axios";
export default {
  setup(){
    //修改左侧目录页
      const list =[
        {
          path: '/user',
          name: 'user',
          label: '用户管理',
          icon: 'user',
          url: 'UserManage/UserManage'
        },
        {
          label: '其他',
          icon: 'location',
          path: '/other',
          children: [
            {
              path: '/search',
              name: 'search',
              label: '综合查询',
              icon: 'setting',
              url: 'Other/Search'
            },
            {
              path: '/page2',
              name: 'page2',
              label: '页面2',
              icon: 'setting',
              url: 'Other/PageTwo'
            }
          ]
        }
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
      };
  },
};
</script>
<style lang="less" scoped>
.icons{
  width: 20px;
  height: 20px;
}
.el-menu{
  border-right:none;
  h3{
    line-height: 48px;
    color: #ffffff;
    text-align: center;
  }
}
</style>