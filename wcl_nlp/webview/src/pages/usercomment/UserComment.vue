# -*- encoding: utf-8 -*-
"""
@File    :   UserComment.vue.vue
@Contact :   wcl614074127@icloud.com
@License :   (C)Copyright 2022

@Author    @Version    @Desciption
-------    --------    -----------
jackie_chen      1.0         None
"""
<template>
  <div>
    <common-header></common-header>
    <comment-header></comment-header>
    <scroll-top></scroll-top>
    <bg-color></bg-color>
    <common-footer></common-footer>
  </div>
</template>

<script>
import CommonHeader from 'common/Header'
import ScrollTop from 'common/ScrollToTop'
import CommonFooter from 'common/Footer'
import BgColor from 'common/BgSet'
import CommentHeader from './components/CommentHeader'
export default {
  name: 'UserComment',
  components: {
    CommonHeader,
    CommentHeader,
    ScrollTop,
    CommonFooter,
    BgColor
  }
}
</script>

<style lang="scss" scoped>

</style>
