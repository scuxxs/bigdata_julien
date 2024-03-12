/*
const env = import.meta.env.MODE || "prod";

const EnvConfig ={
    development: {
        baseApi:'/api',
        mockApi:'https://mock.apifox.com/m1/4068509-0-default/api',
    },
    test: {
        baseApi:'//test.future.com/api',
        mockApi:'https://mock.apifox.com/m1/4068509-0-default/api',
    },
    pro: {
        baseApi:'//future.com/api',
        mockApi:'https://mock.apifox.com/m1/4068509-0-default/api',
    },
};
export default {
    env,
    //mock 总开关
    mock: true,
    ...EnvConfig[env],
};
*/
export default {
    baseUrl: {
        dev: '/api/',  //开发环境
        pro: '',       //生产环境
    }
};