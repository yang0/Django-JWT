from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError("请填入手机号码！")
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, mobile, password, **extra_fields):
        # extra_fields['is_superuser'] = False
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password, **extra_fields):
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        return self._create_user(mobile, password, **extra_fields)


class AgentOrSaleManOrOperate(AbstractBaseUser, PermissionsMixin):
    account = models.CharField(verbose_name='用户邮箱', max_length=32, null=True, blank=True)
    mobile = models.CharField(verbose_name='联系手机号', max_length=11, unique=True)
    name = models.CharField(verbose_name='联系人姓名', max_length=32, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    USERNAME_FIELD = 'mobile'

    objects = UserManager()

    def __str__(self):
        return 'mobile={}'.format(self.mobile)

    class Meta:
        db_table = 'agent_saleman_operate'
        verbose_name = verbose_name_plural = '代理商或者销售代表或者运营表'