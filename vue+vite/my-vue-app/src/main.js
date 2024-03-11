import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
//import ElementPlus from 'element-plus'
//import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './assets/less/index.less'
import store from './store/index.js';
import  './api/mockData/mock.js';



const app =createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(router).use(store)
app.mount('#app')
//app.use(ElementPlus)






// The Vue build version to load with the `import` command

// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

