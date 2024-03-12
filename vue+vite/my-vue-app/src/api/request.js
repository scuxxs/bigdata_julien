/*import axios from "axios";
import config from "../config";
import {ElMessage} from "element-plus";
const NETWORK_ERROR = '网络请求异常，请稍后重试'
//创建一个axios实例对象
const service = axios.create(
    {
        baseURL:config.baseApi
    }
)
//在请求前
service.interceptors.request.use((req)=>{
    return req
})
//在请求后
service.interceptors.response.use((res)=>{
    const {code, data, msg} =res.data
    //根据后端要求而定
    if(code === 200){
        return data
    }  else if(code === 301){
        window.location.pathname = '/login'
    }
    else {

        //网络请求错误
        ElMessage.error((msg || NETWORK_ERROR))
        return Promise.reject(msg ||NETWORK_ERROR)
    }
})
export default service;*/
//封装核心函数
/* function request(options){
    {}*/
  /*  {
        method: 'get',
            data:{

    },
    mock.false
    }
*/
/*    options.method =options.method || 'get'
    if(options.method.toLowerCase()=='get'){
        options.params = options.data
    }
    //对mock的处理
    let isMock =config.mock
    if(typeof options.mock!=='undefined'){
        isMock =options.mock
    }
    //对线上环境做处理
    if(config.env =='prod'){
        service.defaults.baseURL =config.baseApi
    }else {
        service.defaults.baseURL = isMock ?  config.mockApi :config.baseApi
    }
    return service(options)
}*/

