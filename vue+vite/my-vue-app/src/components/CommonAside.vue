<template>
  <el-aside width="200px">
    <el-menu class="el-menu-vertical-demo" background-color="#545c64"
             text-color="#fff" :collapse="false">
      <el-menu-item :index="item.path" v-for="item in noChildren()"
                    :key="item.path">
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
          > <component class="icons" :is="subItem.icon"></component>
            <span>{{subItem.label}}</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-sub-menu>
    </el-menu>
  </el-aside>
</template>
<script >
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
              path: '/page1',
              name: 'page1',
              label: '页面1',
              icon: 'setting',
              url: 'Other/PageOne'
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
      const noChildren = ()=>{
        return list.filter(item=>!item.children);
      };
      const hasChildren = ()=>{
        return list.filter((item)=>item.children);
      };
      return{
        noChildren,
        hasChildren,
      };
  },
};
</script>
<style lang="less" scoped>
.icons{
  width: 20px;
  height: 20px;
}
</style>