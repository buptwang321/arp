<template>
  <div>
  <el-container style="height: 800px;">
    <el-aside width="200px" style="background-color: #FFFFFF">
      <el-menu :default-openeds="['2', '1']">
        <el-submenu index="1">
          <template slot="title"><i class="el-icon-message"></i>社交用户</template>
            <el-menu-item index="1-1" @click="toadd">导入用户</el-menu-item>
        </el-submenu>

        <el-submenu index="2">
          <template slot="title"><i class="el-icon-menu"></i>用户管理</template>
            <el-menu-item index="2-1" @click="toget">查看数据</el-menu-item>
        </el-submenu>

        <el-submenu index="3">
          <template slot="title"><i class="el-icon-collection-tag"></i>广告推荐</template>
            <el-menu-item index="3-1" @click="torecommend">查看推荐</el-menu-item>
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
    // 社交平台主界面，负责作不同功能页面指引跳转
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
      // 添加新社交用户
      toadd() {
        this.$router.push('/platforms/add_cust')
      },
      // 显示自己平台所有社交用户
      toget() {
        this.$router.push('/platforms/show_cust')
      },
      // 对社交用户进行广告推荐
      torecommend() {
        this.$router.push('/platforms/show_recommend')
      }
    },
    mounted() {
  
    }
  };
</script>
