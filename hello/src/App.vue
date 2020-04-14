<template>
  <!--<div id="app">-->
    <!--<div id="nav">-->
      <!--<router-link to="/">Home</router-link> |-->
      <!--&lt;!&ndash;<router-link to="/about">About</router-link>&ndash;&gt;-->
    <!--</div>-->
    <!--<router-view/>-->
  <!--</div>-->
  <div id="app">
    <el-container>
      <el-header style="padding: 0; height: 60px; text-align: center; background-color: #FFFFFF; color: #409EFF; border-bottom: 1px solid #eee;">
        <el-row>
           <el-col :span="10"><div style="font-size: 30px; line-height: 60px; font-family: 'Helvetica Neue'; margin-left: 60px; float: left">
             <i class="el-icon-s-data"></i>ARP</div>
           </el-col>
          <el-col :span="4">
            <el-button style="font-size: 20px; line-height: 30px" type="text" @click="dialogVisible = true">快速识别TEST</el-button>
            <el-dialog
              title="智能识别"
              :visible.sync="dialogVisible"
              width="40%"
              @closed="resetForm">
              <el-form label-width="80px" :model="identify_data">
                <el-form-item label="输入文本" prop="text">
                  <el-input rows="5" type="textarea" v-model="identify_data.text"></el-input>
                </el-form-item>
                <el-form-item label="识别结果" prop="result">
                  <el-input v-model="identify_data.result" readonly="readonly"></el-input>
                </el-form-item>
                <el-form-item label="关键词" prop="secondary">
                  <el-input v-model="identify_data.secondary" readonly="readonly"></el-input>
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button @click="resetForm">取 消</el-button>
                <el-button type="primary" @click="identify">识 别</el-button>
              </span>
            </el-dialog>
          </el-col>
          <!--<el-col :span="14"><div style="line-height: 60px">&nbsp;?</div></el-col>-->
          <el-col :span="10" v-if="user.email!=null"><div style="font-size: 20px; line-height: 60px; color: #409EFF; float: right">
            <span style="margin-right: 15px;">{{user.type}}</span>
            <span style="margin-right: 15px; color: #C0C4CC;">|</span>
            <span style="margin-right: 15px;">{{user.email}}</span>
            <el-dropdown>
              <i class="el-icon-arrow-down" style="margin-right: 30px"></i>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>查看</el-dropdown-item>
                <el-dropdown-item>新增</el-dropdown-item>
                <el-dropdown-item><div @click="logout">登出</div></el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>

          </div></el-col>
          <!--<el-col :span="24"><div style="font-size: 20px; line-height: 60px">标题</div></el-col>-->
          <!--<el-col :span="24"><div style="font-size: 20px; line-height: 60px">标题</div></el-col>-->
        </el-row>
         <!--<el-row style="height: 60px; background: #99a9bf">-->
           <!--<el-col :span="24"><div style="font-size: 24px">???</div></el-col>-->
        <!--</el-row>-->
      </el-header>
      <el-main style="padding: 0;">
        <router-view v-if="isRouterAlive"></router-view>
      </el-main>
    </el-container>
  </div>

</template>

<style>
/*#app {*/
  /*font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
  /*-webkit-font-smoothing: antialiased;*/
  /*-moz-osx-font-smoothing: grayscale;*/
  /*text-align: center;*/
  /*color: #2c3e50;*/
/*}*/

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

  /*.el-header {*/
    /*background-color: #B3C0D1;*/
    /*color: #333;*/
    /*text-align: center;*/
    /*line-height: 60px;*/
    /*padding: 0;*/
  /*}*/
  /*.el-main{*/
    /*background-color: #E9EEF3;*/
    /*color: #333;*/
    /*text-align: center;*/
    /*padding: 0;*/
    /*!*line-height: 160px;*!*/
  /*}*/
</style>

<script>
import LabelWrap from "element-ui/packages/form/src/label-wrap";
export default {
  components: {LabelWrap},
  provide () {
    return {
      reload: this.reload
    }
  },
  data(){
    return{
      dialogVisible: false,
      isRouterAlive: true,
      user: {
        email: sessionStorage.getItem('email'),
        type: sessionStorage.getItem('type'),
        id: sessionStorage.getItem('id')
      },
      identify_data: {
        text: '',
        result: '',
        secondary: ''
      }
    }
  },
  methods: {
    logout: function () {
      console.log('???');
      sessionStorage.clear();
      this.user.email = null;
      this.$router.push('/')
    },
    reload() {
      this.isRouterAlive = false;
      this.$nextTick(function() {
         this.isRouterAlive = true
      })
    },
    identify() {
      console.log(this.identify_data);
      this.$http
          .post('/cnn', this.identify_data)
          .then(response => {
            console.log(response.data);
            this.identify_data['result'] = response.data['label']
            this.identify_data['secondary'] = response.data['secondary']
            // this.reload();
          })
          .catch(function (error) {
            console.log(error)
          })
    },
    resetForm() {
      console.log(this.$refs['identify_data']);
      this.identify_data['text'] = '';
      this.identify_data['result'] = '';
      this.identify_data['secondary'] = ''
      // this.$nextTick(()=> {
      //   this.$refs['identify_data'].resetFields()
      // });
      // if (this.$refs[formName] !== undefined){
      //   this.$refs[formName].resetFields()
      // }

    }
  },
  mounted() {
    this.reload()
  }
}
</script>
