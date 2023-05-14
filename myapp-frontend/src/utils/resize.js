import {nextTick, ref} from "vue";
import {debounce} from 'throttle-debounce';

/*chart 是echarts图的实例*/
export const chart = ref();
export const chart_=ref()
/*检测侧边栏是否缩放*/
let sidebarElm;
/*使用element-resize-detector 来监听侧边栏是否产生变化*/
const elementResizeDetectorMaker = require("element-resize-detector");
const erd = elementResizeDetectorMaker();

/*使用防抖debounce函数，减少resize的次数*/
const chartResizeHandler = debounce(100, function() {
    if (chart.value) {
        chart.value.resize()
    }if(chart_.value){
        chart_.value.resize()
    }
} ,false)
/*在侧边栏宽度变化后，执行该函数*/
const sidebarResizeHandler = () => {
    nextTick(() => {
        chartResizeHandler()
    })
}
/*添加窗口大小变化监听*/
const initResizeEvent = () => {
    window.addEventListener('resize', chartResizeHandler)
}
/*移除窗口大小变化监听*/
const destroyResizeEvent = () => {
    window.removeEventListener('resize', chartResizeHandler)
}
/*初始化 sider监听*/
const initSidebarResizeEvent = () => {
    /*获取侧边栏的document*/
    sidebarElm = document.getElementsByClassName('sider-content')[0];
    if (sidebarElm) {
        erd.listenTo(sidebarElm, sidebarResizeHandler)
    }

}
/*移除 sider监听*/
const destroySidebarResizeEvent = () => {
    if (sidebarElm) {
        erd.removeListener(sidebarElm)
    }
}

export const mounted = () => {
    initResizeEvent();
    initSidebarResizeEvent();
}
export const beforeDestroy = () => {
    destroyResizeEvent();
    destroySidebarResizeEvent();
}
