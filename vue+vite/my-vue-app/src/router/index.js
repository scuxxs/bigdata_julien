// 路由文件
import { createRouter, createWebHistory } from "vue-router";
//import Home from '../views/home/Home.vue'
const routes = [

    {
        path: '/',
        component: () => import('../views/Main.vue'),
        redirect:'/login',
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
                path:'/search',
                name:'search',
                component: () => import('../views/Page/Search.vue')
            },
            {
                path:'/page2',
                name:'page2',
                component: () => import('../views/Page/Page2.vue')
            },
            {
                path:'/student',
                name:'student',
                component: () => import('../views/student/Student.vue')
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





