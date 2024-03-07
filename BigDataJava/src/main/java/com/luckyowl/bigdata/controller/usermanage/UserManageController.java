package com.luckyowl.bigdata.controller.usermanage;

import com.luckyowl.bigdata.utils.R;
import com.luckyowl.bigdata.utils.RUtils;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/userManage")
public class UserManageController {

    /**
     * 登录接口
     * @return
     */
    @RequestMapping("/login")
    public R login(){
        //todo
        String data = "loginData";
        return RUtils.success(data);
    }

    /**
     * 注册接口
     * @return
     */
    @RequestMapping("/register")
    public R register(){
        //todo
        String data = "register";
        return RUtils.success(data);
    }

    /**
     * 登出接口
     * @return
     */
    @RequestMapping("/logout")
    public R logout(){
        String data = "logout";
        return RUtils.success(data);
    }
}
