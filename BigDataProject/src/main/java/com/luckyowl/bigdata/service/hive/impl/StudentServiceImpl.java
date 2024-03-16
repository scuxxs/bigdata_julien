package com.luckyowl.bigdata.service.hive.impl;

import com.luckyowl.bigdata.dto.StudentDTO;
import com.luckyowl.bigdata.entity.hive.Student;
import com.luckyowl.bigdata.mapper.hive.StudentMapper;
import com.luckyowl.bigdata.mapper.mysql.MySQLStudentMapper;
import com.luckyowl.bigdata.service.hive.StudentService;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;
import java.util.List;

@Component
public class StudentServiceImpl implements StudentService {

    @Resource
    private StudentMapper studentMapper;

    @Resource
    private MySQLStudentMapper mySQLStudentMapper;

    @Override
    public List<Student> getAllStudentInfo() {
        Integer studentNum = mySQLStudentMapper.getNumOfStudent();
        List<Student> studentList;
        if(studentNum < 1000){
            studentList = studentMapper.getAllStudentInfo();
            mySQLStudentMapper.insertStudent(studentList);
        }
        else{
            studentList = mySQLStudentMapper.getAllStudentInfo();
        }
        return studentList;
    }

    @Override
    public List<Student> getInfoByCondition(StudentDTO studentDTO) {
        return studentMapper.getStudentByCondition(studentDTO);
    }

    @Override
    public Integer getNumOfStudent() {
        return studentMapper.getNumOfStudent();
    }

    @Override
    public List<Student> getLate() {
        return studentMapper.getLate();
    }

    @Override
    public List<Student> getCheat() {
        return studentMapper.getCheat();
    }

    @Override
    public List<Student> getPoverty() {
        return studentMapper.getPoverty();
    }

    @Override
    public List<Student> getPolitics() {
        return studentMapper.getPolitics();
    }

    @Override
    public List<Student> getAcademy() {
        return studentMapper.getAcademy();
    }

    @Override
    public List<Student> getMental() {
        return studentMapper.getMental();
    }

    @Override
    public List<Student> getStudent(Student student) {
        return studentMapper.getStudent(initStudent(student));
    }

    public Student initStudent(Student student){
        if(student.getId() == null){
            student.setId("");
        }
        if(student.getName() == null){
            student.setName("");
        }
        if(student.getMajor() == null){
            student.setMajor("");
        }
        if(student.getCollege() == null){
            student.setCollege("");
        }
        return student;
    }

}
