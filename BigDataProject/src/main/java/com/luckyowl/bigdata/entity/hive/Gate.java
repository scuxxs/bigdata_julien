package com.luckyowl.bigdata.entity.hive;

import lombok.Data;

@Data
public class Gate {

    private String id;
    private String type;
    private String record_time;
    private Integer is_vocation;
}
