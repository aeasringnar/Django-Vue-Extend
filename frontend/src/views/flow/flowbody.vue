
<template>
  <div class="app-container">
    <el-row>
      <el-col :span="10">
        <el-button size="small" type="primary" @click="new_data">新增</el-button>
        <!-- <el-button size="small" @click="centerDialog_patch = true">编辑</el-button> -->
      </el-col>
      <el-col :span="4"><p/></el-col>
      <el-col :span="4">
        <el-select size="small" v-model="my_pagination.search_type" placeholder="请选择" style="width: 100%" @change="my_change">
          <el-option label="全部分类" value=""/>
          <el-option label="测试分类" value="0"/>
          <el-option label="测试分类" value="1"/>
        </el-select>
      </el-col>
      <el-col :span="6">
        <mysearch v-model="my_pagination.search" @searchData="to_search"/>
      </el-col>
    </el-row>
    <br>
    <el-table
      :data="page_datas"
      border
      stripe
      style="width: 100%">
      <el-table-column prop="id" label="ID"/>
      <el-table-column prop="abstract" label="摘要"/>
      <el-table-column prop="user.username" label="申请人"/>
      <el-table-column prop="flow_file" label="附件"/>
      <el-table-column prop="content" label="备注"/>
      <el-table-column fixed="right" label="操作" width="100" align="center">
        <template slot-scope="scope">
          <el-row>
            <el-button size="small" @click="edit_data(scope.row)">编辑</el-button>
          </el-row>
          <el-row style="margin-top: 10px;">
            <el-button size="small" type="danger" @click="delete_data_fuc(scope.row)">删除</el-button>
          </el-row>
        </template>
      </el-table-column>
    </el-table>
    <br>
    <pagination :total="my_pagination.count" :page.sync="my_pagination.page" :page_size.sync="my_pagination.page_size" @pagination="pag_change"/>

    <el-dialog
      :visible.sync="centerDialog"
      v-dialogDrag
      title="新增"
      width="50%"
      center>
      <div>
        <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="100px">
          <el-form-item label="摘要" prop="abstract">
            <el-input size="small" v-model="ruleForm.abstract"/>
          </el-form-item>
          <el-form-item label="审批流" prop="approval_flow">
            <el-select size="small" v-model="ruleForm.approval_flow" placeholder="请选择" filterable clearable style="width: 100%;">
              <el-option v-for="data in appflow_datas" :key="data.id" :label="data.name" :value="data.id"/>
            </el-select>
          </el-form-item>
          <el-form-item label="附件">
            <upload-file v-model="ruleForm.flow_file"/>
          </el-form-item>
          <el-form-item label="备注">
            <el-input size="small" v-model="ruleForm.content" type="textarea"/>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button size="small" @click="resetForm('ruleForm')">取 消</el-button>
        <el-button size="small" type="primary" @click="submitForm('ruleForm')">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :visible.sync="centerDialog_delete"
      v-dialogDrag
      title="确认删除"
      width="30%"
      center>
      <span>是否确认删除，删除后不可恢复？</span>
      <span slot="footer" class="dialog-footer">
        <el-button size="small" @click="centerDialog_delete = false">取 消</el-button>
        <el-button size="small" type="primary" @click="true_delete">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :visible.sync="centerDialog_patch"
      title="编辑"
      width="50%"
      center>
      <div>
        <el-form ref="ruleForm_patch" :model="ruleForm_patch" :rules="rules_patch" label-width="100px">
          <el-form-item label="摘要" prop="abstract">
            <el-input size="small" v-model="ruleForm_patch.abstract"/>
          </el-form-item>
          <el-form-item label="附件">
            <upload-file v-model="ruleForm_patch.flow_file"/>
          </el-form-item>
          <el-form-item label="备注">
            <el-input size="small" v-model="ruleForm_patch.content" type="textarea"/>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button size="small" @click="resetForm('ruleForm_patch')">取 消</el-button>
        <el-button size="small" type="primary" @click="submitForm('ruleForm_patch')">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<style>
.el-table .cell .el-tooltip {
  white-space: pre-line;
}
</style>
<script>
import store from '@/store'
import Vue from 'vue'
import { GetAjax, PostAjax, PatchAjax, DeleteAjax } from '@/api/myapi'
import datetime from 'date-and-time'
import Mysearch from '@/components/SearchField/index2.vue'
import Pagination from '@/components/Pagination'
import UploadImage from '@/components/Upload/singleImage.vue'
import UploadFile from '@/components/Upload/singleFile.vue'
// import Tinymce from '@/components/Tinymce/index.vue'

