# -*- encoding: utf-8 -*-
"""
@File    :   TextAnalysis.vue.vue
@Contact :   wcl614074127@icloud.com
@License :   (C)Copyright 2022

@Author    @Version    @Desciption
-------    --------    -----------
jackie_chen      1.0         None
"""
<template>
  <div>
    <common-header></common-header>
    <start-analysis></start-analysis>
    <common-footer></common-footer>
    <bg-color></bg-color>
  </div>
</template>

<script>
import CommonHeader from 'common/Header'
import CommonFooter from 'common/Footer'
import BgColor from 'common/BgSet'
import StartAnalysis from './components/StartAnalysis'

export default {
  name: 'TextAnalysis',
  components: {
    CommonHeader,
    StartAnalysis,
    CommonFooter,
    BgColor
  },
  data () {
    return {
      textarea: ''
    }
  }
}

</script>

<style lang="scss" scoped>
</style>
