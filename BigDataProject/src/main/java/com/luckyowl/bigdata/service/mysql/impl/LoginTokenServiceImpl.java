package com.luckyowl.bigdata.service.mysql.impl;

import com.luckyowl.bigdata.entity.mysql.LoginToken;
import com.luckyowl.bigdata.entity.mysql.User;
import com.luckyowl.bigdata.mapper.mysql.LoginTokenMapper;
import com.luckyowl.bigdata.mapper.mysql.UserManageMapper;
import com.luckyowl.bigdata.service.mysql.LoginTokenService;
import com.luckyowl.bigdata.service.mysql.UserManageService;
import com.luckyowl.bigdata.utils.Const.HeaderUtil;
import com.luckyowl.bigdata.utils.Const.LoginTokenConst;
import com.luckyowl.bigdata.utils.CookieUtil;
import com.luckyowl.bigdata.utils.JwtUtil;
import com.luckyowl.bigdata.utils.LocalAccountUtil;
import com.luckyowl.bigdata.utils.R;
import org.apache.zookeeper.Login;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

@Service
public class LoginTokenServiceImpl implements LoginTokenService {

    @Resource
    private LoginTokenMapper loginTokenMapper;

    @Resource
    private UserManageMapper userManageMapper;

    @Override
    public LoginToken getLoginTokenByIp(String ip, Integer tokenType) {
        return loginTokenMapper.getLoginTokenByIp(ip, tokenType);
    }

    @Deprecated
    @Override
    public Map<String, String> getLoginTokenFromRequest(Cookie[] cookies) {
        Map<String, String> tokenMap = new HashMap<>();
        for (Cookie cookie : cookies) {
            if(cookie.getName().equals(LoginTokenConst.ACCESS_TOKEN)){
                tokenMap.put(LoginTokenConst.ACCESS_TOKEN, cookie.getValue());
                continue;
            }
            if(cookie.getName().equals(LoginTokenConst.REFRESH_TOKEN)){
                tokenMap.put(LoginTokenConst.REFRESH_TOKEN, cookie.getValue());
            }
        }
        return tokenMap;
    }

    @Override
    public Map<String, String> getLoginTokenFromRequest(HttpServletRequest request) {
        Map<String, String> tokenMap = new HashMap<>();
        String accessToken = request.getHeader(LoginTokenConst.ACCESS_TOKEN);
        String refreshToken = request.getHeader(LoginTokenConst.REFRESH_TOKEN);
        if(accessToken != null){
            tokenMap.put(LoginTokenConst.ACCESS_TOKEN, accessToken);
        }
        if(refreshToken != null){
            tokenMap.put(LoginTokenConst.REFRESH_TOKEN, refreshToken);
        }
        return tokenMap;
    }

    @Override
    public Boolean getPermission(String ip, HttpServletRequest request, HttpServletResponse response) {
        //先解析请求携带了哪些token
        Map<String, String> requestToken = getLoginTokenFromRequest(request);
        //获取ip对应的accessToken
        if(requestToken.isEmpty()){
            return false;
        }
        //获取accessToken
        String accessToken = requestToken.getOrDefault(LoginTokenConst.ACCESS_TOKEN, null);
        //accessToken不为空 且 没过期
        if(accessToken != null && !JwtUtil.isTokenExpired(accessToken)){
            LoginToken loginToken = getLoginTokenByIp(ip, LoginTokenConst.ACCESS_TYPE);
            if(loginToken != null && loginToken.getToken().equals(requestToken.get(LoginTokenConst.ACCESS_TOKEN))){
                //获取User存入LocalAccountUtil
                User loginUser = userManageMapper.getUserByUid(loginToken.getUid());
                if(loginUser != null){
                    LocalAccountUtil.setUserData(loginUser);
                    return true;
                }
                return false;
            }
        }
        //获取refreshToken
        String refreshToken = requestToken.getOrDefault(LoginTokenConst.REFRESH_TOKEN, null);
        //refreshToken不为空 且 没过期
        if(refreshToken != null && !JwtUtil.isTokenExpired(refreshToken)){
            LoginToken loginToken = getLoginTokenByIp(ip, LoginTokenConst.REFRESH_TYPE);
            if(loginToken != null && loginToken.getToken().equals(requestToken.get(LoginTokenConst.REFRESH_TOKEN))){
                //更新accessToken和refreshToken
                //返回accessToken与refreshToken根据ip更新数据库
                Map<String, String> tokenMap = new HashMap<>();

                //弃用cookie
                //CookieUtil.updateLoginToken(response, tokenMap);
                HeaderUtil.updateLoginToken(response, tokenMap);
                //构造newRefreshLoginToken
                String newRefreshToken = tokenMap.getOrDefault(LoginTokenConst.REFRESH_TYPE, null);
                if(newRefreshToken != null){
                    LoginToken newRefreshLoginToken = new LoginToken(ip, LoginTokenConst.REFRESH_TYPE, newRefreshToken, loginToken.getUid());
                    //刷新refreshToken
                    updateLoginToken(newRefreshLoginToken);
                }
                //构造newAccessLoginToken
                String newAccessToken = tokenMap.getOrDefault(LoginTokenConst.ACCESS_TYPE, null);
                if(newAccessToken != null){
                    LoginToken newAccessLoginToken = new LoginToken(ip, LoginTokenConst.REFRESH_TYPE, newAccessToken, loginToken.getUid());
                    if(accessToken != null){
                        insertLoginToken(newAccessLoginToken);
                    }
                    else {
                        updateLoginToken(newAccessLoginToken);
                    }
                }
                //获取User存入LocalAccountUtil
                User loginUser = userManageMapper.getUserByUid(loginToken.getUid());
                if(loginUser != null){
                    LocalAccountUtil.setUserData(loginUser);
                    return true;
                }
                return false;
            }
        }
        return false;
    }

    @Override
    public Set<String> blackIpList() {
        return new HashSet<>();
    }

    @Override
    public Integer updateLoginToken(LoginToken loginToken) {
        return loginTokenMapper.updateLoginToken(loginToken);
    }

    @Override
    public Integer insertLoginToken(LoginToken loginToken) {
        return loginTokenMapper.addLoginToken(loginToken);
    }

    @Override
    public Integer deleteLoginToken(LoginToken loginToken) {
        return loginTokenMapper.delLoginToken(loginToken);
    }

    @Override
    public Integer deleteLoginTokenByIp(String ip) {
        return loginTokenMapper.delLoginTokenByIp(ip);
    }
}
