package com.luckyowl.bigdata.utils;

import com.luckyowl.bigdata.utils.Const.LoginTokenConst;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Cookie;
import java.util.HashMap;
import java.util.Map;

/**
 * 弃用cookie存入loginToken， 改为Header
 */
public class CookieUtil {

    public static void setAccessToken(HttpServletResponse response, Map<String, String> tokenMap){
        Cookie accessToken = new Cookie(LoginTokenConst.ACCESS_TOKEN, JwtUtil.getAccessToken());
        accessToken.setMaxAge(LoginTokenConst.ACCESS_TIME_S);
        response.addCookie(accessToken);
        tokenMap.put(LoginTokenConst.ACCESS_TOKEN, accessToken.getValue());
    }

    public static void setRefreshToken(HttpServletResponse response, Map<String, String> tokenMap){
        Cookie refreshToken = new Cookie(LoginTokenConst.REFRESH_TOKEN, JwtUtil.getRefreshToken());
        refreshToken.setMaxAge(LoginTokenConst.REFRESH_TIME_S);
        response.addCookie(refreshToken);
        tokenMap.put(LoginTokenConst.REFRESH_TOKEN, refreshToken.getValue());
    }

    /*
    public static Map<String, String> updateLoginToken(HttpServletResponse response, Map<String, String> tokenMap){
        if(tokenMap == null){
            tokenMap = new HashMap<>();
        }
        setAccessToken(response, tokenMap);
        setRefreshToken(response, tokenMap);
        return tokenMap;
    }*/
}
