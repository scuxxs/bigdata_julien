package com.luckyowl.bigdata.service.mysql;

import com.luckyowl.bigdata.dto.PrecautionDTO;
import com.luckyowl.bigdata.dto.StudentDTO;
import com.luckyowl.bigdata.utils.R;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface PrecautionService {

    R sendPrecaution(PrecautionDTO dto);

    /**
     * 根据uid查询预警管理的预警信息
     * @param uid
     * @return
     */
    R getPrecautionByUid(String uid);
}
