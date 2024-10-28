import { createStore } from 'vuex'
import VuexPersistence from 'vuex-persist'
import axios from 'axios'

const vuexLocal = new VuexPersistence({
    storage: window.localStorage
})


const store = createStore({
    state() {
        return {
            status: '',
            token: localStorage.getItem('token') || '',
            user: [],
        }
    },
    mutations: {
        AUTH_REQUEST(state) {
            state.status = 'loading'
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
            state.user = ''
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
                        const token = resp.data.auth_token
                        console.log(resp.data)
                        const user = resp.data
                        localStorage.setItem('token', token)
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
                        const token = resp.data.auth_token
                        const user = resp.data
                        localStorage.setItem('token', token)
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
                        const token = resp.data.auth_token
                        localStorage.removeItem('token', token)
                        resolve(resp)
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },
        delete_user({ commit, state, token, dispatch }) {
            const auth_token = localStorage.getItem('token', token)
            return new Promise((resolve, reject) => {
                if (confirm("Are you sure you want to delete the account!"))
                    axios({
                        url: '/api/users/' + state.token.id,
                        data: token,
                        headers: { Authorization: 'Token ' + auth_token },
                        method: 'DELETE'
                    }
                    )
                        .then(resp => {
                            commit('DELETE_USER')
                            commit('LOGOUT')
                            const token = resp.data.token
                            localStorage.removeItem('token', token)
                            dispatch('logout')
                            resolve(resp)
                        })
                        .catch(err => {
                            console.log(auth_token);
                            reject(err)
                        })
            })
        }
    },
    getters: {
        authUser: state => state.token,
        isLoggedIn: state => !!state.token,
        authStatus: state => state.status,
    },
    plugins: [vuexLocal.plugin]
})

export default store

