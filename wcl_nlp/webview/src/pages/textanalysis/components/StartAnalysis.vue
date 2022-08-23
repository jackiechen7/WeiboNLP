# -*- encoding: utf-8 -*-
"""
@File    :   StartAnalysis.vue.vue
@Contact :   wcl614074127@icloud.com
@License :   (C)Copyright 2022

@Author    @Version    @Desciption
-------    --------    -----------
jackie_chen      1.0     文本情感分析
"""
<template>
  <div class="outer">
    <div class="middle">
      <div class="logo">
        <svg class="svg" width="40px" height="40px" viewBox="0 0 64 64" version="1.1">
          <title>Icon</title>
          <defs>
            <linearGradient x1="50%" y1="0%" x2="50%" y2="100%" id="linearGradient-1">
              <stop stop-color="#FFFFFF" offset="0%"></stop>
              <stop stop-color="#F2F2F2" offset="100%"></stop>
            </linearGradient>
            <circle id="path-2" cx="31.9988602" cy="31.9988602" r="2.92886048"></circle>
            <filter x="-85.4%" y="-68.3%" width="270.7%" height="270.7%" filterUnits="objectBoundingBox" id="filter-3">
              <feOffset dx="0" dy="1" in="SourceAlpha" result="shadowOffsetOuter1"></feOffset>
              <feGaussianBlur stdDeviation="1.5" in="shadowOffsetOuter1" result="shadowBlurOuter1"></feGaussianBlur>
              <feColorMatrix values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0  0 0 0 0.159703351 0" type="matrix"
                in="shadowBlurOuter1"></feColorMatrix>
            </filter>
          </defs>
          <g id="slogo" class="rotation" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
            <g>
              <g id="Icon">
                <circle id="Oval-1" fill="url(#linearGradient-1)" cx="32" cy="32" r="32"></circle>
                <path
                  d="M36.7078009,31.8054514 L36.7078009,51.7110548 C36.7078009,54.2844537 34.6258634,56.3695395 32.0579205,56.3695395 C29.4899777,56.3695395 27.4099998,54.0704461 27.4099998,51.7941246 L27.4099998,31.8061972 C27.4099998,29.528395 29.4909575,27.218453 32.0589004,27.230043 C34.6268432,27.241633 36.7078009,29.528395 36.7078009,31.8054514 Z"
                  id="blue" fill="#2359F1" fill-rule="nonzero"></path>
                <path
                  d="M45.2586091,17.1026914 C45.2586091,17.1026914 45.5657231,34.0524383 45.2345291,37.01141 C44.9033351,39.9703817 43.1767091,41.6667796 40.6088126,41.6667796 C38.040916,41.6667796 35.9609757,39.3676862 35.9609757,37.0913646 L35.9609757,17.1034372 C35.9609757,14.825635 38.0418959,12.515693 40.6097924,12.527283 C43.177689,12.538873 45.2586091,14.825635 45.2586091,17.1026914 Z"
                  id="green" fill="#57CF27" fill-rule="nonzero"
                  transform="translate(40.674608, 27.097010) rotate(60.000000) translate(-40.674608, -27.097010) ">
                </path>
                <path
                  d="M28.0410158,17.0465598 L28.0410158,36.9521632 C28.0410158,39.525562 25.9591158,41.6106479 23.3912193,41.6106479 C20.8233227,41.6106479 18.7433824,39.3115545 18.7433824,37.035233 L18.7433824,17.0473055 C18.7433824,14.7695034 20.8243026,12.4595614 23.3921991,12.4711513 C25.9600956,12.4827413 28.0410158,14.7695034 28.0410158,17.0465598 Z"
                  id="red" fill="#FF561B" fill-rule="nonzero"
                  transform="translate(23.392199, 27.040878) rotate(-60.000000) translate(-23.392199, -27.040878) ">
                </path>
                <g id="inner-round">
                  <use fill="black" fill-opacity="1" filter="url(#filter-3)" xlink:href="#path-2"></use>
                  <use fill="#F7F7F7" fill-rule="evenodd" xlink:href="#path-2"></use>
                </g>
              </g>
            </g>
          </g>
        </svg>
        <span class="name">情感分析API</span>
      </div>
      <p>输入一段想分析的文字：
        <a @click="changetext">随机一段文字示例？</a>
        <i class="el-icon-circle-close-outline" @click="cleartext"></i>
      </p>

      <el-input class="text" type="textarea" :rows="10" placeholder="请输入内容" v-model="textarea">
      </el-input>
    </div>
    <div class="show">
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="grid-content">
            <ve-funnel :data="chartDataf" :legend-visible="false" height="315px" class="charts-f"></ve-funnel>
          </div>
        </el-col>
        <el-col :span="8">
          <div v-if="this.sentiments" class="grid-content bg-content">
            <el-progress class="progress" v-if="this.sentiments>50" type="circle" :percentage="this.sentiments"
              color="#13ce66" :format="format">
            </el-progress>
            <el-progress class="progress" v-else type="circle" :percentage="this.sentiments" color="#ff4949"
              :format="format1">
            </el-progress>
          </div>
          <div v-else class="grid-content">
            <el-progress class="progress" type="circle" :percentage="0" :format="format2">
            </el-progress>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="grid-content">
            <ve-pie :data="chartData" :settings="chartSettings" :legend-visible="false" height="315px" class="charts">
            </ve-pie>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'StartAnalysis',
  data () {
    this.chartSettings = {
      dimension: '关键词',
      metrics: '数量'
    }
    return {
      textarea: '',
      sentiments: '',
      chartData: {
        columns: ['关键词', '数量'],
        rows: [{
          '关键词': '1',
          '数量': 1538
        },
        {
          '关键词': '2',
          '数量': 3512
        },
        {
          '关键词': '3',
          '数量': 2432
        }]
      },
      chartDataf: {
        columns: ['状态', '数值'],
        rows: [{
          '状态': '',
          '数值': 0.9
        },
        {
          '状态': '',
          '数值': 0.6
        },
        {
          '状态': '',
          '数值': 0.3
        },
        {
          '状态': '',
          '数值': 0.1
        },
        {
          '状态': '',
          '数值': 0.1
        }]
      },
      text: [
        '老百姓真的都还是善良的老百姓。昨天的核酸到现在还没出结果，所有周围的病友都在一边疑惑为啥不出结果，一边又自顾自的帮疾控找理由：应该是我们人太多了，他们很辛苦了已经…… ​​​​',
        '很久没点开超话了……前两天看到一个歌迷朋友剪辑了一个15年前视频，那时的我，呃，确实还不是一个能自洽的我……但幸好会唱歌这一点，让我遇见了这么棒的你们……今天这个日子，想点一首歌，送给一直陪伴我的星星们。这18年里，我们一起成长，彼此鼓励，努力成为更好的人。很开心，也很幸运有你们一路陪伴，我继续唱歌给你们听，《然后我们成了想成为的人》送给你们！',
        '这个人真的好可恶呀！',
        '十五年，拍不同阶段的同框照纪念一下我的青春。我很爱且感谢我的这个职业，能让我成长的每一个足印都有迹可寻。祝福陪伴过的，一路仍在陪伴的你们，都安好，都奋力燃烧！不负自己',
        '任何人不知道用这个手写短信和男朋友聊天我都会伤心的ok？ ​​​​',
        '错过了就不遗憾，只要是好答案。',
        '100多码也叫快一点？？？？？司机超速抢黄灯撞上劳斯莱斯致车损185万，真的很可恶',
        '一代人有一代人的江湖，曾经的江湖也不过是沧海一粟'
      ]

    }
  },
  methods: {
    cleartext () {
      this.textarea = ''
    },
    changetext () {
      this.textarea = this.text[parseInt(Math.random() * 7)]
    },
    // 环形图中的文字
    format (sentiments) {
      return `${this.sentiments}% 积极`
    },
    format1 (sentiments) {
      return `${this.sentiments}% 消极`
    },
    format2 (sentiments) {
      return `0% 消极`
    }
  },
  mounted () {
    this.changetext()
  },
  watch: {
    'textarea': function (newval) {
      if (newval !== '') {
        axios.get('http://localhost:8000/snownlpapi?&snownlp=' + newval)
          .then((response) => {
            console.log(response.data)
            this.sentiments = parseInt(parseFloat(response.data.sentiments) * 100)
            console.log(this.sentiments)
            this.chartData.rows = [{
              '关键词': response.data.keywords[0],
              '数量': Math.random() * 300
            },
            {
              '关键词': response.data.keywords[1],
              '数量': Math.random() * 200
            },
            {
              '关键词': response.data.keywords[2],
              '数量': Math.random() * 100
            }]
            this.chartDataf.rows = [{
              '状态': response.data.tf[0][0],
              '数值': response.data.tf[0][1]
            },
            {
              '状态': response.data.tf[1][0],
              '数值': response.data.tf[1][1]
            },
            {
              '状态': response.data.tf[2][0],
              '数值': response.data.tf[2][1]
            },
            {
              '状态': response.data.tf[3][0],
              '数值': response.data.tf[3][1]
            },
            {
              '状态': response.data.tf[4][0],
              '数值': response.data.tf[4][1]
            }]
          })
      }
    }
  }
}

