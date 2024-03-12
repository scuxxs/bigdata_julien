package com.luckyowl.bigdata.service.mysql.impl;

import com.luckyowl.bigdata.dto.PrecautionDTO;
import com.luckyowl.bigdata.dto.StudentDTO;
import com.luckyowl.bigdata.entity.hive.Student;
import com.luckyowl.bigdata.entity.mysql.Precaution;
import com.luckyowl.bigdata.mapper.mysql.PrecautionMapper;
import com.luckyowl.bigdata.service.mysql.PrecautionService;
import com.luckyowl.bigdata.utils.R;
import com.luckyowl.bigdata.utils.RUtils;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.List;

@Service
public class PrecautionServiceImpl implements PrecautionService {

    @Resource
    private PrecautionMapper precautionMapper;

    @Override
    public R sendPrecaution(PrecautionDTO dto) {
        List<Precaution> precautionList = new ArrayList<>();
        String msg = dto.getMsg();
        Integer precaution_type = dto.getPrecautionType();
        for (Student student : dto.getStudentList()) {
            Precaution precaution = new Precaution();
            precaution.setUid(student.getId());
            precaution.setPrecaution_type(precaution_type);
            precaution.setPrecaution_level(student.getPrecautionLevelByType(precaution_type));
            precaution.setMsg(msg);
            precaution.setIs_read(0);
            precautionList.add(precaution);
        }
        Integer insertNum = -1;
        try {
            insertNum = precautionMapper.sendPrecaution(precautionList);
        }
        catch (Exception e){
            return RUtils.error("插入数据失败!");
        }
        return RUtils.success(null, "成功发送:"+insertNum+"条预警信息!");
    }

    @Override
    public R getPrecautionByUid(String uid) {
        List<Precaution> precautionList = precautionMapper.getPrecautionByUid(uid);
        return RUtils.success(precautionList);
    }
}
