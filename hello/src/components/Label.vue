<template>
  <div style="margin:0px auto; margin-top: 60px">
    <span style="color: #409EFF; font-size: 20px">一级标签页</span>
  <el-form label-position="top">
    <el-form-item></el-form-item>
    <el-form-item label="标签说明">
      <el-tag type="success">可用标签</el-tag>
      <el-tag type="danger">禁用标签</el-tag>
      <el-tag type="warning">未训练标签</el-tag>
    </el-form-item>
    <el-form-item label="标签库">
      <el-popover placement="top" trigger="hover"
                  style="margin-right: 10px"
                  :key="tag.name"
                  :type="tag.type"
                  v-for="tag in dynamicTags">
        <el-form label-position="top">
          <el-form-item label="上传语料"></el-form-item>
          <el-upload
            class="upload-demo"
            ref="upload"
            action="https://jsonplaceholder.typicode.com/posts/"
            :auto-upload="false">
            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success">上传到服务器</el-button>
            <!--<div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>-->
          </el-upload>
          <el-form-item label="状态设置">
            <el-button v-if="tag.type=='success'" size="small" type="danger" @click="update_use(tag.name, 0)">禁用</el-button>
            <el-button v-if="tag.type=='danger'" size="small" type="success" @click="update_use(tag.name, 1)">启用</el-button>
            <span v-if="tag.type=='warning'" style="color: #909399">标签不可用</span>
          </el-form-item>
        </el-form>
         <el-tag
            slot="reference"
            :key="tag.name"
            :type="tag.type"
            closable
            :disable-transitions="false"
            @close="handleClose(tag)">
            {{tag.name}}
          </el-tag>
      </el-popover>

    </el-form-item>
    <el-form-item label="新增标签">
      <el-input
      class="input-new-tag"
      v-if="inputVisible"
      v-model="inputValue"
      ref="saveTagInput"
      size="small"
      @keyup.enter.native="handleInputConfirm"
      @blur="handleInputConfirm"
    >
    </el-input>
    <el-button v-else class="button-new-tag" size="small" @click="showInput" type="primary">+ New Tag</el-button>
    </el-form-item>

  </el-form>
  </div>

</template>

<style>
  .el-tag + .el-tag {
    margin-left: 10px;
  }
  .button-new-tag {
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }
  .input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }
</style>

<script>
  function to_type(t, a) {
    // 根据标签状态在页面显示不同颜色
    if (a == 1)
      return 'success'; // 可用标签
    else {
      if (t == 1)
        return 'danger'; // 禁用标签
      else
        return 'warning'; // 未训练标签
    }
  }
  export default {
    inject: ['reload'],
    data() {
      return {
        // name：标签名称
        // trained：是否被训练
        // availabel：是否可用
        form: {
          name: '',
          trained: 0,
          available: 0
        },
        dynamicTags: [],
        // 控制输入框显示
        inputVisible: false,
        inputValue: ''
      };
    },
    methods: {
      handleClose(tag) {
        this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
      },
      // 显示输入框
      showInput() {
        this.inputVisible = true;
        this.$nextTick(_ => {
          this.$refs.saveTagInput.$refs.input.focus();
        });
      },
      // 添加新标签
      handleInputConfirm() {
        let inputValue = this.inputValue;
        this.form.name = inputValue;
        if (inputValue) {
          this.$http
            // 调用后端添加新标签接口 
            .post('/add_label', this.form)
            .then(response => (console.log(response.data)))
            .catch(function (error) { // 请求失败处理
              console.log(error);
            });
          this.dynamicTags.push({name: inputValue, type: to_type(this.form.trained, this.form.available)});
        }
        this.inputVisible = false;
        this.inputValue = '';
      },
      // 更新标签状态
      update_use(name, state) {
        let update = {name: name, available: state};
        this.$http
          .post('/update_use', update)
          .then(response => {
            console.log(response.data);
            this.reload();
          })
          .catch(function (error) {
            console.log(error)
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
          __this.dynamicTags.push({name: item['fields']['name'],
            type: to_type(item['fields']['trained'], item['fields']['available'])})
        })
      })
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
    }
  }
</script>
