package com.luckyowl.bigdata.mapper.mysql;

import com.luckyowl.bigdata.entity.mysql.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Component;

import java.util.List;

@Mapper
public interface UserManageMapper {

    /**
     * 获取全部用户信息
     * @return
     */
    List<User> getAllUserInfo();

    /**
     *根据Uid获取用户信息
     */
    User getUserByUid(@Param("uid") String uid);

    /**
     * 添加用户信息
     */
    Integer addUser(@Param("user") User user);

    /**
     * 删除用户信息
     */
    Boolean delUser(String uid);

    /**
     * 修改用户信息
     */
    User editUser(User user);
}
