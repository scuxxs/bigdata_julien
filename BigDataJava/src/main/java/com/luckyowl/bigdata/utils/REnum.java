package com.luckyowl.bigdata.utils;

public enum REnum {
    //状态码定义
    SUCCESS(200,"成功"),
    ERROR(-1,"发生错误");
    private Integer code;
    private String msg;

    REnum(Integer code, String msg){
        this.code = code;
        this.msg = msg;
    }

    public Integer getCode(){
        return code;
    }

    public String getMsg(){
        return msg;
    }
}
