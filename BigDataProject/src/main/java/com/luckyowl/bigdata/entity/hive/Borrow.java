package com.luckyowl.bigdata.entity.hive;

import lombok.Data;

@Data
public class Borrow {

    private String id;
    private String loandate;
    private String returndate;
    private int renewtime;
    private int recalltime;
    private String isbn;
}
