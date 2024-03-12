package com.luckyowl.bigdata.service.mysql.impl;

import com.luckyowl.bigdata.entity.mysql.LoginToken;
import com.luckyowl.bigdata.entity.mysql.User;
import com.luckyowl.bigdata.mapper.mysql.LoginTokenMapper;
import com.luckyowl.bigdata.mapper.mysql.UserManageMapper;
import com.luckyowl.bigdata.service.mysql.LoginTokenService;
import com.luckyowl.bigdata.service.mysql.UserManageService;
import com.luckyowl.bigdata.utils.*;
import com.luckyowl.bigdata.utils.Const.HeaderUtil;
import com.luckyowl.bigdata.utils.Const.LoginTokenConst;
import com.luckyowl.bigdata.utils.Const.UserManageRConst;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletResponse;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Component
public class UserManageServiceImpl implements UserManageService {

    @Resource
    private UserManageMapper userManageMapper;

    @Resource
    private LoginTokenMapper loginTokenmapper;

    @Value("${login.secret-key}")
    private String secretKey;

    @Override
    public String getSecretKey() {
        return secretKey;
    }

    @Override
    public List<User> getAllUserInfo() {
        return userManageMapper.getAllUserInfo();
    }

    @Override
    public User getUserByUid(String uid) {
        return userManageMapper.getUserByUid(uid);
    }

    @Override
    public R loginByUser(User loginuser, String netIp ,HttpServletResponse response) {
        User existUser = getUserByUid(loginuser.getUid());
        if(existUser == null){
            return RUtils.error(UserManageRConst.INVALID_USER);
        }
        //若密码不同
        if(!BCryptUtil.matches(loginuser.getPassword(), existUser.getPassword())){
            return RUtils.error(UserManageRConst.PASSWORD_FAIL);
        }
        //密码相同，登录成功
        LocalAccountUtil.setUserData(existUser);
        //配置免密登录
        setPermission(netIp, response, existUser);
        return RUtils.success(existUser);
    }

    @Override
    public R loginByToken(String logintoken) {
        return null;
    }

    @Override
    public R registerUser(User user) {
        User existUser = getUserByUid(user.getUid());
        //如果没有存在的用户则注册，如果有则报错
        if(existUser == null){
            String encodeP = BCryptUtil.encodePassword(user.getPassword());
            user.setPassword(encodeP);
            Integer result = addUser(user);
            if(result == 1){
                return RUtils.success(user, UserManageRConst.INSERT_SUCCESS);
            }
        }
        else {
            return RUtils.error(UserManageRConst.EXIST_USER);
        }
        return RUtils.error(UserManageRConst.INSERT_FAIL);
    }

    @Override
    public Integer addUser(User user) {
        return userManageMapper.addUser(user);
    }

    @Override
    public void setPermission(String netIp, HttpServletResponse response, User user) {
        //创建免密登录token
        String accessToken = JwtUtil.getAccessToken();
        String refreshToken = JwtUtil.getRefreshToken();
        Map<String, String> tokenMap = new HashMap<>();
        tokenMap.put(LoginTokenConst.ACCESS_TOKEN, accessToken);
        tokenMap.put(LoginTokenConst.REFRESH_TOKEN, refreshToken);
        //1. 先清除数据库中历史记录：清除该ip下的loginToken
        loginTokenmapper.delLoginTokenByIp(netIp);
        //2. 存入数据库
        loginTokenmapper.addLoginToken(new LoginToken(netIp, LoginTokenConst.ACCESS_TYPE, accessToken, user.getUid()));
        loginTokenmapper.addLoginToken(new LoginToken(netIp, LoginTokenConst.REFRESH_TYPE, refreshToken, user.getUid()));
        //(弃用)3. 存入cookie
        //CookieUtil.updateLoginToken(response, tokenMap);
        //3. 存入Header
        HeaderUtil.updateLoginToken(response, tokenMap);
    }
}