</script>

<style lang="scss" scoped>
  .logo {
    text-align: center;

    .svg {
      vertical-align: middle;
    }

    @-webkit-keyframes rotation {
      from {
        -webkit-transform: rotate(0deg);
      }

      to {
        -webkit-transform: rotate(360deg);
      }
    }

    .rotation {
      -webkit-transform: rotate(360deg);
      animation: rotation 3s linear infinite;
      -moz-animation: rotation 3s linear infinite;
      -webkit-animation: rotation 3s linear infinite;
      -o-animation: rotation 3s linear infinite;
      transform-origin: center center;
    }

    .name {
      vertical-align: middle;
      font-size: .48rem;
      margin-left: .24rem;
      font-weight: 200;
      color: #fff;
    }
  }

  .middle {
    position: relative;
    top: 30px;
    min-width: 800px;
    max-width: 900px;
    margin: 0 auto;

    .text {
      font-size: 16px;
      font-family: "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    }

    p {
      font-size: 16px;
      color: #fff;
      text-align: left;
      position: relative;

      i {
        float: right;
        color: #fff;
        font-size: 30px;
        cursor: pointer;
      }

      a {
        text-decoration: underline;
        font-size: 14px;
        color: #cccccc;
        cursor: pointer;
      }
    }
  }

  .el-row {
    margin-bottom: 20px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .el-col {
    border-radius: 4px;
  }

  .grid-content {
    border-radius: 4px;
    min-height: 36px;
    position: relative;
  }

  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }

  .show {
    max-width: 1100px;
    margin: 80px auto 20px;
    text-align: center;
    position: relative;

    .progress {
      transform: scale(1.6);
      margin-top: 45px;
    }

    .charts-f {
      margin-top: -67px;
    }

    .charts {
      margin-top: -117px;
    }
  }

</style>
