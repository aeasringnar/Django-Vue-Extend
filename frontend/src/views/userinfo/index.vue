<template>
    <div class="app-container">
        <el-table
            :data="page_datas"
            border
            stripe
            style="width: 100%">
            <el-table-column prop="username" label="用户名"></el-table-column>
            <el-table-column prop="realname" label="角色">
                <template slot-scope="scope">
                    <template v-if="scope.row.group != null">
                        <span>{{ scope.row.group.group_type }}</span>
                    </template>
                    <template v-else>
                        <span>无</span>
                    </template>
                </template>
            </el-table-column>
            <el-table-column prop="real_name" label="姓名"/>
            <el-table-column prop="phone" label="手机"/>
            <el-table-column prop="email" label="邮箱"/>
            <el-table-column prop="bf_logo_time" label="上次登录时间" width="155"/>
        </el-table>
    </div>
</template>

<script>
    import store from '@/store'
    import Vue from 'vue'
    import { GetAjax } from '@/api/myapi'
    import datetime from 'date-and-time'

    export default {
        name: "userinfo",
        data () {
            return {
                page_datas: [],
            }
        },
        methods: {
            get_need_data(params) {
                GetAjax('/userinfo/',params).then(response => {
                    const data = response.data
                    console.log(data)
                    this.page_datas.push(data)
                })
            },
        },
        created: function() {
            this.get_need_data()
        }
    }
</script>

<style scoped>
/*.el-upload*/
.avatar-uploader {
    height: 180px;
    width: 250px;
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.avatar-uploader:hover {
    border-color: #409eff;
}
.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 248px;
    height: 178px;
    line-height: 178px;
    text-align: center;
}
.avatar {
    width: 100%;
    height: 180px;
    display: block;
    border-radius: 6px;
}
</style>