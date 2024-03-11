// 路由文件
import { createRouter, createWebHistory } from "vue-router";
//import Home from '../views/home/Home.vue'
const routes = [

    {
        path: '/',
        component: () => import('../views/Main.vue'),
        redirect:'/home',
        children:[
            {
                path:'/home',
                name:'home',
                component: () => import('../views/home/Home.vue')
            },
            {
                path:'/user',
                name:'user',
                component: () => import('../views/User/User.vue')
            },
            {
                path:'page1',
                name:'page1',
                component: () => import('../views/Page/Page1.vue')
            },
            {
                path:'page2',
                name:'page2',
                component: () => import('../views/Page/Page2.vue')
            },
        ]
    },
    {
        path: '/login',
        component: () => import('../components/LoginView.vue')

    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})
export default router;





