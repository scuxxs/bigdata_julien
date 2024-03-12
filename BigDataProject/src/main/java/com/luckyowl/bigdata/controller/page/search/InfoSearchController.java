package com.luckyowl.bigdata.controller.page.search;

import com.luckyowl.bigdata.dto.StudentDTO;
import com.luckyowl.bigdata.entity.hive.Student;
import com.luckyowl.bigdata.service.hive.StudentService;
import com.luckyowl.bigdata.utils.R;
import com.luckyowl.bigdata.utils.RUtils;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;

@RestController
@RequestMapping("/search")
public class InfoSearchController {

    @Resource
    StudentService studentService;

    /**
     *
     */
    @PostMapping("/studentInfo")
    public R studentInfo(@RequestBody StudentDTO studentDTO){
        //todo 根据条件获取
        List<Student> studentList = null;
        studentList = studentService.getInfoByCondition(studentDTO);
        return RUtils.success(studentList);
    }

    /**
     *
     */
    @GetMapping("/all")
    public R getAllStudent(){
        List<Student> studentList = studentService.getAllStudentInfo();
        return RUtils.success(studentList);
    }

    @GetMapping("/getNum")
    public R getNumOfStudent(){
        return RUtils.success(studentService.getNumOfStudent());
    }
}
