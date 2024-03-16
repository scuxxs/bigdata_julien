package com.luckyowl.bigdata.entity.mysql;

import lombok.Data;

@Data
public class LoginToken {

    //网络IP
    private String netIp;

    //token类型 0:accessToken 1:refreshToken
    private Integer tokenType;

    //免登录访问token
    private String token;

    //用户uid
    private String uid;

    public LoginToken(String netIp, Integer tokenType, String token, String uid){
        this.netIp = netIp;
        this.tokenType = tokenType;
        this.token = token;
        this.uid = uid;
    }
}
