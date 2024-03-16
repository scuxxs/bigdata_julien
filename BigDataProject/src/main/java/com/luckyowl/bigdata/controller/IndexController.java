package com.luckyowl.bigdata.controller;

import com.luckyowl.bigdata.entity.hive.Student;
import com.luckyowl.bigdata.entity.mysql.User;
import com.luckyowl.bigdata.utils.LocalAccountUtil;
import com.luckyowl.bigdata.utils.R;
import com.luckyowl.bigdata.utils.RUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/index")
public class IndexController {

    /*@Autowired
    @Qualifier("hiveJdbcTemplate")
    private JdbcTemplate hiveJdbcTemplate;*/

    /*@Autowired
    @Qualifier("mysqlSqlSessionTemplate")
    private JdbcTemplate mysqlJdbcTemplate;*/


    /*@GetMapping("/showDatabase")
    public R show(){
        String sql = "select * from student";
        List<Student> lisxt = hiveJdbcTemplate.query(sql, new BeanPropertyRowMapper<>(Student.class));
        return RUtils.success(list);
    }*/

    /*@GetMapping("/showMysql")
    public R showmysql(){
        String sql = "select * from user";
        List<User> list = mysqlJdbcTemplate.query(sql, new BeanPropertyRowMapper<>(User.class));
        return RUtils.success(list);
    }*/

    @GetMapping("/test")
    public R test(){
        User user = LocalAccountUtil.getUserData();
        return RUtils.success(user, "获取到USER");
    }

    @GetMapping("/test2")
    public R test2(){
        User user = LocalAccountUtil.getUserData();
        return RUtils.success(user, "获取到USER2");
    }
}