export default {
  name: 'flowbodyManage',
  components: { Mysearch, Pagination, UploadImage, UploadFile },
  data() {
    return {
      centerDialog: false,
      centerDialog_delete: false,
      centerDialog_patch: false,
      page_datas: [],
      ruleForm: {
        approval_flow: '',
        content: '',
        abstract: '',
        flow_file: ''
      },
      rules: {
        abstract: [
          { required: true, message: '请输入摘要', trigger: 'blur' }
        ],
        approval_flow: [
          { required: true, message: '请选择审批流', trigger: 'change' }
        ],
      },
      ruleForm_patch: {
        approval_flow: '',
        content: '',
        abstract: '',
        flow_file: ''
      },
      rules_patch: {
        abstract: [
          { required: true, message: '请输入摘要', trigger: 'blur' }
        ],
      },
      delete_data: {},
      my_pagination: {
        page: 1,
        page_size: 10,
        count: 0,
        search: '',
        search_type: '',
      },
      appflow_datas: []
    }
  },
  created: function() {
    this.get_need_data(this.my_pagination)
    this.get_appflow_data()
  },
  methods: {
    get_need_data(params) {
      GetAjax('/flowbody/', params).then(response => {
        const data = response.data
        console.log(data)
        this.page_datas = data
        this.my_pagination.count = response.count
      })
    },
    get_appflow_data(params) {
      GetAjax('/approvalflow/', params).then(response => {
        const data = response.data
        console.log(data)
        this.appflow_datas = data
      })
    },
    post_need_data(data) {
      PostAjax('/flowbody/', data).then(response => {
        const data = response.data
        console.log(data)
        this.centerDialog = false
        this.$refs['ruleForm'].resetFields()
        this.$message({
          showClose: true,
          message: '新增成功！',
          type: 'success'
        })
        this.get_need_data(this.my_pagination)
      })
    },
    patch_need_data(data) {
      PatchAjax('/flowbody/' + data.id + '/', data).then(response => {
        const data = response.data
        console.log(data)
        this.centerDialog_patch = false
        this.$refs['ruleForm'].resetFields()
        this.$message({
          showClose: true,
          message: '修改成功！',
          type: 'success'
        })
        this.get_need_data(this.my_pagination)
      })
    },
    delete_need_data(data) {
      DeleteAjax('/flowbody/' + data.id + '/', data).then(response => {
        const data = response.data
        console.log(data)
        this.centerDialog_delete = false
        this.$message({
          showClose: true,
          message: '删除成功！',
          type: 'success'
        })
        this.get_need_data(this.my_pagination)
      })
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (formName == 'ruleForm') {
            // datetime.format(this.ruleForm.date, 'YYYY-MM-DD')
            // console.log(datetime.format(this.ruleForm.time, 'hh:mm:ss'))
            console.log(this.ruleForm)
            this.post_need_data(this.ruleForm)
          } else {
            console.log(this.ruleForm_patch)
            this.patch_need_data(this.ruleForm_patch)
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // form数据验证
    resetForm(formName) {
      console.log(formName)
      this.centerDialog = false
      this.centerDialog_patch = false
      this.$refs[formName].resetFields()
    },
    // 删除按钮
    delete_data_fuc(row) {
      console.log(row)
      this.delete_data = row
      this.centerDialog_delete = true
    },
    // 新增按钮
    new_data() {
      this.centerDialog = true
    },
    // 确定删除按钮
    true_delete() {
      this.delete_need_data(this.delete_data)
    },
    // 编辑按钮
    edit_data(row) {
      console.log(row)
      this.ruleForm_patch = JSON.parse(JSON.stringify(row))
      this.centerDialog_patch = true
    },
    // 搜索层相关
    to_search() {
      this.my_pagination.page = 1
      console.log(this.my_pagination.search)
      // this.get_need_data(this.my_pagination)
    },
    pag_change() {
      console.log(this.my_pagination)
      // this.get_need_data(this.my_pagination)
    },
    search_change() {
      console.log(this.my_pagination.search)
      this.get_need_data(this.my_pagination)
    },
    my_change(val) {
      this.my_pagination.page = 1
      this.my_pagination.search_type = val
      console.log(this.my_pagination.search_type)
      this.get_need_data(this.my_pagination)
    }
  }
}
</script>

<style scoped>
</style>  
