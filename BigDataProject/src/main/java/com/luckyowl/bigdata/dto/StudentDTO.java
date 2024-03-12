package com.luckyowl.bigdata.dto;

import lombok.Data;

import java.util.List;

@Data
public class StudentDTO {
    private List<String> id;
    private List<String> name;
    private List<String> college;
    private List<String> major;
    private List<String> node_name;
    private List<Integer> late_level;
    private List<Integer> cheat_level;
    private List<Integer> poverty_level;
    private List<Integer> politics_level;
    private List<Integer> academy_level;
    private List<Integer> total_grade;
}
