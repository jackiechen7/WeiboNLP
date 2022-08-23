// 全局变量文件
import Vue from 'vue'
import Vuex from 'vuex'
import user from './userInfo'
import usertweets from './userTweets'
import group from './group'
import total from './tweetsTotal'
import sentiments from './sentiments'
import mutations from './mutations'
import usercomment from './userComment'
import tempid from './tempId'
import tempids from './tempids'

Vue.use(Vuex)

export default new Vuex.Store({
  user,
  usertweets,
  tempid,
  tempids,
  group,
  usercomment,
  total,
  sentiments,
  mutations
})
