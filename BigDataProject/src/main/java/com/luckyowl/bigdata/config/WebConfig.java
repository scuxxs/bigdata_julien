package com.luckyowl.bigdata.config;

import com.luckyowl.bigdata.interceptors.AuthorityInterceptor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Value("${enable-loginToken}")
    private Boolean useLoginToken;

    @Bean
    public AuthorityInterceptor getAuthorityInterceptor(){
        return new AuthorityInterceptor();
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        if(useLoginToken){
            //配置权限验证拦截器
            registry.addInterceptor(getAuthorityInterceptor())
                    .addPathPatterns("/**")
                    .excludePathPatterns("/userManage/**","/test/**");
        }
    }
}

