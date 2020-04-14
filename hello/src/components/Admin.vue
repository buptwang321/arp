<template>
  <div>
  <el-container style="height: 800px;">
    <el-aside width="200px" style="background-color: #FFFFFF">
      <el-menu :default-openeds="['1', '1']">
        <el-submenu index="1">
          <template slot="title"><i class="el-icon-message"></i>用户管理</template>
            <el-menu-item index="1-1" @click="tousers">平台用户</el-menu-item>
            <el-menu-item index="1-2" @click="tocust">社交用户</el-menu-item>
        </el-submenu>

        <el-submenu index="2">
          <template slot="title"><i class="el-icon-menu"></i>广告管理</template>
            <el-menu-item index="2-1" @click="togetads">广告数据</el-menu-item>
        </el-submenu>

        <el-submenu index="3">
          <template slot="title"><i class="el-icon-collection-tag"></i>一级标签管理</template>
            <el-menu-item index="3-1" @click="tolabel">标签管理</el-menu-item>
        </el-submenu>

         <el-submenu index="4">
          <template slot="title"><i class="el-icon-goods"></i>语料库管理</template>
        </el-submenu>
         <el-submenu index="5">
          <template slot="title"><i class="el-icon-s-promotion"></i>推荐管理</template>
        </el-submenu>
      </el-menu>
    </el-aside>

    <el-container>
      <!--<el-header style="text-align: right; font-size: 12px; height: 30px;">-->
        <!--<el-dropdown>-->
          <!--<i class="el-icon-setting" style="margin-right: 15px"></i>-->
          <!--<el-dropdown-menu slot="dropdown">-->
            <!--<el-dropdown-item>查看</el-dropdown-item>-->
            <!--<el-dropdown-item>新增</el-dropdown-item>-->
            <!--<el-dropdown-item>删除</el-dropdown-item>-->
          <!--</el-dropdown-menu>-->
        <!--</el-dropdown>-->
        <!--<span>王小虎</span>-->
      <!--</el-header>-->

      <!--<el-main style="border: 1px solid #eee;">-->
        <!--<el-table :data="tableData">-->
          <!--<el-table-column prop="date" label="日期" width="140">-->
          <!--</el-table-column>-->
          <!--<el-table-column prop="name" label="姓名" width="120">-->
          <!--</el-table-column>-->
          <!--<el-table-column prop="address" label="地址">-->
          <!--</el-table-column>-->
        <!--</el-table>-->
      <!--</el-main>-->
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
    // 管理员主界面，负责作不同功能页面指引跳转
    data() {
      const item = {
        // date: '2016-05-02',
        name: sessionStorage.getItem('email'),
        address: sessionStorage.getItem('type')
      };
      return {
        tableData: Array(20).fill(item)
      }
    },
    methods: {
      // 标签管理
      tolabel() {
        this.$router.push('/admin/label')
      },
      // 广告管理
      togetads() {
        this.$router.push('/admin/get_ads')
      },
      // 平台用户管理
      tousers() {
        this.$router.push('/admin/show_users')
      },
      // 社交用户管理
      tocust() {
        this.$router.push('/admin/show_cust')
      }
    }
  };
</script>
