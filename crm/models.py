from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import gettext_lazy as _  # 国际化
from django.utils.safestring import mark_safe  # 渲染
# Create your models here.

# class UserProfile(models.Model):
#     """账号表"""
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # 也是关联外键 一张表
#     # 只可以关联一次 Django只带的用户表 User
#     name = models.CharField(max_length=32)
#     roles = models.ManyToManyField("Role", blank=True, null=True)
#
#     # 多对多的关联
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = "账号表"
class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):  # 普通用户
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('用户名必须是邮箱')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)  #  密码加密 哈希 错位
        self.is_active = True   # 是否活跃（是否可以登录）
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):  # 超级用户
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    '''账号表'''
    email = models.EmailField(  #
        verbose_name='邮箱',  # 别名
        max_length=255,  # 最大长度
        unique=True,  # 是否唯一
        null=True  # 是否可为空
    )
    name = models.CharField(max_length=32)
    password = models.CharField(_('password'), max_length=128,
                                help_text=mark_safe("<a href='password'>修改密码</a>"))  # 密码  # 在数据库里储存渲染好的前端代码
    is_active = models.BooleanField(default=True)  # 是否活跃的
    is_admin = models.BooleanField(default=False)  # 是否是管理员
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)  # 上次登陆时间
    objects = UserProfileManager()  # 密码加密

    USERNAME_FIELD = 'email'  # 以email做主键做用户名
    REQUIRED_FIELDS = ['name']  # 创建用户时哪些字段是必须的

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name_plural = "账号表"

class Customer(models.Model):
    """客户信息表"""
    name = models.CharField(max_length=32, blank=True, null=True)
    qq = models.CharField(max_length=64, unique=True)
    qq_name = models.CharField(max_length=64, blank=True, null=True)
    source_choices = {(0, "转介绍"),
                      (1, "QQ群"),
                      (2, "官网"),
                      (3, "百度推广"),
                      (4, "51CTO"),
                      (5, "知乎"),
                      (6, "市场推广")
                      }
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.CharField(max_length=64, verbose_name="转介绍人的QQ", blank=True, null=True)

    consult_course = models.ForeignKey("Course", verbose_name="咨询课程", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="咨询详情")
    consultant = models.ForeignKey("UserProfile", on_delete=models.CASCADE)  # 账号
    date = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField("Tag", blank=True, null=True)

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name_plural = "客户信息表"


class Tag(models.Model):
    """标签表"""
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "标签表"


class CustomerFollowUp(models.Model):
    """客户跟进表"""
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="跟进内容")
    consultant = models.ForeignKey("UserProfile", on_delete=models.CASCADE)  # 跟进人
    data = models.DateTimeField(auto_now_add=True)  # 跟进时间
    intention_choices = {(0, "两月内报名"),
                         (1, "一个月内报名"),
                         (2, "已报名"),
                         (3, "不报名"),
                         }
    intention = models.SmallIntegerField(choices=intention_choices)

    def __str__(self):
        return "<%s:%s>" % (self.customer.qq, self.intention)

    class Meta:
        verbose_name_plural = "客户跟进表"


class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=64, unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name="周期（月）")
    outline = models.TextField(verbose_name="课程大纲")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "课程表"


class Branch(models.Model):
    """校区表"""
    name = models.CharField(max_length=128, unique=True)
    addr = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "校区表"


class ClassList(models.Model):
    """班级表"""
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile")
    class_type_choices = {(0, "面授"),
                          (1, "网络"),
                          (2, "脱产"),
                          }
    class_type = models.SmallIntegerField(verbose_name="班级类型", choices=class_type_choices)
    start_date = models.DateTimeField(verbose_name="开班日期")
    end_date = models.DateTimeField(verbose_name="结业日期", blank=True, null=True)

    def __str__(self):
        return "%s %s %s" % (self.branch, self.course, self.semester)

    class Meta:  # 联合唯一
        verbose_name_plural = "班级表"
        unique_together = ('branch', 'course', 'semester')


class CourseRecord(models.Model):
    """上课记录表"""
    from_class = models.ForeignKey("ClassList", verbose_name="上课班级", on_delete=models.CASCADE)
    teacher = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name="第几节课")

    has_homework = models.BooleanField(default=True, verbose_name="是否有作业")
    homework_title = models.CharField(max_length=128, blank=True, null=True, verbose_name="作业名称")
    homework_content = models.TextField(verbose_name="作业内容", blank=True, null=True)
    outline = models.TextField(verbose_name="本节课大纲")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.from_class, self.day_num)

    class Meta:
        verbose_name_plural = "上课记录表"
        unique_together = ('from_class', 'day_num')  # 联合唯一


class StudentRecord(models.Model):
    """学生学习记录表"""
    student = models.ForeignKey("Enrollment", on_delete=models.CASCADE)
    course_record = models.ForeignKey("Customer", on_delete=models.CASCADE)
    attendance_choices = {(0, "已签到"),
                          (1, "迟到"),
                          (2, "缺勤"),
                          (3, "早退"),
                          }
    attendance = models.SmallIntegerField(choices=attendance_choices, default=0)
    score_choices = {(100, "A+"),
                     (90, "A"),
                     (80, "A-"),
                     (70, "B+"),
                     (60, "B"),
                     (50, "B-"),
                     (40, "c+"),
                     (30, "c"),
                     (20, "c-"),
                     (-50, "D"),
                     }
    score = models.SmallIntegerField(choices=score_choices)
    memo = models.TextField(verbose_name="作业备注", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" % (self.student, self.course_record, self.score)

    class Meta:
        verbose_name_plural = "学生学习记录表"
        unique_together = ('student', 'course_record')  # 联合唯一


class Enrollment(models.Model):
    """报名表"""
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey("ClassList", verbose_name="所报班级", on_delete=models.CASCADE)
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问", on_delete=models.CASCADE)
    contract_approved = models.BooleanField(default=True, verbose_name="合同已审核")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.customer, self.enrolled_class)

    class Meta:
        verbose_name_plural = "报名表"
        unique_together = ('customer', 'enrolled_class')


class Payment(models.Model):
    """缴费记录表"""
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", verbose_name="所报课程", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name="数额", default=500)
    consultant = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.customer, self.amount)

    class Meta:
        verbose_name_plural = "缴费记录表"


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=32, unique=True)
    menus = models.ManyToManyField("Menu", blank=True, verbose_name="菜单")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "角色表"


class Menu(models.Model):
    """角色对应的菜单表"""
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)  # 菜单的路径

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "角色对应的菜单表"
