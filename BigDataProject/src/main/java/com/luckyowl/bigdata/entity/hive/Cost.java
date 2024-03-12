package com.luckyowl.bigdata.entity.hive;

import lombok.Data;

@Data
public class Cost {

    private String id;
    private String record_id;
    private String transdate;
    private String transtime;
    private Float amount;
    private String type;
}
