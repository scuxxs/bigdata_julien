// 引入 axios
import axios from 'axios';

// 创建 axios 实例
const api = axios.create({
    baseURL: '' ,// 替换为你的 API 地址
    timeout: 30000, // 请求超时时间
});

// 请求拦截器
api.interceptors.request.use(
    (config) => {
        // 在请求发送之前，检查本地存储中是否有 accessToken
        const accessToken = localStorage.getItem('accessToken');
        const refreshToken = localStorage.getItem('refreshToken');
        // 如果存在 accessToken，则将其添加到请求头中
        if (accessToken) {
            config.headers['access_token'] = ` ${accessToken}`;
        }
        if (refreshToken) {
            config.headers['refresh_token'] = ` ${refreshToken}`;
        }
        return config;
    },
    // (error) => {
    //     return Promise.reject(error);
    // }
);

// 导出实例
export default api;