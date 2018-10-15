from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import gettext_lazy as _  # 国际化
from django.utils.safestring import mark_safe  # 渲染


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

        user.set_password(password)  # 密码加密 哈希 错位
        self.is_active = True  # 是否活跃（是否可以登录）
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
    password = models.CharField(_('password'), max_length=128,
                                help_text=mark_safe("<a href='password'>修改密码</a>"))  # 密码  # 在数据库里储存渲染好的前端代码
    name = models.CharField(max_length=32, )
    is_active = models.BooleanField(default=True)  # 是否活跃的
    is_admin = models.BooleanField(default=False)  # 是否是管理员
    roles = models.ManyToManyField("Role", blank=True)
    objects = UserProfileManager()  # 密码加密
    stu_account = models.ForeignKey("Student", verbose_name="关联学生账号", blank=True, null=True,
                                    on_delete=models.CASCADE)  # 可以为空 可以不填

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


class Student(models.Model):
    """学生表"""
    name = models.CharField(max_length=32)
    dorm = models.ForeignKey("Dorm", on_delete=models.CASCADE, verbose_name="宿舍")
    gender_choices = {(0, "男"),
                        (1, "女"),
                      }
    attendance = models.SmallIntegerField(choices=gender_choices, default=1)
    enrolled_class = models.ForeignKey("ClassList", verbose_name="所在班级", on_delete=models.CASCADE )
    date = models.DateTimeField(auto_now_add=True, verbose_name="登录时间")

    def __str__(self):
        return "%s %s" % (self.name, self.enrolled_class)

    class Meta:
        verbose_name_plural = "学生表"

class Grade(models.Model):
    """成绩表"""
    course = models.ManyToManyField("Course", verbose_name="课程")
    student = models.ManyToManyField("Student", verbose_name="学生")
    grade = models.PositiveIntegerField(verbose_name="成绩", unique=0)

    def __str__(self):
        return "%d" % (self.grade,)

    class Meta:
        verbose_name_plural = "成绩表"



class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=64, unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name="周期（星期）")
    outline = models.TextField(verbose_name="课程大纲")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "课程表"


class Branch(models.Model):
    """校区表"""
    name = models.CharField(max_length=128, unique=True)
    address = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "校区表"


class Dorm(models.Model):
    """宿舍表"""
    name = models.CharField(max_length=64, unique=True)
    address = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "宿舍表"


class Sanitation(models.Model):
    """宿舍卫生表"""
    dorm = models.ManyToManyField("Dorm", verbose_name="宿舍")
    date = models.DateTimeField(verbose_name="检测日期")
    sanitation_choices = {(0, "非常干净"),
                          (1, "干净"),
                          (2, "比较干净"),
                          (3, "卫生差"),
                          }
    attendance = models.SmallIntegerField(choices=sanitation_choices, default=1)
    def __str__(self):
        return "%s" % (self.dorm,)

    class Meta:
        verbose_name_plural = "宿舍卫生表"



class Specialty(models.Model):
    """专业表"""
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "专业表"


class ClassList(models.Model):
    """班级表"""
    name = models.CharField(max_length=64, unique=True)
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE, verbose_name="校区")
    course = models.ManyToManyField("Course", verbose_name="课程")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ForeignKey("UserProfile", on_delete=models.CASCADE, verbose_name="班主任")
    specialty = models.ForeignKey("Specialty", on_delete=models.CASCADE, verbose_name="专业")

    def __str__(self):
        return "%s" % (self.name)

    class Meta:  # 联合唯一
        verbose_name_plural = "班级表"



class CourseRecord(models.Model):
    """老师班级上课记录表，确认老师来上课（老师自己填）"""
    from_class = models.ForeignKey("ClassList", verbose_name="上课班级", on_delete=models.CASCADE)
    teacher = models.ForeignKey("UserProfile", on_delete=models.CASCADE, verbose_name="教学老师")
    day_num = models.PositiveSmallIntegerField(verbose_name="第几节课")
    has_homework = models.BooleanField(default=True, verbose_name="是否有作业")
    homework_title = models.CharField(max_length=128, blank=True, null=True, verbose_name="作业名称")
    homework_content = models.TextField(verbose_name="作业内容", blank=True, null=True)
    outline = models.TextField(verbose_name="本节课大纲")
    date = models.DateTimeField(auto_now_add=True, verbose_name="上课时间")

    def __str__(self):
        return "%s %s" % (self.from_class, self.day_num)

    class Meta:
        verbose_name_plural = "上课记录表"
        unique_together = ('from_class', 'day_num')  # 联合唯一


class StudentRecord(models.Model):
    """学生上课记录表(老师登记，确认学生来上课)"""
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    course_record = models.ForeignKey("CourseRecord", on_delete=models.CASCADE, verbose_name="课程")  # 外键
    attendance_choices = {(0, "已签到"),
                          (1, "迟到"),
                          (2, "缺勤"),
                          (3, "早退"),
                          (4, "请假"),
                          }
    attendance = models.SmallIntegerField(choices=attendance_choices, default=0)
    score_choices = {(40, "A"),
                     (30, "B"),
                     (20, "C"),
                     (10, "D"),
                     (0, "D-"),
                     }
    score = models.SmallIntegerField(choices=score_choices, verbose_name="平时成绩", )
    memo = models.TextField(verbose_name="作业备注", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="上课记录时间")

    def __str__(self):
        return "%s %s" % (self.course_record, self.score)

    class Meta:
        verbose_name_plural = "学生上课记录表"
        unique_together = ('student', 'course_record')  # 联合唯一


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



