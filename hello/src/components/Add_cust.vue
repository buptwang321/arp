<template>
  <div style="margin:0px auto; margin-top: 30px">
    <span style="color: #409EFF; font-size: 20px">上传用户</span>
    <el-upload
        style="margin-top: 10px"
        class="upload-demo"
        ref="upload"
        action="http://127.0.0.1:8000/upload_cust"
        :file-list="fileList"
        :auto-upload="false"
        :data="belong">
        <el-button slot="trigger" size="small" type="primary">批量上传</el-button>
        <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
        <div slot="tip" class="el-upload__tip">批量上传社交用户，包括昵称及文本数据等</div>
    </el-upload>
    <el-form ref="form" status-icon label-width="80px" :model="form" :rules="rules">
      <el-form-item></el-form-item>
    <el-form-item label="用户呢称" prop="name">
      <el-input v-model="form.name" style="width: 500px"></el-input>
    </el-form-item>
    <el-form-item label="用户文本" prop="text">
     <el-input type="textarea" rows="5" v-model="form.text" placeholder="添加一条用户文本数据"></el-input>
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
    // 添加社交用户信息
    data() {
      return {
        // 用户所属社交平台id
        belong: {
          belong: sessionStorage.getItem('id'),
        },
        options: [],
        filelist: [],
        // name：用户名称
        // text：用户文本内容
        // label：用户文本标签
        // secondary1，2，3:文本关键词
        // secondary：三个关键词合成一个字符串
        form: {
          name: '',
          text: '',
          belong: 0,
          label: '',
          secondary1: '',
          secondary2: '',
          secondary3: '',
          secondary: ''
        },
        // 表单验证规则
        rules: {
          name: [
            {required:true, message:'标题不能为空', trigger:'blur'},
            // {type: 'email', message:'邮箱格式错误', trigger:['change', 'blur']}
          ],
          text: [
            {required:true, message:'文本不能为空',trigger:'blur'}
          ],
        }
      }
    },
    methods: {
      // 提交添加表单，添加新社交用户
      submitForm(formname) {
        this.$refs[formname].validate((valid) => {
          if (valid) {
            // 调用后端添加新社交用户接口
            this.$http
              .post('/add_cust', this.form)
              // 返回信息
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
            // 为用户添加新文本
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
      // 清空表单
      resetForm(formName) {
          this.$refs[formName].resetFields();
      },
      // 自动识别，识别用户文本内容分配标签
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
              // belong：用户所属社交平台id
              // sessionStorage：存储登录用户的信息
              this.form['belong'] = Number(sessionStorage.getItem('id'))
              // this.reload();
            })
            .catch(function (error) {
              console.log(error)
            })
      },
      // 上传文件，用作批量上传用户
      submitUpload() {
        console.log(this.filelist)
        this.$refs.upload.submit();
        this.$message({
                  message: '上传成功',
                  type: 'success'
                  })
      },
    },
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