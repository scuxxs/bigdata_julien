// 路由文件
import { createRouter, createWebHistory } from "vue-router";

//import Home from '../views/home/Home.vue'

const routes = [
    {
        path: '/',
        component: () => import('../views/Main.vue'),
        children:[
            {
                path:'/',
                name:'home',
                component: () => import('../views/home/Home.vue')
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})


//router.beforeEach((to,from)=>{
    // if(to.meta.requireAuth) {
    //     let token = localStorage.getItem('auth-system-token');
    //     let isLogin = localStorage.getItem('auth-system-login');
    //     if(!token||!isLogin){
    //         return {
    //             path: '/login'
    //         }
    //     }
    // }
//})

 export default router;
