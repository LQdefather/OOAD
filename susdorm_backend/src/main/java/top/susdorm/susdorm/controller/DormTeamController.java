package top.susdorm.susdorm.controller;


import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.web.bind.annotation.*;
import jakarta.annotation.Resource;
import java.util.List;

import top.susdorm.susdorm.service.IDormTeamService;
import top.susdorm.susdorm.entity.DormTeam;


import org.springframework.web.bind.annotation.RestController;


/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author Leon
 * @since 2023-10-09
 */

@RestController

@RequestMapping("/dormTeam")
public class DormTeamController {


        @Resource
        private IDormTeamService dormTeamService;

        @PostMapping
        public boolean save(@RequestBody DormTeam dormTeam) {
                return dormTeamService.saveOrUpdate(dormTeam);
                }

        @DeleteMapping("/{id}")
        public boolean delete(@PathVariable Integer id) {
                return dormTeamService.removeById(id);
                }

        @GetMapping
        public List<DormTeam> findAll() {
                return dormTeamService.list();
                }

        @GetMapping("/{id}")
        public DormTeam findOne(@PathVariable Integer id) {
                return dormTeamService.getById(id);
                }

        @GetMapping("/page")
        public Page<DormTeam> findPage(@RequestParam Integer pageNum,
                                        @RequestParam Integer pageSize) {
                return dormTeamService.page(new Page<>(pageNum, pageSize));
                }

}

