package com.luckyowl.bigdata.utils;

import javax.servlet.http.HttpServletRequest;

public class IpUtil {

    public static String getIpFromRequest(HttpServletRequest request){
        String ipAddress = request.getHeader("X-Forwarded-For");
        if(ipAddress == null){
            ipAddress = request.getRemoteAddr();
        }
        return ipAddress;
    }
}
