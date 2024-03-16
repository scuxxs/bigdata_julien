package com.luckyowl.bigdata.entity.mysql;

import lombok.Data;

@Data
public class Precaution {

    private String uid;
    private Integer precaution_type;
    private Integer precaution_level;
    private String msg;
    private Integer is_read;
}
