# -*- encoding: utf-8 -*-
"""
@File    :   Header.vue
@Contact :   wcl614074127@icloud.com
@License :   (C)Copyright 2022

@Author    @Version    @Description
-------    --------    -----------
jackie_chen      1.0   页面头部样式
"""
<template>
  <div>
    <router-link to="/">
      <p>个人微博分析首页</p>
    </router-link>
    <router-link to="/comment">
      <p>单条微博分析首页</p>
    </router-link>
    <router-link to="/crawler">
      <p>微博持续爬虫</p>
    </router-link>
    <router-link to="/analysis">
      <p>自定义文本分析</p>
    </router-link>
    <router-link to="/mycrawler">
      <p>已爬虫用户和微博</p>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'CommonHeader'
}

</script>

<style lang="scss" scoped>
  div {
    text-align: center;
  }

  p {
    display: inline-block;
    color: #fff;
    font-size: .3rem;
    padding: .26rem .24rem;
    -webkit-font-smoothing: antialiased;
    text-align: center;
  }

  p:hover {
    color: #4fb6ff;
  }

</style>
