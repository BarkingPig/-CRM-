# Generated by Django 2.1 on 2018-10-16 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, null=True, unique=True, verbose_name='邮箱')),
                ('password', models.CharField(help_text="<a href='password'>修改密码</a>", max_length=128, verbose_name='password')),
                ('name', models.CharField(max_length=32, verbose_name='用户名')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': '账号表',
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('address', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name_plural': '校区表',
            },
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='班级名')),
                ('semester', models.PositiveSmallIntegerField(verbose_name='学期')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Branch', verbose_name='校区')),
            ],
            options={
                'verbose_name_plural': '班级表',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='课程名')),
                ('period', models.PositiveSmallIntegerField(verbose_name='周期（星期）')),
                ('outline', models.TextField(verbose_name='课程大纲')),
            ],
            options={
                'verbose_name_plural': '课程表',
            },
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.PositiveSmallIntegerField(verbose_name='第几节课')),
                ('has_homework', models.BooleanField(default=True, verbose_name='是否有作业')),
                ('homework_title', models.CharField(blank=True, max_length=128, null=True, verbose_name='作业名称')),
                ('homework_content', models.TextField(blank=True, null=True, verbose_name='作业内容')),
                ('outline', models.TextField(verbose_name='本节课大纲')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='上课时间')),
                ('from_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ClassList', verbose_name='上课班级')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教学老师')),
            ],
            options={
                'verbose_name_plural': '上课记录表',
            },
        ),
        migrations.CreateModel(
            name='Dorm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('address', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'verbose_name_plural': '宿舍表',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.PositiveIntegerField(unique=0, verbose_name='成绩')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Course', verbose_name='课程')),
            ],
            options={
                'verbose_name_plural': '成绩表',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('url_name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name_plural': '角色对应的菜单表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('menus', models.ManyToManyField(blank=True, to='crm.Menu', verbose_name='菜单')),
            ],
            options={
                'verbose_name_plural': '角色表',
            },
        ),
        migrations.CreateModel(
            name='Sanitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='检测日期')),
                ('attendance', models.SmallIntegerField(choices=[(0, '非常干净'), (3, '卫生差'), (1, '干净'), (2, '比较干净')], default=1)),
                ('dorm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Dorm', verbose_name='宿舍')),
            ],
            options={
                'verbose_name_plural': '宿舍卫生表',
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'verbose_name_plural': '专业表',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('attendance', models.SmallIntegerField(choices=[(1, '女'), (0, '男')], default=1)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='登录时间')),
                ('dorm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Dorm', verbose_name='宿舍')),
                ('enrolled_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ClassList', verbose_name='所在班级')),
            ],
            options={
                'verbose_name_plural': '学生表',
            },
        ),
        migrations.CreateModel(
            name='StudentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.SmallIntegerField(choices=[(2, '缺勤'), (1, '迟到'), (0, '已签到'), (4, '请假'), (3, '早退')], default=0)),
                ('score', models.SmallIntegerField(choices=[(40, 'A'), (20, 'C'), (30, 'B'), (10, 'D'), (0, 'D-')], verbose_name='平时成绩')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='上课记录时间')),
                ('course_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.CourseRecord', verbose_name='课程')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Student')),
            ],
            options={
                'verbose_name_plural': '学生上课记录表',
            },
        ),
        migrations.AddField(
            model_name='grade',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Student', verbose_name='学生'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='course',
            field=models.ManyToManyField(to='crm.Course', verbose_name='课程'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Specialty', verbose_name='专业'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='班主任'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(blank=True, null=True, to='crm.Role'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='stu_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Student', verbose_name='关联学生账号'),
        ),
        migrations.AlterUniqueTogether(
            name='studentrecord',
            unique_together={('student', 'course_record')},
        ),
        migrations.AlterUniqueTogether(
            name='courserecord',
            unique_together={('from_class', 'day_num')},
        ),
    ]
