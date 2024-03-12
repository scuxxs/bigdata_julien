package com.luckyowl.bigdata.mapper.mysql;

import com.luckyowl.bigdata.dto.PrecautionDTO;
import com.luckyowl.bigdata.entity.mysql.Precaution;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface PrecautionMapper {

    Integer sendPrecaution(@Param("dataList") List<Precaution> precautionList);

    List<Precaution> getPrecautionByUid(@Param("uid") String uid);
}
