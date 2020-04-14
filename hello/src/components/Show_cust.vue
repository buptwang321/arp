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
        prop="belong"
        label='所属'
        sortable
        width="80">
      </el-table-column>
      <el-table-column
        prop="name"
        label="昵称"
        sortable
        width="180">
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
      label="操作"
      width="150">
      <template slot-scope="scope">
        <el-button v-if="type=='平台用户'" style="font-size: 20px" type="text" @click="add(scope.row)"><i class="el-icon-circle-plus-outline"></i></el-button>
        <el-button type="text" @click="update_label(scope.row)">更新标签</el-button>
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
        title="添加"
        :visible.sync="dialogVisible2"
        width="50%"
        @closed="resetForm">
        <el-form ref="form" status-icon label-width="80px" :model="form" :rules="rules">
          <el-form-item label="内容文本" prop="text">
          <el-input type="textarea" rows="5" v-model="form.text" ></el-input>
          </el-form-item>
          <el-form-item label="一级标签" prop="label">
            <el-select v-model="form.label" style="width: 100%" placeholder="请自主选择或自动识别">
              <el-option v-for="item in options"
                    :key="item.label"
                    :label="item.label"
                    :value="item.label">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label='关键词' prop="secondary">
            <el-input v-model="form.secondary"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('form')">添加</el-button>
            <el-button @click="identify">自动识别</el-button>
            <el-button @click="resetForm('form')">取消</el-button>
          </el-form-item>
        </el-form>
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
      inject: ['reload'],
      data() {
        return {
          search: '',
          // 翻页功能
          currentPage: 1, //初始页
          pagesize:10, // 总页数
          type: '',
          options: [],
           dialogVisible2: false,
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
           //  表单验证规则
           rules: {
              name: [
                {required:true, message:'标题不能为空', trigger:'blur'},
                // {type: 'email', message:'邮箱格式错误', trigger:['change', 'blur']}
              ],
              text: [
                {required:true, message:'文本不能为空',trigger:'blur'}
              ],
              label: [
                {required:true, message: '请自动识别', trigger:'blur'}
              ],
              secondary: [
                {required:true, message: '请自动识别', trigger:'blur'}
              ],
            },
           tableData: []
        }
      },
      methods: {
        // 分页功能
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
        add(row) {
          this.dialogVisible2 = true
          this.form['belong'] = row.id
          console.log(row)
        },
        // 自动识别，识别用户文本内容分配标签
        identify() {
        console.log(this.form);
        this.$http
        // 后端神经网络接口，作文本识别
          .post('/cnn', this.form)
          .then(response => {
            console.log(response.data);
            this.form['label'] = response.data['label']
            this.form['secondary'] = response.data['secondary']
            // 将三个关键词连接成一个字符串
            let res = this.form['secondary'].split(', ')
            console.log(res)
            this.form['secondary1'] = res[0] 
            this.form['secondary2'] = res[1]
            this.form['secondary3'] = res[2]
            // this.reload();
          })
          .catch(function (error) {
            console.log(error)
          })
      },
        // 清空重置表单
        resetForm() {
          this.form['text'] = '';
          this.form['label'] = '';
          this.form['secondary'] = ''
        },
        // 社交用户添加新文本内容
        submitForm(formname) {
          this.$refs[formname].validate((valid) => {
            if (valid) {
              let res = this.form['secondary'].split(', ')
              console.log(res)
              this.form['secondary1'] = res[0] 
              this.form['secondary2'] = res[1]
              this.form['secondary3'] = res[2]
              // 调用后端添加新文本接口
              this.$http
                .post('/add_words', this.form)
                .then(response => {
                  if (response.data['error_num'] == 0){
                    this.$message({
                    message: response.data['msg'],
                    type: 'success'
                    })
                  }
                  else{
                    this.$message.error(response.data['msg'])
                  }
                })
                .catch(function (error) {
                  console.log(error)
                })
            } else {
              console.log('error submit!!');
              return false;
            }
          });
        },
        // 更新社交用户兴趣偏好
        update_label(row) {
          this.form['id'] = row.id
          this.$http
            // 调用后端计算用户兴趣偏好接口
            .post('/get_label', this.form)
            .then(response => {
              console.log(response.data);
              let label = response.data['label']
              if (label[0] != null)
                this.form['label1'] = label[0]
              if (label[1] != null)
                this.form['label2'] = label[1]
              if (label[2] != null)
                this.form['label3'] = label[2]
              console.log(this.form)
              this.$http
                .post('/update_label', this.form)
                .then(response => {
                  console.log(response.data);
                  console.log(this.form)
                  this.reload();
                })
                .catch(function (error) {
                  console.log(error)
                })
              // this.reload();
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
        // 显示用户兴趣偏好
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