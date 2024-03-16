package com.luckyowl.bigdata.mapper.mysql;

import com.luckyowl.bigdata.entity.mysql.LoginToken;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.zookeeper.Login;
import org.springframework.security.core.parameters.P;

@Mapper
public interface LoginTokenMapper {

    /**
     * 根据ip获取loginToken
     */
    LoginToken getLoginTokenByIp(@Param("netIp") String ip, @Param("tokenType") Integer tokenType);

    /**
     * 根据 ip 和 tokenType 更新loginToken
     */
    Integer updateLoginToken(@Param("loginToken") LoginToken loginToken);

    /**
     * 插入 loginToken
     */
    Integer addLoginToken(@Param("loginToken") LoginToken loginToken);

    /**
     * 删除 loginToken
     */
    Integer delLoginToken(@Param("loginToken") LoginToken loginToken);

    /**
     * 根据 ip 删除 loginToken
     */
    Integer delLoginTokenByIp(@Param("netIp") String ip);
}
