package top.susdorm.susdorm.controller;


import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.web.bind.annotation.*;
import jakarta.annotation.Resource;
import java.util.List;

import top.susdorm.susdorm.service.IAuthUserService;
import top.susdorm.susdorm.entity.AuthUser;


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

@RequestMapping("/authUser")
public class AuthUserController {


        @Resource
        private IAuthUserService authUserService;

        @PostMapping
        public boolean save(@RequestBody AuthUser authUser) {
                return authUserService.saveOrUpdate(authUser);
                }

        @DeleteMapping("/{id}")
        public boolean delete(@PathVariable Integer id) {
                return authUserService.removeById(id);
                }

        @GetMapping
        public List<AuthUser> findAll() {
                return authUserService.list();
                }

        @GetMapping("/{id}")
        public AuthUser findOne(@PathVariable Integer id) {
                return authUserService.getById(id);
                }

        @GetMapping("/page")
        public Page<AuthUser> findPage(@RequestParam Integer pageNum,
                                        @RequestParam Integer pageSize) {
                return authUserService.page(new Page<>(pageNum, pageSize));
                }

}

