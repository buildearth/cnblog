from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserInfo(AbstractUser):
    """
    用户信息表
    """
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to='avatars/', default='/avatars/default.png')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    blog = models.OneToOneField(to='Blog', null=True)


class Blog(models.Model):
    """
    站点表，每个人注册完成之后都有自己专有的一个站点，就像购物中每个人都有一个自己的购物车一样
    """
    title = models.CharField(max_length=64, verbose_name="个人博客标题")
    site_name = models.CharField(max_length=64, verbose_name="站点名称")
    theme = models.CharField(max_length=32, verbose_name="博客主题")

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    个人站点文章分类
    """
    title = models.CharField(max_length=32, verbose_name="分类标题")
    blog = models.ForeignKey(to='Blog', verbose_name="所属博客")

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    个人站点的 标签
    """
    title = models.CharField(max_length=32, verbose_name="标签名称")
    blog = models.ForeignKey(to='Blog', verbose_name="所属博客")

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=64, verbose_name="文章标题")
    desc = models.CharField(max_length=255, verbose_name="文章描述")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    content = models.TextField()

    # 下面三个字段是为了在文章展示时，不在进行跨表查询从而提高效率的
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    user = models.ForeignKey(to='UserInfo', verbose_name="作者")
    category = models.ForeignKey(to='Category', null=True)
    tags = models.ManyToManyField(to='Tag', through='Article2Tag', through_fields=('article', 'tag'))

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article', verbose_name="文章")
    tag = models.ForeignKey(to='Tag', verbose_name="标签")

    class Meta:
        unique_together = [
            ('article', 'tag')
        ]

    def __str__(self):
        return self.article.title + "---" + self.tag.title


class ArticleUpDown(models.Model):
    user = models.ForeignKey(to='UserInfo', null=True)
    article = models.ForeignKey(to='Article', null=True)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            ('article', 'user')
        ]


class Comment(models.Model):
    content = models.CharField(max_length=255, verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    article = models.ForeignKey(to='Article', verbose_name="评论文章")
    user = models.ForeignKey(to='UserInfo', verbose_name="评论者")
    parent_comment = models.ForeignKey(to='self', null=True)

    def __str__(self):
        return self.content