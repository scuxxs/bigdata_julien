package com.luckyowl.bigdata.config;

import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.SqlSessionTemplate;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;

import javax.sql.DataSource;

@Configuration
@MapperScan(basePackages = "com.luckyowl.bigdata.mapper.hive",sqlSessionFactoryRef = "hiveSqlSessionFactory")
public class HiveDataSourceConfig {

    @Bean(name = "hiveDataSource")
    @ConfigurationProperties(prefix = "spring.datasource.hive")
    public DataSource getHiveDataSource(){
        return DataSourceBuilder.create().build();
    }

    @Bean("hiveSqlSessionFactory")
    public SqlSessionFactory hiveSqlSessionFactory(@Qualifier("hiveDataSource") DataSource dataSource) throws Exception{
        SqlSessionFactoryBean bean = new SqlSessionFactoryBean();
        bean.setDataSource(dataSource);
        bean.setMapperLocations(
                new PathMatchingResourcePatternResolver().getResources("classpath*:mapper/hive/*.xml")
        );
        return bean.getObject();
    }

    @Bean("hiveSqlSessionTemplate")
    public SqlSessionTemplate hiveSqlSessionTemplate(@Qualifier("hiveSqlSessionFactory") SqlSessionFactory sessionFactory){
        return new SqlSessionTemplate(sessionFactory);
    }
}
