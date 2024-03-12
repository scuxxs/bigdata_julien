package com.luckyowl.bigdata.utils;

import com.luckyowl.bigdata.utils.Const.LoginTokenConst;
import io.jsonwebtoken.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.Date;

@Component
public class JwtUtil {

    private static String SECRET_KEY;

    @Value("${login.secret-key}")
    public void setSecretKey(String secretKey) {
        JwtUtil.SECRET_KEY = secretKey;
    }

    private static String generateJwt(String subject, long time) {
        Date now = new Date();
        Date expirationDate = new Date(now.getTime() + time);

        return Jwts.builder()
                .setSubject(subject)
                .setIssuedAt(now)
                .setExpiration(expirationDate)
                .signWith(SignatureAlgorithm.HS256, generateHmacSha256Key(SECRET_KEY))
                .compact();
    }

    public static String getAccessToken(){
        return generateJwt(LoginTokenConst.ACCESS_TOKEN, LoginTokenConst.ACCESS_TIME);
    }

    public static String getRefreshToken(){
        return generateJwt(LoginTokenConst.REFRESH_TOKEN, LoginTokenConst.REFRESH_TIME);
    }

    public static boolean isTokenExpired(String token) {
        try {
            Claims claims = Jwts.parser().setSigningKey(generateHmacSha256Key(SECRET_KEY)).parseClaimsJws(token).getBody();
            Date expirationDate = claims.getExpiration();
            return expirationDate.before(new Date());
        } catch (ExpiredJwtException | UnsupportedJwtException | MalformedJwtException | SignatureException | IllegalArgumentException e) {
            // Token 解析失败，也认为是过期的
            return true;
        }
    }

    public static byte[] generateHmacSha256Key(String key) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hashedKey = digest.digest(key.getBytes(StandardCharsets.UTF_8));

            // 截取前32个字节作为HMAC-SHA256密钥
            return Arrays.copyOf(hashedKey, 32);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace(); // 处理异常
            return null;
        }
    }

}
