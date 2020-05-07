import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: [],
    users: [],
  },
  mutations: {
    AUTH_REQUEST(state, users) {
      state.status = 'loading'
      state.users = users
    },
    AUTH_SUCCES(state, token, user) {
      state.status = 'success'
      state.token = token
      state.user = user
    },
    AUTH_ERROR(state) {
      state.status = 'error'
    },
    LOGOUT(state) {
      state.status = ''
      state.token = ''
    },
    DELETE_USER(state) {
      state.users = ''
    }
  },
  actions: {
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('AUTH_REQUEST')
        axios({
          url: '/api/auth/login',
          data: user,
          method: 'POST'
        })
          .then(resp => {
            const token = resp.data.username
            const user = resp.data
            localStorage.setItem('token', token)
            axios.defaults.headers.common['Authorization'] = token
            commit('AUTH_SUCCES', token)
            commit('AUTH_SUCCES', user)
            resolve(resp)
          })
          .catch(err => {
            commit('AUTH_ERROR')
            localStorage.removeItem('token')
            reject(err)
          })
      })
    },
    register({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('AUTH_REQUEST')
        axios({
          url: '/api/auth/register',
          data: user,
          method: 'POST'
        })
          .then(resp => {
            const token = resp.data.username
            const user = resp.data
            localStorage.setItem('token', token)
            axios.defaults.headers.common['Authorization'] = token
            commit('AUTH_SUCCES', token)
            commit('AUTH_SUCCES', user)
            resolve(resp)
          })
          .catch(err => {
            commit('AUTH_ERROR', err)
            localStorage.removeItem('token')
            reject(err)
          })
      })
    },
    logout({ commit }, user) {
      return new Promise((resolve, reject) => {
        axios({
          url: '/api/auth/logout',
          data: user,
          method: 'POST'
        })
          .then(resp => {
            commit('LOGOUT')
            const token = resp.data.username
            localStorage.removeItem('token', token)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    delete_user({ commit, state, dispatch }, user) {
      return new Promise((resolve, reject) => {
        if (confirm("Are you sure you want to delete the account!"))
          axios({
            url: '/api/users/' + state.token.id,
            data: user,
            method: 'DELETE'
          })
            .then(resp => {
              commit('DELETE_USER')
              commit('LOGOUT')
              dispatch('logout')
              resolve(resp)
            })
            .catch(err => {
              reject(err)
            })
      })
    }
  },
  getters: {
    authUser: state => state.token,
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    allUsers: state => state.users,
  },
  plugins: [createPersistedState()]
})

