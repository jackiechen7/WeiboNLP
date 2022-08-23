# -*- encoding: utf-8 -*-
"""
@File    :   Footer1.vue
@Contact :   wcl614074127@icloud.com
@License :   (C)Copyright 2022

@Author    @Version    @Description
-------    --------    -----------
jackie_chen      1.0   页面底部固定样式
"""
<template>
  <div class='footer'>
    <p>Copyright © 2022 Made by wcl.</p>
    <p>本科毕业设计 常工院</p>
  </div>
</template>

<script>
export default {
  name: 'CommonFooter'
}

</script>

<style lang="scss" scoped>
  .footer {
    position: fixed;
    bottom: 30px;
    width: 100%;
    text-align: center;
  }

</style>
