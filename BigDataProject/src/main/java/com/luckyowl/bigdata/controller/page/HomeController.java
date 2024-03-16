package com.luckyowl.bigdata.controller.page;

import com.luckyowl.bigdata.utils.R;
import com.luckyowl.bigdata.utils.RUtils;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/home")
public class HomeController {

    @GetMapping("/inithome")
    public R getHome(){
        return RUtils.success();
    }
}
