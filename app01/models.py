from django.db import models


# Create your models here.

# class UserInfo(models.Model):
#     name = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#     age = models.IntegerField()
class Department(models.Model):
    """部门表"""
    name = models.CharField(max_length=32, verbose_name='部门名称')

    def __str__(self):
        return self.name


class User(models.Model):
    """员工表"""
    name = models.CharField(max_length=16, verbose_name="姓名")
    password = models.CharField(max_length=64, verbose_name="密码")
    age = models.IntegerField(verbose_name="年龄")
    account_balance = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")
    # 外键约束
    # to 表示与哪张表关联
    # to_field 表示表中的哪一列
    # 在django中,数据表中的名称自动加上_id,也就是depart_id
    # on_delete=models.CASCADE 表示级联删除(删除部门,部门下的所有员工都会被删除)
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE, verbose_name="部门")
    # on_delete=models.SET_NULL, null=True, blank=True 表示置空(删除部门,部门下的所有员工的部门字段置为空)
    # depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.SET_NULL, null=True, blank=True)mi
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(choices=gender_choices, verbose_name="性别")


class Pretty(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=32)
    price = models.IntegerField(verbose_name="价格", default=0)
    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Admin(models.Model):
    """管理员表 """
    name = models.CharField(max_length=16, verbose_name="姓名")
    password = models.CharField(max_length=64, verbose_name="密码")
