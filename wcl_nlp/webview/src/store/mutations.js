// 更改store中state状态的唯一方法就是提交mutation

export default {
  changeUserTweets (state, usertweets) {
    state.usertweets = usertweets
  },
  changeSentiments (state, sentiments) {
    state.sentiments = sentiments
  },
  changeUserComment (state, usercomment) {
    state.usercomment = usercomment
  }
}
