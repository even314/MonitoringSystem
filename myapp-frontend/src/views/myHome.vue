<template>
  <div id="img_show">
    <el-carousel :interval="2000" type="card" height="350px"  indicator-position="outside">
      <el-carousel-item v-for="item in imgs" :key="item.id">
        <div class="image">
           <img :src="item.img" class="inImg"/>
        </div>
      </el-carousel-item>
    </el-carousel>
  </div>

 
<a >
<section>
  <div class="all">
    <div class="leftItem"></div>
    <div class="background-img">
      <div class="box">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        
        <div class="content">
          <h2>大数据集群监控系统开发及异常定位算法</h2>
          <p>
              功能：<br/>            
              1.监控数据展示：可以对n套集群的健康状态、集群内各节点、节点所在的服务器（cpu、内存、网络）等监控信息进行展示，具备实时刷新开关功能；<br/>         
              2.对指定的某个异常监控指标曲线，通过波动相似性对比分析，从海量监控指标中筛选出所有具有相似波动规律的监控指标曲线；<br/>          
              3.告警界面：根据所选特征，确定最大值和最小值，返回超出此范围的异常信息；<br/>            
            4.根据日期查询历史异常信息。<br/>
          </p>
        </div>
        
      </div>
    </div>
    <div class="rightItem"></div>
  </div>
</section>
  </a>
</template>

<script>
export default {
  name: 'img_show',
  data () {
    return {
      imgs: [
        {
          id: 1, img: require('@/assets/bj1.jpg')
        },
        {
          id: 2, img: require('@/assets/bj2.jpg')
        },
        {
          id: 3, img: require('@/assets/bj3.jpg')
        },
        {
          id: 3, img: require('@/assets/bj5.jpg')
        },
        {
          id: 3, img: require('@/assets/bj6.jpg')
        },
        {
          id: 3, img: require('@/assets/bj7.jpg')
        },
        {
          id: 3, img: require('@/assets/bj8.png')
        },
      ]
    }
  }
}
</script>

<style scoped>
/* img_show{
  background-color: dimgrey;
  padding-top: 50px;
  width: auto;
} */
.image{
  /* align-content: center; */
  width:100%;
  height:100%;
  position: absolute; 
  background-size:cover;
  
}
h2{
  font-size: large;
  font-weight: bold;
  font-family: 'Courier New', Courier, monospace;
}
.text {
  /* border: 10px solid;
  border-image: linear-gradient(to right, purple, pink) 1; */
  box-shadow: 5px 8px white;
}

*{
  margin:0;
  padding:0;
}

.container{  padding-top: 20px;
  padding-bottom: 20px;}
body{
  background-color: #111845;
}

.background-img{
  background-image: url("https://3.bp.blogspot.com/-piZWCW2uUbg/W2fPXxkWZgI/AAAAAAAAOu0/eydmMjTIqcwLMHEEr2H7imqoRTxMw4o9QCLcBGAs/s1600/among_trees_night_dribbble.png");
height: 250px;
  width: 1500px;
  background-repeat: no-repeat;
  background-size: cover;
  margin-left: 20 auto;
  padding-left:30px;
  border: 1px solid #2a3cad;
  border-radius: 4px;
  box-shadow: 0px 0px 5px #2a3cad;
  position: relative;
}

.content h2{ font-size:19px;}

.box{
  position: absolute;
  margin-top: 120px;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 1500px;
  height: 220px;
  background: #111845a6;
  box-sizing: border-box;
  overflow: hidden;
  box-shadow: 0 20px 50px rgb(23, 32, 90);
  border: 2px solid #2a3cad;
  color: white;
  padding: 20px;
}
.all{
  display: flex;
  .leftItem,
  .rightItem{
    flex:3;
  }
}
.box:before{
  content: '';
  position:absolute;
  top:0;
  left:-100%;
  width:100%;
  height:100%;
  background: rgba(255,255,255,0.1);
  transition:0.5s;
  pointer-events: none;
}

.box:hover:before{
  left:-50%;
  transform: skewX(-5deg);
}


.box .content{
  position:absolute;
  top:15px;
  left:15px;
  right:15px;
  bottom:15px;
  border:1px solid #f0a591;
  padding:20px;
  text-align:center;
  box-shadow: 0 5px 10px rgba(9,0,0,0.5);
  
}
.content{
  text-align: left;
}
.box span{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: block;
  box-sizing: border-box;
  
}

.box span:nth-child(1)
{
  transform:rotate(0deg);
}

.box span:nth-child(2)
{
  transform:rotate(90deg);
}

.box span:nth-child(3)
{
  transform:rotate(180deg);
}

.box span:nth-child(4)
{
  transform:rotate(270deg);
}

.box span:before
{
  content: '';
  position: absolute;
  width:50%;
  height: 2px;
  background: #50dfdb;
  animation: animate 4s linear infinite;
}

@keyframes animate {
  0% {
  transform:scaleX(0);
  transform-origin: left;
  }
  50%
  {
    transform:scaleX(1);
  transform-origin: left;
  }
  50.1%
  {
    transform:scaleX(1);
  transform-origin: right;
    
  }
  
  100%
  {
    transform:scaleX(0);
  transform-origin: right;
    
  }
 
} .inImg{
    width:600px;
    height: 350px;
  }
  
</style>
