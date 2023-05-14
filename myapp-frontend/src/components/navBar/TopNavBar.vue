<template>
  <!-- 头部二级菜单栏的组件封装 -->
  <div class="sidebar">
    <div
        mode="horizontal"
      class="sidebar-el-menu"
      :default-active="toIndex"
      background-color="#fff"
      text-color="#000000"
      router>
      <div v-for="(item, index) in itemList" :key="index" :index="item.path">
        <!-- 需要图标的在 item 对象中加上属性 icon -->
        <!-- <i :class="item.icon"></i> -->
        <span>
          <slot></slot>
          {{ item.title }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    itemList: {
      type: Array,
      default: () => []
    }
  },
  data(){
    return {

    }
  },
  methods:{

  },
}
</script>

<style scoped>
/* 左侧菜单栏定位和位置大小设定 */
.sidebar {
  display: block;
  position: absolute;
  left: 0;
  top: 70px;
  bottom: 0;
  overflow-y: scroll;
}
.sidebar::-webkit-scrollbar {
  width: 0;
}
.sidebar-el-menu {
  width: 250px;
}
.sidebar > ul {
  height: 100%;
}

</style>
