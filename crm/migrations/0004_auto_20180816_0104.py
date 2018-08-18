# Generated by Django 2.1 on 2018-08-15 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20180816_0052'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='menu',
            new_name='menus',
        ),
        migrations.AlterField(
            model_name='classlist',
            name='class_type',
            field=models.SmallIntegerField(choices=[(1, '网络'), (0, '面授'), (2, '脱产')], verbose_name='班级类型'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='source',
            field=models.SmallIntegerField(choices=[(4, '51CTO'), (6, '市场推广'), (0, '转介绍'), (2, '官网'), (1, 'QQ群'), (5, '知乎'), (3, '百度推广')]),
        ),
        migrations.AlterField(
            model_name='customerfollowup',
            name='intention',
            field=models.SmallIntegerField(choices=[(3, '不报名'), (1, '一个月内报名'), (2, '已报名'), (0, '两月内报名')]),
        ),
        migrations.AlterField(
            model_name='studentrecord',
            name='attendance',
            field=models.SmallIntegerField(choices=[(3, '早退'), (0, '已签到'), (2, '缺勤'), (1, '迟到')], default=0),
        ),
        migrations.AlterField(
            model_name='studentrecord',
            name='score',
            field=models.SmallIntegerField(choices=[(-50, 'D'), (70, 'B+'), (20, 'c-'), (100, 'A+'), (50, 'B-'), (90, 'A'), (40, 'c+'), (60, 'B'), (80, 'A-'), (30, 'c')]),
        ),
    ]