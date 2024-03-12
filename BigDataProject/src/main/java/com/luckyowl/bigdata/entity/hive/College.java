package com.luckyowl.bigdata.entity.hive;

import lombok.Data;

@Data
public class College {

    private String major;
    /**
     * 预警类型
     * 0:late 1:cheat 2:poverty 3:politics 4:academy 5:mental
     */
    private Integer precaution_type;
    /**
     * 预警等级
     * 0\1\2\3\4
     */
    private Integer precaution_level;
    private Integer precaution_num;
}
