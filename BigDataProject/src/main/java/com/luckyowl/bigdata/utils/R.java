package com.luckyowl.bigdata.utils;

import lombok.Data;

/**
 * 通用返回类型
 */
@Data
public class R<T> {

    //响应状态码
    private Integer code;

    //响应信息
    private String msg;

    //返回数据
    private T data;
}
