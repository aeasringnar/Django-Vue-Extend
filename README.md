# django-vue-extend

基于 django 2.x + vue2.x 的 集成项目

## 技术栈

- **后端框架**：基于 Django 2.X + django-rest-framework
- **前端框架**：基于 Vue 2.X + Element UI
- **数据模型**：基于 PyMySQL 存储
- **授权验证**：基于 JWT
- **内置功能**：个人中心、用户管理、权限管理、审批流&审批流管理等

### 本地开发

开启服务端

```bash
$ cd backend
$ pip install -r requirements.txt
$ python manage.py ruserver
$ open http://localhost:9000/
```

开启前端

```bash
$ npm install
$ npm run dev
```