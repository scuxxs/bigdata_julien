// 路由文件
import { createRouter, createWebHistory } from "vue-router";
//import Home from '../views/home/Home.vue'
const routes = [

    {
        path: '/',
        component: () => import('../views/Main.vue'),
        redirect:'/login',
        children:[
            // {
            //     path:'/home',
            //     name:'home',
            //     component: () => import('../views/home/Home.vue')
            // },
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
                path: '/warning',
                name: 'warning',
                component: () => import('../views/Page/Warning.vue')
            },
            {
                path: '/latewarning',
                name: 'latewarning',
                component: () => import('../views/Page/Latewarning.vue')
            },
            {
                path: '/cheatwarning',
                name: 'cheatwarning',
                component: () => import('../views/Page/Cheatwarning.vue')
            },
            {
                path: '/mentalwarning',
                name: 'mentalwarning',
                component: () => import('../views/Page/Mentalwarning.vue')
            },
            {
                path: '/politicswarning',
                name: 'politicswarning',
                component: () => import('../views/Page/Politicswarning.vue')
            },
            {
                path: '/povertywarning',
                name: 'povertywarning',
                component: () => import('../views/Page/Povertywarning.vue')
            },
        ]
    },
    {
        path: '/login',
        component: () => import('../components/LoginView.vue')

    },
    {
        path:'/student',
        name:'student',
        component: () => import('../views/student/Student.vue')
    },

]

const router = createRouter({
    history: createWebHistory(),
    routes
})
export default router;





