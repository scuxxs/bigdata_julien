package com.luckyowl.bigdata.controller.test;

import com.luckyowl.bigdata.service.hive.StudentService;
import com.luckyowl.bigdata.service.mysql.UserManageService;
import com.luckyowl.bigdata.utils.R;
import com.luckyowl.bigdata.utils.RUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


import javax.annotation.Resource;

@RestController
@RequestMapping("/test")
public class testController {

    @Resource
    private UserManageService userManageService;

    @Resource
    private StudentService studentService;


    @GetMapping("/getSecret")
    public R getSecret(){
        return RUtils.success(userManageService.getSecretKey());
    }

    @GetMapping("/getAllUser")
    public R getAllUser(){
        return RUtils.success(userManageService.getAllUserInfo());
    }

    @GetMapping("/getAllStudent")
    public R getAllStudent(){
        return RUtils.success(studentService.getAllStudentInfo());
    }

}
