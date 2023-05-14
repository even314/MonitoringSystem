<template>
  <el-row type="flex">
    <el-col>
      <!--      <h5 class="mb-2">Default colors</h5>-->
      <el-menu mode="horizontal" background-color="gray">
        <el-sub-menu class="menu-item" index="1">
          <template #title>
            <el-icon>
              <img src="@/assets/node.png" class="image" />
              <location />
            </el-icon>
            <span>集群层面</span>
          </template>
          <el-menu-item class="item"
            @click="goTo('/cluster/elasticsearch_cluster_health_active_shards')">active_shards</el-menu-item>
          <el-menu-item class="item"
            @click="goTo('/cluster/elasticsearch_cluster_health_number_of_nodes')">number_of_nodes</el-menu-item>
          <el-menu-item class="item" @click="goTo('/cluster/elasticsearch_cluster_health_status')">status</el-menu-item>
        </el-sub-menu>

        <el-sub-menu class="menu-item" index="2">
          <template #title>
            <el-icon>
              <img src="@/assets/cluster.png" class="image" />
              <location />
            </el-icon>
            节点层面
          </template>
          <el-sub-menu index="3" class="sub">
            <template #title>
              <el-icon>
                <location />
              </el-icon>
              <span class="mertic">单指标</span>
            </template>
            <el-menu-item class="item" @click="goTo('/node/sig/elasticsearch_indices_indexing_index_time_seconds_total')">
              indices_indexing_index_time_seconds_total
            </el-menu-item>
            <el-menu-item class="item" @click="goTo('/node/sig/elasticsearch_indices_search_query_time_seconds')">
              indices_search_query_time_seconds
            </el-menu-item>
            <el-menu-item class="item" @click="goTo('/node/sig/elasticsearch_os_load5')">os_load5</el-menu-item>
            <el-menu-item class="item" @click="goTo('/node/sig/elasticsearch_process_cpu_percent')">process_cpu_percent
            </el-menu-item>
            <el-menu-item class="item" @click="goTo('/node/sig/elasticsearch_transport_rx_size_bytes_total')">
              transport_rx_size_bytes_total
            </el-menu-item>
            <el-menu-item class="item"
              @click="goTo('/node/sig/elasticsearch_transport_tx_size_bytes_total')">transport_tx_size_bytes_total
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="4" class="sub">
            <template #title>
              <el-icon>
                <location />
              </el-icon>
              <span class="mertic">多指标</span>
            </template>
            <el-menu-item class="item" @click="goTo('/node/mul/elasticsearch_filesystem_data_available_bytes')">
              filesystem_data_available_bytes
            </el-menu-item>
          </el-sub-menu>
        </el-sub-menu>

        <el-menu-item class="menu-item" @click="goTo('/compare')">
          <img src="@/assets/sim.png" class="image" />
          <location />
          <span>相似波动曲线</span>
        </el-menu-item>

        <el-menu-item class="menu-item" @click="goTo('/warning')">
          <location />
          <img src="@/assets/notice.png" class="image" />
          <location />
          <span>异常警告</span>
        </el-menu-item>

        <el-menu-item class="menu-item" @click="goTo('/history')">
          <location />
          <img src="@/assets/history.png" class="image" />
          <location />
          <span>历史记录</span>
        </el-menu-item>

        <span class="accupy1">
        </span>
        <h2 class="title">
          大数据集群监控和异常定位算法
        </h2>
        <span class="accupy2">
        </span>

        <el-menu-item class="menu-item" @click="goTo('/')">
          <img src="@/assets/home.png" class="image" />
          <location />
          <span>返回主页</span>
        </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script>

export default {
  data() {
    return {};
  },

  methods: {
    // handleOpen(key, keyPath) {
    //   console.log(key, keyPath);
    // },
    // handleClose(key, keyPath) {
    //   console.log(key, keyPath);
    // },
    goTo(path) {
      this.$router.replace(path)
    }
  }
};
</script>

<style>
.bar {
  background-color: gray;
}

.whole-menu {
  display: flex;
  /*align-items: center;*/
  /*justify-content: center;*/
  background-color: black;
  font-size: larger;
  font-weight: bold;
}

.item {
  font-size: large;
  font-weight: bold;
  font-family: initial;
  color: white;
}

.menu-item {
  position: relative;
  display: flex;
  transition: 0.4s;
  font-size: larger;
  font-weight: bold;
  /* background-color: darkgray; */
}

.menu-item:hover {
  /*background-color: white;*/
  /*color: white;*/
  border-bottom: solid 6px;
  border-bottom-color: brown;
  /*height: 80px;*/
}

.mertic {
  font-size: medium;
  font-weight: bold;
}

.sub:hover {
  border-bottom: solid 5px;
  border-bottom-color: brown;
}

.image {
  width: 25px;
  height: 25px;
}

.right-btn {
  float: right;
  margin-right: 10px;
  height: 100%;
  /* line-height: 50px;    */
}

.title {
  font-weight: bold;
  font-size: 30px;
  margin-top: 12px;
  color: black;
  /* text-align: center; */
}

.accupy1 {
  width: 70px;
}

.accupy2 {
  width: 150px;
  margin-right: 0px;
}</style>