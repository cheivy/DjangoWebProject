from django.db import models
import datetime
# Create your models here.

from django.db import models

# 简繁转换历史表
class History(models.Model):
    input = models.CharField(max_length=200, verbose_name="输入内容")
    output = models.CharField(max_length=200, verbose_name="输出内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="查询时间")

    class Meta:
        verbose_name = "简繁转换记录"

# 小篆查询独立历史表
class XiaoZhuanHistory(models.Model):
    char = models.CharField(max_length=10, verbose_name="查询汉字")
    info = models.CharField(max_length=300, verbose_name="字形信息")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="查询时间")

    class Meta:
        verbose_name = "小篆查询记录"
