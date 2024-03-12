import Mock from 'mockjs'
import homeApi from './home.js'

//拦截请求
Mock.mock('/home/getData',homeApi.getHomeData)
