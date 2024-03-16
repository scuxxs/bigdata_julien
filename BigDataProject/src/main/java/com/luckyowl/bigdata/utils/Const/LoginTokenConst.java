package com.luckyowl.bigdata.utils.Const;

public final class LoginTokenConst {

    public final static Integer ACCESS_TYPE = 0;

    public final static Integer REFRESH_TYPE = 1;

    public final static String ACCESS_TOKEN = "access_token";

    public final static String REFRESH_TOKEN = "refresh_token";

    // 定义了 JWT 的过期时间，这里设置为 2 小时
    public final static long ACCESS_TIME = 86400000 / 12; // 24 hours in milliseconds

    // 定义了 JWT 的刷新时间，这里设置为 24 小时
    public final static long REFRESH_TIME = 86400000;

    //以秒为单位
    public final static Integer ACCESS_TIME_S = 86400 / 12;

    public final static Integer REFRESH_TIME_S = 86400;
}
