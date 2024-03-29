package com.luckyowl.bigdata.interceptors;

import com.luckyowl.bigdata.entity.mysql.LoginToken;
import com.luckyowl.bigdata.service.mysql.LoginTokenService;
import com.luckyowl.bigdata.utils.IpUtil;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.sql.Date;
import java.util.Set;

@Component
public class AuthorityInterceptor implements HandlerInterceptor {

    @Resource
    private LoginTokenService loginTokenService;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {

        //获取URI
        String getURI = request.getRequestURI();

        //获取Ip
        String ipAddress = IpUtil.getIpFromRequest(request);
        if(ipAddress == null){
            return false;
        }

        //黑名单过滤
        Set<String> blaskIpList = loginTokenService.blackIpList();
        if(blaskIpList != null && blaskIpList.contains(ipAddress)){
            return false;
        }

        //根据ip获取请求免密放行权限
        if(loginTokenService.getPermission(ipAddress, request, response)){
            return true;
        }
        //未登录
        response.sendRedirect("/userManage/reLogin");
        return false;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        HandlerInterceptor.super.postHandle(request, response, handler, modelAndView);
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        HandlerInterceptor.super.afterCompletion(request, response, handler, ex);
    }
}
