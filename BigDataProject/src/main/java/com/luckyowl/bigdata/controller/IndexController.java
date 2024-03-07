package com.luckyowl.bigdata.controller;

import com.alibaba.fastjson.JSON;
import com.baomidou.dynamic.datasource.annotation.DS;
import com.luckyowl.bigdata.utils.R;
import com.luckyowl.bigdata.utils.REnum;
import com.luckyowl.bigdata.utils.RUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.sql.DataSource;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/index")
public class IndexController {

    @Autowired
    @Qualifier("hiveJdbcTemplate")
    private JdbcTemplate hiveJdbcTemplate;

    @Autowired
    @Qualifier("mysqlJdbcTemplate")
    private JdbcTemplate mysqlJdbcTemplate;

    @GetMapping("/showDatabase")
    public R show(){
        String sql = "select * from student";
        List<Map<String, Object>> list = hiveJdbcTemplate.queryForList(sql);
        return RUtils.success(list);
    }

    @GetMapping("/showMysql")
    public R showmysql(){
        String sql = "select * from test";
        List<Map<String, Object>> list = mysqlJdbcTemplate.queryForList(sql);
        return RUtils.success(list);
    }

}
