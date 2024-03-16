package com.luckyowl.bigdata.dto;

import com.luckyowl.bigdata.entity.hive.Student;
import lombok.Data;

import java.util.List;
import java.util.Map;

@Data
public class PrecautionDTO {

    private Integer precautionType;

    private String msg;

    private List<Student> studentList;
}
