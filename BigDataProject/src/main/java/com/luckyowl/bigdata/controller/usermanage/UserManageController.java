package com.luckyowl.bigdata.controller.usermanage;

import com.luckyowl.bigdata.entity.mysql.User;
import com.luckyowl.bigdata.service.mysql.UserManageService;
import com.luckyowl.bigdata.utils.*;
import com.luckyowl.bigdata.utils.Const.UserManageRConst;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@RestController
@RequestMapping("/userManage")
public class UserManageController {

    @Resource
    private UserManageService userManageService;

    /**
     * 登录接口
     * @return
     */
    @RequestMapping("/login")
    public R login(@RequestBody User loginuser, HttpServletRequest request, HttpServletResponse response){
        String netIp = IpUtil.getIpFromRequest(request);
        return userManageService.loginByUser(loginuser, netIp, response);
    }

    /**
     * 登录接口(测试)
     */
    @RequestMapping("/loginTest")
    public R login(){
        return RUtils.success("LoginTest");
    }

    @GetMapping("/getUser")
    public R getUser(HttpServletRequest request, HttpServletResponse response) throws IOException {
        User user = LocalAccountUtil.getUserData();
        if(user == null){
            response.sendRedirect("/userManage/reLogin");
        }
        return RUtils.success(user);
    }

    /**
     * 登录失败重新登录
     * @param
     * @return
     */
    @GetMapping("/reLogin")
    public R reLogin(){
        R r = RUtils.relogin();
        return RUtils.relogin();
    }

    /**
     * 注册接口
     * @return
     */
    @PostMapping("/register")
    public R register(@RequestBody User user){
        return userManageService.registerUser(user);
    }

    /**
     * 登出接口
     * @return
     */
    @RequestMapping("/logout")
    public R logout(){
        //todo 登出
        return RUtils.success();
    }

    /**
     * 获取加密密码
     */
    @RequestMapping("/encodePassword")
    public R getEncode(@RequestBody User user){
        return RUtils.success(BCryptUtil.encodePassword(user.getPassword()));
    }
}
