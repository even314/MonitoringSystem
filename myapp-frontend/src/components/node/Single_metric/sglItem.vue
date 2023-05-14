<template lang="">
  <div>
    <section class="container">
      <section class="itemLeft">
                <el-radio-group v-model="radio" @change="radioChange">
                    <el-radio :label="c1">{{c1}}</el-radio>
                    <el-radio :label="c2">{{c2}}</el-radio>
                </el-radio-group>
                <br />
                <el-switch
                  class="demo"
                  v-model="realTime"
                  active-text="打开实时刷新"
                  inactive-text="关闭实时刷新"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                  size="large"
                  @change="reload"
                />
      </section>
        <section class="itemRight">
          <itemPage v-if="isAlive"><nodeSgl :cluster="cluster" 
              :feature="this.$route.name" :node_name="node_name" :type="type" 
              :step="step"  :realTime="realTime" /></itemPage>
        </section>
    </section>
  </div>

</template>
<script>
import nodeSgl from '@/components/charts/nodeSgl.vue';
import itemPage from '@/components/charts/itemPage.vue';
import { ref,nextTick } from 'vue'
const radio = ref("cc-cc408-hya")
const isAlive = ref(true)
const realTime=ref(true)
//刷新子组件
const reload = () => {
            isAlive.value = false;
            nextTick(() => {
                isAlive.value = true;
            });
            };
//复选框刷新
function radioChange(){
            reload()
        }
export default {

  components:{
    nodeSgl,itemPage
  },
  data(){
    let step=''
    if(this.$route.name=='elasticsearch_process_cpu_percent'){
      step='start'
    }
    return {
      // feature:this.$route.name,
      step:step,
      cluster:radio,
      radio,
      isAlive,
      c1:"cc-cc408-hya",
      c2:"cc-cc553-interestPrice",
      radioChange,
      realTime,
      reload
    }
  }

}
</script>
<style lang="less">
  .container{
        min-width: 1200px;
        max-width: 2048px;
        margin: 0 auto;
        padding:.125rem .125rem 0;
        display: flex;
        
        // flex布局，容器比例
        .itemLeft{
            flex: 1;
            background-color: rgba(44, 44, 91, 0.8);
        }
        .itemRight{
            flex: 9;
            height: 10.5rem;
            padding: .125rem;
            margin:.25rem
        }
      }

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
  color: #a6f0ff;
  font-size: large;
  font-weight: bold;
}
.demo.el-switch .el-switch__core,
.el-switch .el-switch__label {
  width: 140px !important;
  height: 27px;
}


.el-radio__label{
  color: #fff;
  font-size: large;
  font-weight: bold;
}
// .el-radio__input.is-checked + .el-radio__label {
//   color: #fd7624 !important;
//   font-size: large;
//   font-weight: bold;
// }
// .el-radio__input.is-checked .el-radio__inner {
//   background: #fd7624 !important;
//   border-color: #fd7624 !important;
// }
</style>