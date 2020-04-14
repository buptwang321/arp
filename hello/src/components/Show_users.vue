<template>
  <div style="margin:0px auto; margin-top: 30px">
    <el-input v-model="search" style="display: inline-block;width: 100%" 
        placeholder="请输入搜索内容">
    </el-input>
    <el-table
      :data="tables.slice((currentPage-1)*pagesize,currentPage*pagesize)"
      :cell-style="rowClass"
      :header-cell-style="rowClass"
      style="width: 100%; text-align: center">
      <el-table-column
        prop="id"
        label='id'
        sortable
        width="80">
      </el-table-column>
      <el-table-column
        prop="email"
        label="邮箱"
        width="250">
      </el-table-column>
      <el-table-column
        prop="type"
        label="类别"
        sortable
        width="180">
      </el-table-column>
      <el-table-column
        prop="company"
        label="公司"
        sortable
        width="220">
      </el-table-column>
      <el-table-column
      fixed="right"
      label="操作"
      width="220">
      <template slot-scope="scope">
        <el-popover placement="top-start" style="margin-right: 20px" width="400">
          <span style="backgroud-color: #FFFFFF">{{scope.row['text']}}</span>
          <el-button slot="reference" type="text" size="medium">查看</el-button>
        </el-popover>
        <el-button @click="delete(scope.row)" type="text" size="medium">删除</el-button>
      </template>
    </el-table-column>
    </el-table>
    <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[5, 10, 20, 40]" 
            :page-size="pagesize"        
            layout="total, sizes, prev, pager, next, jumper"
            :total="tableData.length"
            style="float: right; margin-top: 15px">
      </el-pagination>
  </div>
  </template>

  <script>
    function to_type(a) {
      if (a === 0)
        return "管理员"
      else if (a === 1)
        return "社交平台"
      else
        return "广告主"
    }
    export default {
      // 显示平台用户数据
      data() {
        // 翻页功能
        return {
          search: '',
          currentPage: 1, //初始页
          pagesize:10,
          tableData: []
        }
      },
      // 
      methods: {
        handleSizeChange: function (size) {
                this.pagesize = size;
                console.log(this.pagesize)  //每页下拉显示数据
        },
        handleCurrentChange: function(currentPage){
                this.currentPage = currentPage;
                console.log(this.currentPage)  //点击第几页
        },
        rowClass () {
          return 'text-align: center;'
        },
        show(row) {
          console.log(row)
        }
      },
      computed: {
        tables () {
          const search = this.search
          if (search) {
            // filter() 方法创建一个新的数组，新数组中的元素是通过检查指定数组中符合条件的所有元素。
            // 注意： filter() 不会对空数组进行检测。
            // 注意： filter() 不会改变原始数组。
            return this.tableData.filter(data => {
              // some() 方法用于检测数组中的元素是否满足指定条件;
              // some() 方法会依次执行数组的每个元素：
              // 如果有一个元素满足条件，则表达式返回true , 剩余的元素不会再执行检测;
              // 如果没有满足条件的元素，则返回false。
              // 注意： some() 不会对空数组进行检测。
              // 注意： some() 不会改变原始数组。
              return Object.keys(data).some(key => {
                // indexOf() 返回某个指定的字符在某个字符串中首次出现的位置，如果没有找到就返回-1；
                // 该方法对大小写敏感！所以之前需要toLowerCase()方法将所有查询到内容变为小写。
                return String(data[key]).toLowerCase().indexOf(search) > -1
              })
            })
          }
          return this.tableData
        }
      },
      // 获取平台用户数据
      mounted() {
        let __this = this
        this.$http
        // 调用后端获取平台用户数据接口
        // 包括id，email，type（角色）和company（所属公司）
        .post('/show_users')
        .then(response => {
          console.log(response.data);
          response.data['list'].forEach(function (item) {
            __this.tableData.push({id: item['pk'], email: item['fields']['email'],
              type: to_type(item['fields']['type']), company: item['fields']['company']})
          })
        })
        .catch(function (error) { // 请求失败处理
          console.log(error);
        });
      }
    }
  </script>