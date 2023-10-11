package top.susdorm.susdorm.controller;


import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.web.bind.annotation.*;
import jakarta.annotation.Resource;
import java.util.List;

import top.susdorm.susdorm.service.IAuthGroupService;
import top.susdorm.susdorm.entity.AuthGroup;


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

@RequestMapping("/authGroup")
public class AuthGroupController {


        @Resource
        private IAuthGroupService authGroupService;

        @PostMapping
        public boolean save(@RequestBody AuthGroup authGroup) {
                return authGroupService.saveOrUpdate(authGroup);
                }

        @DeleteMapping("/{id}")
        public boolean delete(@PathVariable Integer id) {
                return authGroupService.removeById(id);
                }

        @GetMapping
        public List<AuthGroup> findAll() {
                return authGroupService.list();
                }

        @GetMapping("/{id}")
        public AuthGroup findOne(@PathVariable Integer id) {
                return authGroupService.getById(id);
                }

        @GetMapping("/page")
        public Page<AuthGroup> findPage(@RequestParam Integer pageNum,
                                        @RequestParam Integer pageSize) {
                return authGroupService.page(new Page<>(pageNum, pageSize));
                }

}

