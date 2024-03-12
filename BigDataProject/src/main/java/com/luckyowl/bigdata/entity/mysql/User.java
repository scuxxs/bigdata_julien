package com.luckyowl.bigdata.entity.mysql;

import lombok.Data;

@Data
public class User {
    private String uid;
    private String password;
    private String nickname;
    private Boolean authorization;
}
