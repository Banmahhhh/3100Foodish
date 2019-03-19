import Vue from 'vue'
import Vuex from 'vuex'

const state = {
  state: initState(),
  mutations: {
    users(state, users) {
      state.users = users;
      window.localStorage.setItem('users', JSON.stringify(state.users))
    },
    clearUser(state) {
      initState(state)
    }
  }
};
function initState(state) {
  state && localStorage.clear()
  state = state || {};
  state.users = attrData();
  state.isLogin = false;
  return state;
}
function attrData() {
  try {
    let users = window.localStorage.getItem('users')
    users = JSON.parse(users) || {}
    return users
  } catch (error) {
    return {}
  }
}
Vue.use(Vuex)
const store = new Vuex.Store(state);
export default store;