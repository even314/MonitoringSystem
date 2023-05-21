<template lang="">
  <el-switch
    :loading="disabled"
    class="demo"
    v-model="realTime"
    active-text="打开实时刷新"
    inactive-text="关闭实时刷新"
    active-color="#13ce66"
    inactive-color="#ff4949"
    size="large"
    @change="reload"
  />
  <br />
  <div>
    <itemPage v-if="isAlive"><clusterView :cluster="cluster" 
        :feature="feature" :node_name="node_name" :type="type" 
        :step="step" :realTime="realTime" :setDisabled="setDisabled"/></itemPage>
  </div>
</template>
<script>
import clusterView from '../charts/clusterView.vue';
import itemPage from '../charts/itemPage.vue';
import { ref, nextTick } from 'vue'

const realTime = ref(true)
const isAlive = ref(true)
const disabled= ref(true)
//刷新子组件
function reload() {
  isAlive.value = false;
  nextTick(() => {
    isAlive.value = true;
    // console.log(realTime.value)
  })
}
 const setDisabled=ref(function(state){
  disabled.value=state
})
export default {
  components: {
    clusterView, itemPage
  },
  data() {
    let step = ''
    let type = 'value'
    if (this.$route.name == 'elasticsearch_cluster_health_status') {
      step = 'start'
      type = 'category'
    }
    return {
      feature: this.$route.name,
      step: step,
      type: type,
      realTime,
      reload,
      isAlive,
      disabled,
      setDisabled
    }
  }

}
</script>
<style>
.demo .el-switch__label {
  width: 10px;
  position: absolute;
  display: none;
  color: #ff00dd;
}
/*打开时文字位置设置*/
.demo .el-switch__label--right {
  color: #fff;
  z-index: 1;
  right: -3px;
}
/*关闭时文字位置设置*/
.demo .el-switch__label--left {
  color: #fff;
  z-index: 2;
  left: 19px;
}
/*显示文字*/
.demo .el-switch__label.is-active {
  display: block;
  text-align: center;
  color: #00ffdd;
  font-size: large;
  font-weight: bold;
}
.demo.el-switch .el-switch__core,
.el-switch .el-switch__label {
  width: 140px !important;
  height: 27px;
}
</style>