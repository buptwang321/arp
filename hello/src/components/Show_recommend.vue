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
        prop="name"
        label="昵称"
        sortable
        width="220">
      </el-table-column>
      <el-table-column
        prop="label1"
        label="🏷️1"
        sortable
        width="150">
      </el-table-column>
      <el-table-column
        prop="label2"
        label="🏷️2"
        sortable
        width="150">
      </el-table-column>
      <el-table-column
        prop="label3"
        label="🏷️3"
        sortable
        width="150">
      </el-table-column>
      <el-table-column
      fixed="right"
      label="查看推荐"
      width="180">
      <template slot-scope="scope">
        <el-button v-if="type=='平台用户'" style="font-size: 30px;" type="text" @click="recommend(scope.row)">
            <i class="el-icon-s-comment"></i>
        </el-button>
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
    <el-dialog
        title="推荐广告"
        :visible.sync="dialogVisible2"
        width="80%">
        <el-table
            :data="tableAds"
            :cell-style="rowClass"
            :header-cell-style="rowClass"
            style="text-align: center">
            <el-table-column type="expand">
                <template slot-scope="props">
                <span>{{props.row['text']}}</span>
                </template>
            </el-table-column>
            <el-table-column
                prop="name"
                label="标题">
            </el-table-column>
            <el-table-column
                prop="secondary"
                label="关键词">
            </el-table-column>
            <el-table-column
                fixed="right"
                label="喜欢">
                <template slot-scope="scope">
                    <el-button  @click="like(scope.row)" type="text" 
                        style="font-size: 30px;" size="medium">
                        <i class="el-icon-finished"></i>
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </el-dialog>
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
      // 对用户进行广告推荐
      inject: ['reload'],
      data() {
        return {
          search: '',
          currentPage: 1, //初始页
          pagesize:10, // 总页数
            dialogVisible2: false,
            type: '',
            options: [],
            // 社交用户个人信息
            // id：用户id
            // belong：所属社交平台id
            // label1，2，3: 用户前三兴趣标签
            // text：用户文本内容
            // secondary1，2，3: 文本内容三个关键词 
            form: {
                id: 0,
                text: '',
                belong: 0,
                label: '',
                secondary1: '',
                secondary2: '',
                secondary3: '',
                secondary: '',
                label1: '',
                label2: '',
                label3: ''
            },
            tableData: [],
            tableAds: [],
            like_form: {
              cust_id: 0,
              ads_id: 0
            }
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
        rowClass () {
          return 'text-align: center;'
        },
        // 点击喜欢功能
        like(row) {
          this.like_form.ads_id = row.id
          this.$http
          // 调用后端用户-广告喜欢功能
          .post('/add_like', this.like_form)
          .then(response => {
            this.$message({
                  message: '喜欢'+row.id,
                  type: 'success'
                  })
            console.log(response.data);
          })
          .catch(function (error) {
            console.log(error)
          })
            
        },
        // 对用户进行广告推荐
        recommend(row) {
            let __this = this
            this.dialogVisible2 = true
            this.tableAds = []
            let temp = {"id": row.id}
            this.like_form.cust_id = row.id
            this.$http
            // 调用后端获取推荐接口
            .post('/get_recommend', temp)
            .then(response => {
                console.log(response.data);
                // 获取推荐结果
                response.data['res'].forEach(function (item) {
                    __this.tableAds.push({name: item['fields']['name'],
                        text: item['fields']['text'], id: item['pk'],
                        secondary: item['fields']['secondary1']+', '+item['fields']['secondary2']+', '+item['fields']['secondary3'],})
                })
                // this.reload();
                console.log(this.tableAds)
            })
            .catch(function (error) {
                console.log(error)
            })
            
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
      // 显示社交用户数据
      // 包括id，name，belong，label1，2，3（兴趣偏好前三）
      mounted() {
        this.type = sessionStorage.getItem('type')
        let __this = this
        this.$http
        .post('/get_cust')
        .then(response => {
          console.log(response.data);
          response.data['list'].forEach(function (item) {
            __this.tableData.push({id: item['pk'], name: item['fields']['name'],
              belong: item['fields']['belong'], label1: item['fields']['label1'],
              label2: item['fields']['label2'], label3: item['fields']['label3']})
          })
        })
        .catch(function (error) { // 请求失败处理
          console.log(error);
        });

        this.$http
        .post('/show_labels')
        .then(response => {
          console.log(response.data['list']);
          response.data['list'].forEach(function (item) {
            __this.options.push({label: item['fields']['name'],
              value: item['fields']['id']})
          })
        })
        .catch(function (error) { // 请求失败处理
          console.log(error);
        });
        }
    }
  </script>