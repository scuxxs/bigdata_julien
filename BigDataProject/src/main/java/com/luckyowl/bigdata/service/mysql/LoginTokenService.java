package com.luckyowl.bigdata.service.mysql;

import com.luckyowl.bigdata.entity.mysql.LoginToken;
import com.luckyowl.bigdata.utils.R;
import org.apache.zookeeper.Login;
import org.springframework.stereotype.Service;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

@Service
public interface LoginTokenService {

    /**
     * 根据Ip获取LoginToken信息
     */
    LoginToken getLoginTokenByIp(String ip, Integer tokenType);

    /**
     * 获取http请求cookie中的LoginToken
     */
    @Deprecated
    Map<String, String> getLoginTokenFromRequest(Cookie[] cookies);

    /**
     * 获取http请求header中的LoginToken
     */
    Map<String, String> getLoginTokenFromRequest(HttpServletRequest request);

    /**
     * 获取免密放行权限
     */
    Boolean getPermission(String ip, HttpServletRequest request, HttpServletResponse response);

    /**
     * 获取ip黑名单
     */
    Set<String> blackIpList();

    /**
     * 更新LoginToken
     */
    Integer updateLoginToken(LoginToken loginToken);

    /**
     * 插入LoginToken
     */
    Integer insertLoginToken(LoginToken loginToken);

    /**
     * 删除LoginToken
     */
    Integer deleteLoginToken(LoginToken loginToken);

    /**
     * 通过 ip 删除LoginToken
     */
    Integer deleteLoginTokenByIp(String ip);
}
