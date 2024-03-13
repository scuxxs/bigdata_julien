<template>
  <el-aside :width="$store.state.isCollapse ? '180px' : '64px'">
    <el-menu class="el-menu-vertical-demo" background-color="#545c64"
             text-color="#fff" :collapse="!$store.state.isCollapse"
             :collapse-transition="false">
      <h3 v-show="$store.state.isCollapse">管理界面</h3>
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
          label: '用户信息',
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
              path: '/warning',
              name: 'warning',
              label: '预警管理',
              icon: 'setting',
              url: 'Other/Warning'
            },

            //       path: '/latewarning',
            //       name: 'latewarning',
            //       label: '迟到预警',
            //       icon: 'edit',
            //       url: 'Other/Latewarning',
            //     },

                // {
                //   path: '/cheatwarning',
                //   name: 'cheatwarning',
                //   label: '防诈预警',
                //   icon: 'WarnTriangleFilled',
                //   url: 'Other/Warning/Cheatwarning',
                // },
                // {
                //   path: '/academywarning',
                //   name: 'academywarning',
                //   label: '学业预警',
                //   icon: 'WarnTriangleFilled ',
                //   url: 'Other/Warning/Academywarning',
                // },
                // {
                //   path: '/mentalwarning',
                //   name: 'mentalwarning',
                //   label: '心理预警',
                //   icon: 'WarnTriangleFilled ',
                //   url: 'Other/Warning/Mentalwarning',
                // },
                // {
                //   path: '/politicswarning',
                //   name: 'politicswarning',
                //   label: '思政预警',
                //   icon: 'WarnTriangleFilled ',
                //   url: 'Other/Warning/Politicswarning',
                // },
                // {
                //   path: '/povertywarning',
                //   name: 'povertywarning',
                //   label: '贫困预警',
                //   icon: 'WarnTriangleFilled ',
                //   url: 'Other/Warning/Povertywarning',
                // },
            //     ]
            // }
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