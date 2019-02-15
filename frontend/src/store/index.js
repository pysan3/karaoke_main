import Vue from 'vue'
import Vuex from 'vuex'
import * as types from './mutation-types'

Vue.use(Vuex)

const state = {
  user_id: -1,
  msg: 'hello'
}

const mutations = {
  [types.UPDATE_MESSAGE] (state, newMsg) {
    state.msg = newMsg
  },
  [types.UPDATE_USER_ID] (state, num) {
    state.user_id = num - 0
  }
}

const actions = {
  repeat (context) {
    let msg = context.state.msg
    context.commit(types.UPDATE_MESSAGE, `${msg} ${msg}`)
  }
}

export default new Vuex.Store({
  state,
  mutations,
  actions
})
