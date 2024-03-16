package com.luckyowl.bigdata.utils;

import com.luckyowl.bigdata.entity.mysql.User;

public class LocalAccountUtil {

    private static final ThreadLocal<User> userData = new ThreadLocal<>();

    public static User getUserData() {
        return userData.get();
    }

    public static void setUserData(User data) {
        userData.set(data);
    }

    public static void clearUserData() {
        userData.remove();
    }
}
