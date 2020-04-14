<template>
  <div>
  <el-container style="height: 800px;">
    <el-aside width="200px" style="background-color: #FFFFFF">
      <el-menu :default-openeds="['1', '1']">
        <el-submenu index="1">
          <template slot="title"><i class="el-icon-message"></i>广告发布</template>
            <el-menu-item index="1-1" @click="toadd">发布广告</el-menu-item>
        </el-submenu>

        <el-submenu index="2">
          <template slot="title"><i class="el-icon-menu"></i>广告管理</template>
            <el-menu-item index="2-1" @click="toget">查看数据</el-menu-item>
        </el-submenu>

        <el-submenu index="3">
          <template slot="title"><i class="el-icon-collection-tag"></i>查看反馈</template>
            <el-menu-item index="3-1">标签管理</el-menu-item>
            <el-menu-item index="3-2">平台标签</el-menu-item>
        </el-submenu>
      </el-menu>
    </el-aside>

    <el-container>
      <router-view/>
    </el-container>
  </el-container>
  </div>
</template>

<style>
  .el-header {
    background-color: #FFFFFF;
    color: #333;
    line-height: 30px;
  }

  .el-aside {
    color: #333;
  }
</style>

<script>
  export default {
    // 广告主主界面，负责作不同功能页面指引跳转
    inject: ['reload'],
    data() {
      const item = {
        date: '2016-05-02',
        name: sessionStorage.getItem('email'),
        address: sessionStorage.getItem('type')
      };
      return {
        tableData: Array(20).fill(item)
      }
    },
    methods: {
      // 添加广告
      toadd() {
        this.$router.push('/advertisers/add_ads')
      },
      // 广告管理
      toget() {
        this.$router.push('/advertisers/get_ads')
      }
    },
    mounted() {
  
    }
  };
</script>
