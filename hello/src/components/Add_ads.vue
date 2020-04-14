<template>
  <div style="margin:0px auto; margin-top: 60px">
    <span style="color: #409EFF; font-size: 20px">发布广告</span>
    <el-form ref="form" status-icon label-width="80px" :model="form" :rules="rules">
      <el-form-item></el-form-item>
    <el-form-item label="广告标题" prop="name">
      <el-input v-model="form.name" style="width: 600px"></el-input>
    </el-form-item>
    <el-form-item label="广告文本" prop="text">
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
  </div>
</template>


<script>
  export default {
    data() {
      return {
        options: [],
        // name：广告名称
        // text：广告文本内容
        // label：广告标签
        // secondary1，2，3: 广告关键词
        // secondary：三个关键词合成一个字符串
        form: {
          name: '',
          text: '',
          label: '',
          belong: 0,
          secondary1: '',
          secondary2: '',
          secondary3: '',
          secondary: ''
        },
        // 表单验证
        rules: {
          name: [
            {required:true, message:'标题不能为空', trigger:'blur'},
            // {type: 'email', message:'邮箱格式错误', trigger:['change', 'blur']}
          ],
          text: [
            {required:true, message:'文本不能为空',trigger:'blur'}
          ],
          // label: [
          //   {required:true, message: '选择角色', trigger:'blur'}
          // ]
        }
      }
    },
    methods: {
      // 提交表单，
      submitForm(formname) {
        // 提交前先作验证
        this.$refs[formname].validate((valid) => {
          if (valid) {
            let res = this.form['secondary'].split(', ')
            console.log(res)
            this.form['secondary1'] = res[0] 
            this.form['secondary2'] = res[1]
            this.form['secondary3'] = res[2]
            // 调用后端add_ads接口添加广告
            this.$http
              .post('/add_ads', this.form)
              .then(response => {
                if (response.data['error_num'] === 0){
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
      // 清空表单
      resetForm(formName) {
          this.$refs[formName].resetFields();
      },
      // 自动识别，识别广告文本内容分配标签
      identify() {
        console.log(this.form);
        // 后端神经网络接口，作文本识别
        this.$http
            .post('/cnn', this.form)
            .then(response => {
              console.log(response.data);
              this.form['label'] = response.data['label']
              this.form['secondary'] = response.data['secondary']
              let res = this.form['secondary'].split(', ')
              console.log(res)
              this.form['secondary1'] = res[0] 
              this.form['secondary2'] = res[1]
              this.form['secondary3'] = res[2]
              // belong：广告所属广告主id
              // sessionStorage：存储登录用户的信息
              this.form['belong'] = Number(sessionStorage.getItem('id'))
              // this.reload();
            })
            .catch(function (error) {
              console.log(error)
            })
      },
    },
    // 页面加载即运行此函数
    mounted() {
      let __this = this
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

