// 路由文件
import { createRouter, createWebHistory } from "vue-router";
const routes = [

    {
        path: '/',
        component: () => import('../views/Main.vue'),
        redirect:'/login',
        children:[
            {
                path:'/Option1',
                name:'user',
                component: () => import('../views/User/User.vue')
            },
            {
                path:'/Option2',
                name:'Option2',
                component: () => import('../views/User/Option2.vue')
            },
            {
                path:'/Option3',
                name:'Option3',
                component: () => import('../views/User/Option3.vue')
            },
            {
                path:'/Option4',
                name:'Option4',
                component: () => import('../views/User/Option4.vue')
            },
            {
                path:'/Option5',
                name:'Option5',
                component: () => import('../views/User/Option5.vue')
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





