import datetime
from django.db import models


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市')
    desc = models.CharField(max_length=200, verbose_name='描述信息')
    add_time = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='机构描述')
    category = models.CharField(default='pxjg', verbose_name='机构类别', max_length=20,
                                choices=(('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')))
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='logo', max_length=100)
    address = models.CharField(max_length=150, verbose_name='地址')
    city = models.ForeignKey(CityDict, verbose_name='所在城市')
    add_time = models.DateTimeField(default=datetime.datetime.now)
    student = models.IntegerField(default=0, verbose_name='学习人数')
    course_num = models.IntegerField(default=0, verbose_name='课程数')

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构')
    name = models.CharField(max_length=10, verbose_name='教师名称')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.datetime.now)
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='头像', max_length=100,null=True)


    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
