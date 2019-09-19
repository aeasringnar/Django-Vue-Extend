const path = require('path');
const fs = require('fs');
const vueCode = require('./codeStr');
const router = require('./routerStr');
// console.log(__dirname);  // 当前文件所在的绝对路径。
// console.log(__filename);  // 当前文件的文件名,包括全路径。  __dirname和__filename都是全局对象。


// 写入主体
var obj_list = [
    {
        dir_name:'system',
        dir_name_cn:'系统管理',
        childs: [
            {
                object_name:'user',
                object_name_cn:'用户管理',
                fields:[
                    {prop:'id',label:'ID'},
                    {prop:'username',label:'用户名'},
                    {prop:'phone',label:'手机号'},
                    {prop:'email',label:'邮箱'},
                    {prop:'real_name',label:'姓名'},
                    {prop:'group.group_type',label:'角色'},
                    {prop:'bf_logo_time',label:'上次登录时间'},
                ]
            },
            {
                object_name:'auth',
                object_name_cn:'权限管理',
                fields:[
                    {prop:'id',label:'ID'},
                    {prop:'auth_type',label:'权限名称'},
                ]
            }
        ]
    },
    {
        dir_name:'flow',
        dir_name_cn:'审批流',
        childs: [
            {
                object_name:'flowgroup',
                object_name_cn:'审批组管理',
                fields:[
                    {prop:'id',label:'ID'},
                    {prop:'name',label:'审批组名称'},
                    {prop:'users',label:'组内用户'},
                ]
            },
            {
                object_name:'approvalflow',
                object_name_cn:'审批流设置',
                fields:[
                    {prop:'id',label:'ID'},
                    {prop:'name',label:'审批名称'},
                ]
            },
            {
                object_name:'flowbody',
                object_name_cn:'审批主体',
                fields:[
                    {prop:'id',label:'ID'},
                    {prop:'abstract',label:'摘要'},
                    {prop:'user.username',label:'申请人'},
                    {prop:'flow_file',label:'附件'},
                    {prop:'content',label:'备注'},
                ]
            }
        ]
    }
]


// 写入vue文件的函数
function writeCode(dir_path, data) {
    const file_path = dir_path + '/' + data.object_name + '.vue'
    fs.writeFile(file_path, vueCode.creatCode(data), (err) => {
        if (err) throw err;
        console.log('文件:' + String(file_path) + '已被保存...');
    });
}

// 写入路由文件的函数
function writeRouter(file_path, data) {
    fs.writeFile(file_path, data, (err) => {
        if (err) throw err;
        console.log('文件:' + String(file_path) + '已被保存...');
    });
}

// 主体函数
function creatCode(obj_list) {
    for (let i in obj_list) {
        // 创建目录
        const base_path = __dirname + '/my_view'
        const dir_path = base_path + '/' + obj_list[i].dir_name
        const router_path = base_path + '/router.js'
        fs.mkdir(dir_path, { recursive: true }, (err) => {
            if (err) throw err;
            for (let j in obj_list[i].childs) {
                writeCode(dir_path, obj_list[i].childs[j])
            }
            writeRouter(router_path, router.creatRouter(obj_list))
        });
    }
}

// 运行主体函数
creatCode(obj_list)
