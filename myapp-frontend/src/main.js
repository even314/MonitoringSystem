import { createApp } from 'vue'
// import Particles from 'particles.vue3'
import App from './App.vue'
import router from "@/routers";
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from "@element-plus/icons-vue"
import DataService from './services/DataService';
import { reactive } from 'vue'
import { delData } from './utils/storageTools';
import  Particles  from   'vue-particles'


export let cluNode=reactive({})
let refresh=reactive({})

async function init(){
cluNode=await DataService.getData('node_names')
refresh=await DataService.getData('refresh')
if(refresh.data.type){
  delData()
}
const app = createApp(App)
// app.use(VueParticles)
app.use(ElementPlus)
app.use(Particles)
app.use(router)
app.mount('#app')
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }

}
init()