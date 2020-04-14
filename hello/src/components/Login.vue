<template>
  <div style="width: 30%; margin: 0px auto; margin-top: 200px">
  <el-form ref="form" status-icon :model="form" :rules="rules" label-width="80px">
    <el-form-item label="邮箱" prop="email">
      <el-input v-model="form.email"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password">
     <el-input type="password" v-model="form.password" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="登陆角色" prop="type">
      <el-radio-group v-model="form.type">
        <el-radio label="平台用户"></el-radio>
        <el-radio label="广告主"></el-radio>
        <el-radio label="管理员"></el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('form')">进入系统</el-button>
      <el-button @click="resetForm('form')">取消</el-button>
    </el-form-item>
  </el-form>
    </div>
</template>

<script>
  export default {
    // 用户登录
    inject: ['reload'],
    data() {
      return {
        // 登录信息
        // email：登录邮箱
        // password：登录密码
        // type：登录角色类型
        form: {
          email: '',
          password: '',
          type: ''
        },
        // 表单验证规则
        rules: {
          email: [
            {required:true, message:'邮箱不能为空', trigger:'blur'},
            // {type: 'email', message:'邮箱格式错误', trigger:['change', 'blur']}
          ],
          password: [
            {required:true, message:'密码不能为空',trigger:'blur'}
          ],
          type: [
            {required:true, message: '选择角色', trigger:'blur'}
          ]
        }
      }
    },
    methods: {
      // 登录，提交表单
      submitForm(formname) {
        this.$refs[formname].validate((valid) => {
          if (valid) {
            // 调用后端验证登录信息接口
            this.$http
              .post('/check', this.form)
              .then(response => {
                // 信息验证成功
                if (response.data['error_num'] == 0){
                  this.$message({
                  message: response.data['msg'],
                  type: 'success'
                  })
                  console.log(response.data['data'])
                  // 将用户个人信息存入sessionStorage
                  sessionStorage.setItem('email', response.data['data']['email'])
                  sessionStorage.setItem('type', response.data['data']['type'])
                  sessionStorage.setItem('id', response.data['id'])
                  // this.$set();
                  console.log(response.data['id'])
                  // 根据用户角色跳转至相应主页
                  if (response.data['data']['type'] === '管理员'){
                    this.$router.push('/admin');
                  }
                  else if (response.data['data']['type'] === '广告主'){
                    this.$router.push('/advertisers');
                  }
                  else {
                    this.$router.push('/platforms');
                  }
                  this.$router.go(0)
                }
                // 信息验证失败，返回对应错误提示
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
      }
    },
    mounted() {
      this.$http
      .post('/show_users')
      .then(response => (console.log(response.data)))
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
    }
  }
</script>
