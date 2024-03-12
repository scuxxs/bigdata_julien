package com.luckyowl.bigdata.mapper.hive;

import com.luckyowl.bigdata.dto.StudentDTO;
import com.luckyowl.bigdata.entity.hive.Student;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface StudentMapper {

    List<Student> getAllStudentInfo();

    List<Student> getStudentByCondition(@Param("studentDto") StudentDTO studentDTO);

    Integer getNumOfStudent();
}
