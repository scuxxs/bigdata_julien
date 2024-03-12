package com.luckyowl.bigdata.entity.hive;

import lombok.Data;

@Data
public class Late {

    private String id;
    private String latedate;
    private String node_name;
    private String reason;
}
