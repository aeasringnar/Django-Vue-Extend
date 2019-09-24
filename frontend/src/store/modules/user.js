import { login, logout, getInfo } from '@/api/login'
import { getToken, setToken, removeToken } from '@/utils/auth'
import router from '../../router'

// 自动权限
const whiteList = ['/login','/404','/','*','/dashboard']
function handleRouter(routers) {
  console.log('查看是否执行')
  for (var i in routers) {
    if (routers[i].children && routers[i].children.length > 0) {
      handleRouter(routers[i].children)
      var len = routers[i].children.length
      var false_len = 0
      for (let j in routers[i].children) {
        if (routers[i].children[j].hidden) {
            false_len ++
        }
      }
      if (len == false_len) {
        routers[i].hidden = true
      } else {
        routers[i].hidden = false
      }
  } else {
    if (whiteList.indexOf(routers[i].path) == -1) {
      if(state.auth_json[routers[i].name]) {
        if (state.auth_json[routers[i].name].auth_list) {
          routers[i].hidden = false
        } else {
          routers[i].hidden = true
        }
      } else {
        routers[i].hidden = true
      }
    }
    }
  }
}

const user = {
  state: {
    token: getToken(),
    name: '',
    avatar: '',
    roles: '',
    auth_json: {},
    routers: router,
    user_obj: {},
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_USER_OBJ: (state, user_obj) => {
      state.user_obj = user_obj
    },
    SET_NAME: (state, name) => {
      state.name = name
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
    },
    SET_AUTHS: (state, auths) => {
      var auth_obj = {}
      for (let i in auths) {
        auth_obj[auths[i].object_name] = {
          auth_create: auths[i].auth_create,
          auth_list: auths[i].auth_list,
          auth_update: auths[i].auth_update,
          auth_destroy: auths[i].auth_destroy
        }
      }
      state.auth_json = auth_obj
    },
    SET_ROUTE: (state, routers) => {
      console.log(JSON.stringify(routers))
      
      handleRouter(routers)
      console.log(JSON.stringify(routers))
      state.routers = routers
    }
  },

  actions: {
    // 登录
    Login({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        login(userInfo).then(response => {
          const data = response.data
          setToken(data.token)
          commit('SET_TOKEN', data.token)
          resolve()
        }).catch(error => {
          reject(error)
          // alert(error)
        })
      })
    },

    // 获取用户信息
    GetInfo({ commit, state }) {
      return new Promise((resolve, reject) => {
        getInfo().then(response => {
          const data = response.data
          console.log(data)
          commit('SET_USER_OBJ', data)
          commit('SET_NAME', data.username)
          commit('SET_ROLES', data.group.group_type)
          commit('SET_AVATAR', data.img_url)
          if (data.group.group_type !== 'SuperAdmin') {
            commit('SET_AUTHS', data.auth.auth_permissions)
            console.log('查看auths：', state.auth_json)
            // commit('SET_ROUTE', router)
            // handleRouter(router)
          }
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 登出
    LogOut({ commit, state }) {
      return new Promise((resolve, reject) => {
        logout(state.token).then(() => {
          commit('SET_TOKEN', '')
          commit('SET_ROLES', [])
          removeToken()
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 前端 登出
    FedLogOut({ commit }) {
      return new Promise(resolve => {
        commit('SET_TOKEN', '')
        removeToken()
        resolve()
      })
    }
  }
}

export default user
