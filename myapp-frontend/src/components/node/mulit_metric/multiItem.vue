<template>
  <div >
      <section class="container">
          <section class="itemLeft">
              <el-radio-group v-model="cluRadio" @change="radioChange" :disabled="disabled">
                  <el-radio :label="a">{{a}}</el-radio>
                  <el-radio :label="b">{{b}}</el-radio>
              </el-radio-group>
              <br/>
              <el-select v-model="nodeSelect" class="mySelect1" placeholder="Select" 
              size="large" @change="selectChange" v-if="isSelectAlive" :disabled="disabled">
                  <el-option
                  v-for="item in selectArr"
                  :key="item"
                  :label="item"
                  :value="item"
                  />
              </el-select>
              <br />
                <el-switch
                  :loading="disabled"
                  v-model="realTime"
                  class="demo"
                  active-text="打开实时刷新"
                  inactive-text="关闭实时刷新"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                  size="large"
                  @change="reloadCharts"
                />
          </section>
          <section class="itemCenter">
              <itemPage v-if="isAlive"><nodeMulti :cluster="cluster" 
                  :feature="this.$route.name" :node_name="node_name" :type="type" 
                  :step="step"  :realTime="realTime" :setDisabled="setDisabled"/></itemPage>
          </section>
      </section>
  </div>
</template>
<script>
import itemPage from '@/components/charts/itemPage.vue';

import nodeMulti from '@/components/charts/nodeMulti.vue';

import { ref,nextTick } from 'vue'
import { cluNode } from '@/main';

export default {
  components:{
      itemPage,nodeMulti
  },
  setup() {
      const node_arr=cluNode.data

      const cluRadio = ref('cc-cc408-hya')
      const nodeSelect = ref('data-node-01')

      const selectArr=ref(node_arr[cluRadio.value])

      const isAlive = ref(true)
      const isSelectAlive=ref(true)

      const realTime=ref(true)
      const disabled= ref(true)

      const reloadCharts = () => {
          isAlive.value = false;
          nextTick(() => {
              isAlive.value = true;
          });
          };
      const reloadSelect=()=>{
          isSelectAlive.value = false;
          selectArr.value=node_arr[cluRadio.value]
          nodeSelect.value='data-node-01' //恢复默认值
          nextTick(() => {
              isSelectAlive.value = true;
          });
      }

      function radioChange(){
          console.log(nodeSelect.value)

          reloadSelect()
          reloadCharts()
      }
      function selectChange(){
          reloadCharts()
      }
      const setDisabled=ref(function(state){
      disabled.value=state
      })
      return{
          cluster:cluRadio,
          feature:"elasticsearch_filesystem_data_available_bytes",
          node_name:nodeSelect,

          cluRadio,
          nodeSelect,

          isAlive,
          isSelectAlive,

          radioChange,
          selectChange,
          reloadCharts,

          a:"cc-cc408-hya",
          b:"cc-cc553-interestPrice",
          selectArr,

          realTime,

          disabled,
          setDisabled
      }
  }
}
</script>
<style lang="less">
  header{
      height: 1rem;
      width: 100%;
      background-color: rgba(0,0,255,.2);
      h1{
          font-size: .575rem;
          color: #fff;
          text-align: center;
          line-height: 1rem;
      }
  }
  //主体容器
  .container{
      // min-width: 1200px;
      // max-width: 2048px;
      margin: 0 auto;
      padding:.125rem .125rem 0;
      display: flex;

      // flex布局，容器比例
      .itemLeft{
          flex: 1;
          height: 15rem;
          background-color:rgba(29, 29, 28, 0.408);
          margin-top: 2rem;
          .el-radio-group,.el-select{
              margin: 20px;
          }
      }
      .itemCenter{
          flex: 10;
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
  font-size: medium;
  font-weight: bold;
}
.demo.el-switch .el-switch__core,
.el-switch .el-switch__label {
  width: 140px !important;
  height: 27px;
}

.el-select-dropdown .el-select-dropdown__item.hover { // 下拉hover上去的背景色
  background-color: #828282 !important;
  color: aquamarine;
}
.el-select-dropdown .el-select-dropdown__item{
    color: rgb(200, 200, 198);
    font-size: medium;
}
.el-select-dropdown { //下拉的背景色
  background: #022f6a !important;
  border: 1px solid #83929d !important;
  color: chartreuse;
}
 
.mySelect1 .el-input__inner {
  font-size: 18px !important;
  text-align: center;
//   background: rgb(0, 92, 219) !important;
//   border: transparent !important;
//   border-radius: 12px !important;
  color: #504c4c;
  font-weight: bold;
  cursor: pointer;
  height: 100% !important;
  line-height: 100% !important;
}
 
.mySelect1 {
  width: 200px;
//   height: 50%; //同父级一样高
//   background: url("../../public/static/img/web/year_target_bg.png")
    // no-repeat;
}
 
.mySelect1Popper {
  border: 1px solid #3062ff;
  background-color: #00122a;
}
.mySelect1Popper .el-select-dropdown__item.hover {
  background-color: #14265d;
}
.mySelect1Popper .el-select-dropdown__item.hover {
  color: #ffffff;
}
.mySelect1Popper .el-input__inner {
    color: #ff00dd;
  height: 40px;
  line-height: 40px;
}
.mySelect1Popper .el-select-dropdown__item {
  color: #97bffc;
  font-size: 24px !important;
  height: 50px;
  line-height: 50px;
}
.el-select-dropdown {
  background: #2a4e6e !important;
  border: 2px solid #0345eb !important;
}
.mySelect1Popper .popper__arrow::after {
  border-bottom-color: #97bffc !important;
}
.mySelect1Popper .popper__arrow {
  border-bottom-color: #3062ff !important;
}
 
.el-select
  .el-input
  .el-select__caret.el-input__icon::before {
  content: "\e790" !important;
  color: #f402e0;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
 
.el-select .el-input .el-select__caret {
  transform: rotateZ(0deg) !important;
  color: chartreuse;
}

</style>