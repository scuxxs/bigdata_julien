package com.luckyowl.bigdata.service.hive.impl;

import com.luckyowl.bigdata.dto.StudentDTO;
import com.luckyowl.bigdata.entity.hive.Student;
import com.luckyowl.bigdata.mapper.hive.StudentMapper;
import com.luckyowl.bigdata.service.hive.StudentService;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;
import java.util.List;

@Component
public class StudentServiceImpl implements StudentService {

    @Resource
    private StudentMapper studentMapper;

    @Override
    public List<Student> getAllStudentInfo() {
        return studentMapper.getAllStudentInfo();
    }

    @Override
    public List<Student> getInfoByCondition(StudentDTO studentDTO) {
        return studentMapper.getStudentByCondition(studentDTO);
    }

    @Override
    public Integer getNumOfStudent() {
        return studentMapper.getNumOfStudent();
    }

}
