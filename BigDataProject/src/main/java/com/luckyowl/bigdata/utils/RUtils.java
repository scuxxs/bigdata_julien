package com.luckyowl.bigdata.utils;

public class RUtils {

    public static R success(Object object){
        R r = new R();
        r.setCode(REnum.SUCCESS.getCode());
        r.setMsg(REnum.SUCCESS.getMsg());
        r.setData(object);
        return r;
    }

    public static R success(){
        R r = new R();
        r.setCode(REnum.SUCCESS.getCode());
        r.setMsg(REnum.SUCCESS.getMsg());
        return r;
    }

    public static R error(){
        R r = new R();
        r.setCode(REnum.ERROR.getCode());
        r.setMsg(REnum.ERROR.getMsg());
        return r;
    }
}
