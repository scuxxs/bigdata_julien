package com.luckyowl.bigdata.service.hive;

import com.luckyowl.bigdata.dto.StudentDTO;
import com.luckyowl.bigdata.entity.hive.Student;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface StudentService {

    List<Student> getAllStudentInfo();

    /**
     * 根据学生模版中有的属性获取学生
     * @param studentDTO
     * @return
     */
    List<Student> getInfoByCondition(StudentDTO studentDTO);

    Integer getNumOfStudent();

}
