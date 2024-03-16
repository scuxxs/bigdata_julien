package com.luckyowl.bigdata.controller.precaution;

import com.luckyowl.bigdata.dto.PrecautionDTO;
import com.luckyowl.bigdata.service.mysql.PrecautionService;
import com.luckyowl.bigdata.utils.R;
import com.luckyowl.bigdata.utils.REnum;
import com.luckyowl.bigdata.utils.RUtils;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.*;

@RestController
@RequestMapping("/precaution")
public class PrecautionController {

    @Resource
    private PrecautionService precautionService;

    private static List<Integer> validType = Arrays.asList(0,1,2,3,4);

    /**
     * 传入数据合法性处理
     */
    private R checkData(PrecautionDTO precautionDTO){
        if(precautionDTO == null){
            return RUtils.error("数据为空!");
        }
        if(!validType.contains(precautionDTO.getPrecautionType())){
            return RUtils.error("预警类型错误!");
        }
        //todo 其他数据合法性校验
        return RUtils.success();
    }

    /**
     * 晚归预警
     */
    @RequestMapping("/late")
    public R precautionLate(@RequestBody PrecautionDTO precautionDTO){
        //todo
        R r = checkData(precautionDTO);
        if(!Objects.equals(r.getCode(), REnum.SUCCESS.getCode())){
            return r;
        }
        r = precautionService.sendPrecaution(precautionDTO);
        return r;
    }

    @RequestMapping("/late/student")
    public R precationLateStudent(@RequestParam("uid") String uid){
        return precautionService.getPrecautionByUid(uid);
    }

    /**
     * 防诈预警
     */
    @RequestMapping("/cheat")
    public R precautionCheat(@RequestBody PrecautionDTO precautionDTO){
        //todo
        R r = checkData(precautionDTO);
        if(!Objects.equals(r.getCode(), REnum.SUCCESS.getCode())){
            return r;
        }
        return RUtils.success();
    }

    /**
     * 贫困预警
     */
    @RequestMapping("/poverty")
    public R precautionPoverty(@RequestBody PrecautionDTO precautionDTO){
        //todo
        R r = checkData(precautionDTO);
        if(!Objects.equals(r.getCode(), REnum.SUCCESS.getCode())){
            return r;
        }
        return RUtils.success();
    }

    /**
     * 政治预警
     */
    @RequestMapping("/politics")
    public R precautionPolitics(@RequestBody PrecautionDTO precautionDTO){
        //todo
        R r = checkData(precautionDTO);
        if(!Objects.equals(r.getCode(), REnum.SUCCESS.getCode())){
            return r;
        }
        return RUtils.success();
    }

    /**
     * 学术预警
     */
    @RequestMapping("/academy")
    public R precautionAcademy(@RequestBody PrecautionDTO precautionDTO){
        //todo
        R r = checkData(precautionDTO);
        if(!Objects.equals(r.getCode(), REnum.SUCCESS.getCode())){
            return r;
        }
        return RUtils.success();
    }

    /**
     * 心理预警
     */
    @RequestMapping("/mental")
    public R precautionMental(@RequestBody PrecautionDTO precautionDTO){
        //todo
        R r = checkData(precautionDTO);
        if(!Objects.equals(r.getCode(), REnum.SUCCESS.getCode())){
            return r;
        }
        return RUtils.success();
    }
}
