from django.db import models


# 广告数据
# id：广告唯一标识id
# label：广告标签
# text：广告文本
# pv：点击量
# belong：所属广告主
# name：广告名称
# secondary1，2，3：广告关键词
class Ads(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField()
    pv = models.IntegerField(blank=True, null=True)
    belong = models.IntegerField(blank=True, null=True)
    secondary1 = models.CharField(max_length=255, blank=True, null=True)
    secondary2 = models.CharField(max_length=255, blank=True, null=True)
    secondary3 = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ads'


# 社交用户数据
# id：社交用户唯一标识id
# name：用户呢称
# belong：所属社交平台
# label1，2，3：一级偏好
class Customers(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    belong = models.IntegerField(blank=True, null=True)
    label1 = models.CharField(max_length=255, blank=True, null=True)
    label2 = models.CharField(max_length=255, blank=True, null=True)
    label3 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


# 标签数据
# id：标签唯一标识id
# name：标签名称
# trained：是否训练
# available：是否启用
class Label(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    trained = models.IntegerField()
    available = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'label'


# 平台用户数据
# id：平台用户唯一标识id
# email：平台用户个人email，用于登录
# password：平台用户密码，用于登录
# type：平台用户类别，0 管理员，1 社交平台， 2 广告主
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    type = models.IntegerField()
    company = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


# 语料数据
# id：每条语料文本唯一标识id
# text：文本数据
# belong：所属用户id
# secondary1，2，3：文本关键词
# label：文本标签
class Words(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.TextField(blank=True, null=True)
    belong = models.IntegerField(blank=True, null=True)
    secondary1 = models.CharField(max_length=255, blank=True, null=True)
    secondary2 = models.CharField(max_length=255, blank=True, null=True)
    secondary3 = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'words'


# 点赞数据
# id：每条点赞对唯一标识id
# cust_id：社交用户id
# ads_id：广告id
# weight：点赞权重
class Like(models.Model):
    id = models.IntegerField(primary_key=True)
    cust_id = models.IntegerField()
    ads_id = models.IntegerField()
    weight = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'like'

# class Label(models.Model):
#     name = models.CharField(max_length=255)
#     trained = models.IntegerField()
#     available = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'label'
#
#
# class User(models.Model):
#     email = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     type = models.IntegerField()
#     company = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'user'
