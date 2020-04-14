<template>
  <div style="margin:0px auto; margin-top: 30px">
      <el-input v-model="search" style="display: inline-block;width: 100%" 
        placeholder="请输入搜索内容">
      </el-input>
    <el-table
      :data="tables.slice((currentPage-1)*pagesize,currentPage*pagesize)"
      :cell-style="rowClass"
      :header-cell-style="headClass"
      tooltip-effect="dark"
      style="width: 100%; text-align: center">
      <el-table-column type="expand">
        <template slot-scope="props">
          <span style="backgroud-color: #000000">{{props.row['text']}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="id"
        label='id'
        sortable
        width="80">
      </el-table-column>
      <el-table-column
        prop="belong"
        label="广告主"
        sortable
        width="100">
      </el-table-column>
      <el-table-column
        prop="name"
        label="标题"
        sortable
        width="180">
      </el-table-column>
      <el-table-column
        prop="label"
        label="一级标签"
        sortable
        width="180">
      </el-table-column>
      <el-table-column
        prop="secondary"
        label="关键词"
        sortable
        width="180">
      </el-table-column>
      <el-table-column
        prop="pv"
        label="点击量"
        sortable
        width="100">
      </el-table-column>
      <el-table-column
      fixed="right"
      label="操作">
      <template slot-scope="scope">
        <!-- <el-popover placement="top-start" style="margin-right: 20px" width="400">
          <span style="backgroud-color: #FFFFFF">{{scope.row['text']}}</span>
          <el-button slot="reference" type="text" size="medium">查看</el-button>
        </el-popover> -->
        <el-button @click="delete1(scope.row)" type="text" size="medium">删除</el-button>
      </template>
    </el-table-column>
    </el-table>
    <!-- <vue-good-table
      :columns="columns"
      :rows="tableData"
      style="width: 1000px; text-align: center"/> -->
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
    export default {
      // 查看广告数据
      inject: ['reload'],
      data() {
        return {
          search: '',
          // 翻页功能
          currentPage: 1, // 初始页
          pagesize:10, // 总页数
          form: {
            type: '',
            id : ''
          },
          columns: [
            {
              label: "广告主",
              field: 'belong',
            },
            {
              label: '标题',
              field: 'name',
            },
            {
              label: '一级标签',
              field: 'label',
            },
            {
              label: '关键词',
              field: 'secondary',
            },
            {
              label: '点击量',
              field: 'pv',
            },
          ],
          tableData: []
        }
      },
      methods: {
        // 翻页功能
        handleSizeChange: function (size) {
                this.pagesize = size;
                console.log(this.pagesize)  //每页下拉显示数据
        },
        handleCurrentChange: function(currentPage){
                this.currentPage = currentPage;
                console.log(this.currentPage)  //点击第几页
        },
        headClass() {
          return 'text-align: center;'
        },
        rowClass () {
          return 'text-align: center'
        },
        show(row) {
          console.log(row)
        },
        // 删除广告
        delete1(row) {
          let form1 = {id: row.id}
          console.log(form1)
          this.$http
          // 调用后端删除广告接口
          .post('/delete_ads', form1)
          .then(response => {
            console.log(response.data);
             if (response.data['error_num'] === 0){
                  this.$message({
                  message: response.data['msg'],
                  type: 'success'
                  })
               this.reload();
                }
                else{
                  this.$message.error(response.data['msg'])
                }
          })
          .catch(function (error) { // 请求失败处理
            console.log(error);
          });
        }
      },
      computed: {
        tables () {
          // 搜索功能
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
      mounted() {
        // 获取广告数据并显示
        let __this = this
        // 根据用户类别获取相应广告数据
        // 管理员获取所有广告数据
        // 广告主获取自己的广告数据
        __this.form.type = sessionStorage.getItem('type')
        __this.form.id = sessionStorage.getItem('id')
        let url = ''
        if (__this.form.type === '管理员'){
          // 获取所有广告数据
          url = '/get_ads'
        }
        else {
          // 根据广告主id获取其广告数据
          url = '/get_ads_id'
          console.log(url)
        }
        // 调用后端获取广告数据接口
        this.$http
        .post(url, __this.form)
        .then(response => {
          console.log(url)
          console.log(__this.form.type);
          console.log(response.data);
          // 将广告数据赋值显示
          response.data['list'].forEach(function (item) {
            __this.tableData.push({belong: item['fields']['belong'], name: item['fields']['name'],
              label: item['fields']['label'], pv: Number(item['fields']['pv']), id: item['pk'],
              secondary: item['fields']['secondary1']+', '+item['fields']['secondary2']+', '+item['fields']['secondary3'],
              text: item['fields']['text']
              })
          })
        })
        .catch(function (error) { // 请求失败处理
          console.log(error);
        });
      }
    }
  </script>
