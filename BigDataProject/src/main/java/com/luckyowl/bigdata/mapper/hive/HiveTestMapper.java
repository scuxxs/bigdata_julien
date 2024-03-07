package com.luckyowl.bigdata.mapper.hive;

import org.apache.ibatis.annotations.Mapper;

import java.util.List;
import java.util.Map;

@Mapper
public interface HiveTestMapper {
    public List<Map<String , Object>> getStudentList();
}
