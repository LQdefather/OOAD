package top.susdorm.susdorm.service.impl;

import top.susdorm.susdorm.entity.AuthUser;
import top.susdorm.susdorm.mapper.AuthUserMapper;
import top.susdorm.susdorm.service.IAuthUserService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author Leon
 * @since 2023-10-09
 */
@Service
public class AuthUserServiceImpl extends ServiceImpl<AuthUserMapper, AuthUser> implements IAuthUserService {

}
