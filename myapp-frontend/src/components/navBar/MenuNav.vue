<!--<template>-->
<!--  <fragment>-->
<!--    <template v-for="(itemss,indexss) in menuData">-->
<!--      &lt;!&ndash; 一级菜单 &ndash;&gt;-->
<!--      <el-submenu :index="indexss+''" :key="indexss" v-if="itemss.showMenu && itemss.children">-->
<!--        &lt;!&ndash; 一级菜单标题 &ndash;&gt;-->
<!--        <template>-->
<!--          <slot>-->
<!--            <i :class="itemss.meta.icon"></i>-->
<!--            <slot>-->
<!--              <span>{{ itemss.name }}</span>-->
<!--            </slot>-->
<!--          </slot>-->
<!--        </template>-->
<!--        <template v-for="(term,indext) in itemss.children">-->
<!--          &lt;!&ndash; 二级菜单没有子路由的时候 &ndash;&gt;-->
<!--          <el-menu-item-->
<!--              :key="term.path"-->
<!--              :index="term.path+''"-->
<!--              v-if="term.showMenu && !term.children"-->
<!--              :class="$route.path===term.path?'is-active':''">-->
<!--            <i :class="term.meta.icon"></i>-->
<!--            <slot>-->
<!--              <span>{{ term.name }}</span>-->
<!--            </slot>-->
<!--          </el-menu-item>-->
<!--          &lt;!&ndash; 二级菜单有子路由的时候,递归循环自身 &ndash;&gt;-->
<!--          <MenuNav v-else :key="indext" :menuData="[...term]"></MenuNav>-->
<!--        </template>-->
<!--      </el-submenu>-->
<!--      <el-menu-item-->
<!--          :key="indexss"-->
<!--          :index="itemss.path+''"-->
<!--          v-if="itemss.showMenu && !itemss.children"-->
<!--          :class="$route.path===itemss.path?'is-active':''">-->
<!--        <i :class="itemss.meta.icon"></i>-->
<!--        <slot>-->
<!--          <span>{{ itemss.name }}</span>-->
<!--        </slot>-->

<!--      </el-menu-item>-->
<!--    </template>-->
<!--  </fragment>-->
<!--</template>-->

<!--<script>-->
<!--export default {-->
<!--  name: 'MenuNav',-->
<!--  props: ['menuData'],-->
<!--  components: {},-->
<!--  data() {-->
<!--    return {};-->
<!--  },-->
<!--  computed: {},-->
<!--  watch: {},-->
<!--  created() {-->
<!--  },-->
<!--  mounted() {-->
<!--    // console.log(this.menuData);-->
<!--  },-->
<!--  // destroyed() {},-->
<!--  methods: {},-->
<!--};-->
<!--</script>-->