package com.luckyowl.bigdata.entity.hive;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
public class Student {
    private String id;
    private String name;
    private String college;
    private String major;
    private String node_name;
    private Integer late_level;
    private Integer cheat_level;
    private Integer poverty_level;
    private Integer politics_level;
    private Integer academy_level;
    private Integer mental_level;
    private Integer total_grade;

    public Integer getPrecautionLevelByType(Integer precaution_type){
        switch (precaution_type){
            case 0:
                return getLate_level();
            case 1:
                return getCheat_level();
            case 2:
                return getPoverty_level();
            case 3:
                return getPolitics_level();
            case 4:
                return getAcademy_level();
            case 5:
                return getMental_level();
            default:
                return -1;
        }
    }
}
