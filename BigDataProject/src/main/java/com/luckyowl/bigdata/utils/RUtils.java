package com.luckyowl.bigdata.utils;

public class RUtils {

    public static R trans(REnum rEnum){
        R r = new R();
        r.setCode(rEnum.getCode());
        r.setMsg(rEnum.getMsg());
        return r;
    }

    public static R transO(REnum rEnum, Object object){
        R r = trans(rEnum);
        r.setData(object);
        return r;
    }

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

    public static R success(Object object, String msg){
        R r = new R();
        r.setCode(REnum.SUCCESS.getCode());
        r.setMsg(msg);
        r.setData(object);
        return r;
    }

    public static R error(){
        R r = new R();
        r.setCode(REnum.ERROR.getCode());
        r.setMsg(REnum.ERROR.getMsg());
        return r;
    }

    public static R error(String setMsg){
        R r = new R();
        r.setCode(REnum.ERROR.getCode());
        r.setMsg(setMsg);
        return r;
    }

    public static R relogin(){
        return trans(REnum.NOLOGIN);
    }
}
