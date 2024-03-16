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
    private StudentService studentService;

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

    @PostMapping("/getStudent")
    public R getStudent(@RequestBody Student student){
        List<Student> studentList = null;
        studentList = studentService.getStudent(student);
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

    @GetMapping("/getLate")
    public R getLate(){
        List<Student> studentList = studentService.getLate();
        return RUtils.success(studentList);
    }

    @GetMapping("/getCheat")
    public R getCheat(){
        List<Student> studentList = studentService.getCheat();
        return RUtils.success(studentList);
    }

    @GetMapping("/getPoverty")
    public R getPoverty(){
        List<Student> studentList = studentService.getPoverty();
        return RUtils.success(studentList);
    }

    @GetMapping("/getPolitics")
    public R getPolitics(){
        List<Student> studentList = studentService.getPolitics();
        return RUtils.success(studentList);
    }

    @GetMapping("/getAcademy")
    public R getAcademy(){
        List<Student> studentList = studentService.getAcademy();
        return RUtils.success(studentList);
    }

    @GetMapping("/getMental")
    public R getMental(){
        List<Student> studentList = studentService.getMental();
        return RUtils.success(studentList);
    }
}
