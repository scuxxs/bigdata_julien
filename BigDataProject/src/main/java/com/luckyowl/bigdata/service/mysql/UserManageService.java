package com.luckyowl.bigdata.service.mysql;

import com.luckyowl.bigdata.entity.mysql.User;
import com.luckyowl.bigdata.utils.R;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletResponse;
import java.util.List;

@Service
public interface UserManageService {

    /**
     * 获取加密秘钥
     */
    String getSecretKey();

    /**
     * 获取全部用户信息
     */
    List<User> getAllUserInfo();

    /**
     * 根据Uid获取用户信息
     */
    User getUserByUid(String uid);

    /**
     * 登录服务 - 密码登录
     */
    R loginByUser(User user, String ip, HttpServletResponse response);

    /**
     * 登录服务 - JWT登录
     */
    @Deprecated
    R loginByToken(String logintoken);

    /**
     * 注册服务
     */
    R registerUser(User user);

    /**
     * 插入用户到数据库
     */
    Integer addUser(User user);

    /**
     * 用户免密登录配置
     * 1. token存入数据库
     * 2. token存入cookie
     */
    void setPermission(String netIp, HttpServletResponse response, User user);
}
