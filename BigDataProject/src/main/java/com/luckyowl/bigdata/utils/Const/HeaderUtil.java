package com.luckyowl.bigdata.utils.Const;

import com.luckyowl.bigdata.utils.JwtUtil;

import javax.servlet.http.HttpServletResponse;
import java.util.HashMap;
import java.util.Map;

public class HeaderUtil {

    public static Map<String, String> updateLoginToken(HttpServletResponse response, Map<String, String> tokenMap){
        String accessToken = JwtUtil.getAccessToken();
        String refreshToken = JwtUtil.getRefreshToken();
        if(tokenMap == null){
            tokenMap = new HashMap<>();
        }
        tokenMap.put(LoginTokenConst.ACCESS_TOKEN, accessToken);
        tokenMap.put(LoginTokenConst.REFRESH_TOKEN, refreshToken);
        response.addHeader(LoginTokenConst.ACCESS_TOKEN, accessToken);
        response.addHeader(LoginTokenConst.REFRESH_TOKEN, refreshToken);
        return tokenMap;
    }
}
