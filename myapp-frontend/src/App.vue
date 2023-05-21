<template>  
<div>
      <div class="login">
        <!-- <Particles id="tsparticles" class="login__particles" :options="particles" /> -->
          <!--引入自定义左侧菜单栏-->
          </div>
          <AsideNav/>
        <!-- <h2>大数据集群监控和异常定位算法</h2> -->
        <div >
          <!--引入跳转路由-->
          <router-view :key="key"/>
        </div>
      </div>
      
</template>

<script >

import AsideNav from '@/components/navBar/asideNav.vue'
import { provide } from 'vue';
import * as echarts from "echarts"
import axios from "axios"



export default {
    setup(){
    // provide("名字自己取","传递的内容")
    provide("echarts",echarts)
    provide("axios",axios)
    return {
      
    }
  },
  name: 'App',
  components: {
    AsideNav,
  },
  computed: {
    key() {
      // 只要保证 key 唯一性就可以了，保证不同页面的 key 不相同
      // console.log(this.$route.fullPath);
      return this.$route.fullPath
    }
  },
}
</script>

<style >
h2{
  color: white;
  font-variant-position: center;
  font-family: Georgia, 'Times New Roman', Times, serif;
  font-weight: bolder;
  margin: 5px;
}
#app {
  /*font-family: Avenir, Helvetica, Arial, sans-serif;*/
  /*-webkit-font-smoothing: antialiased;*/
  /*-moz-osx-font-smoothing: grayscale;*/
  text-align: center;
  /* // color: #2c3e50;
  // margin: 0px;
  // padding: 0px;
  // border: 0; */
  background-image: url("@/assets/bj4.jpg");
  /* background-color: gray; */
  height: 100%;
  width: 100%;
  position: absolute;
}

</style>
