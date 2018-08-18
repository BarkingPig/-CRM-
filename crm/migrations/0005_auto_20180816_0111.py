# Generated by Django 2.1 on 2018-08-15 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20180816_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='source',
            field=models.SmallIntegerField(choices=[(4, '51CTO'), (6, '市场推广'), (5, '知乎'), (1, 'QQ群'), (0, '转介绍'), (2, '官网'), (3, '百度推广')]),
        ),
        migrations.AlterField(
            model_name='customerfollowup',
            name='intention',
            field=models.SmallIntegerField(choices=[(3, '不报名'), (0, '两月内报名'), (2, '已报名'), (1, '一个月内报名')]),
        ),
        migrations.AlterField(
            model_name='studentrecord',
            name='attendance',
            field=models.SmallIntegerField(choices=[(1, '迟到'), (2, '缺勤'), (0, '已签到'), (3, '早退')], default=0),
        ),
        migrations.AlterField(
            model_name='studentrecord',
            name='score',
            field=models.SmallIntegerField(choices=[(70, 'B+'), (90, 'A'), (50, 'B-'), (-50, 'D'), (80, 'A-'), (30, 'c'), (20, 'c-'), (40, 'c+'), (60, 'B'), (100, 'A+')]),
        ),
    ]
