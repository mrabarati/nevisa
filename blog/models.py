from django.db                  import models
from django.urls                import reverse
from django.utils               import timezone
from account.models             import User
from extentions.utils           import jalali_converter
from django.utils.html          import format_html

from django.contrib.contenttypes.fields import GenericRelation

from comment.models import Comment




class ArticleManager(models.Manager):

    def published(self):
        return self.filter(status = 'p')

class CategoryManager(models.Manager):

    def active(self):
        return self.filter(status = True)


class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آیپی')


    class Meta:
        verbose_name = 'آدرس آیپی'
        verbose_name_plural = 'آدرس های آیپی'


class Category(models.Model):

    parent = models.ForeignKey('self', default=None, null=True,blank=True, on_delete=models.SET_NULL,related_name='children', verbose_name='زیر دسته') 
    title = models.CharField(max_length = 200,verbose_name="عنوان دسته بندی")
    slug  = models.SlugField(max_length = 100 ,unique = True, verbose_name="آدرس دسته بندی")
    status    = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    position  = models.IntegerField(verbose_name='پوزیشن')
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['parent__id','position']

    def __str__(self) -> str:
        return self.title
    
    objects = CategoryManager()

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', "پیش نویس"),      #draft
        ('p', "منتشر شده"),     #publish
        ('i', "درحال برسی"),    #investigation
        ('b', "برگشت داده شده") #back
    )
    
    author      = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name ='نویسنده')
    slug        = models.SlugField(max_length = 100 ,unique = True, verbose_name="آدرس مقاله")
    title       = models.CharField(max_length = 200,verbose_name="عنوان مقاله")
    status      = models.CharField(max_length=1,choices=STATUS_CHOICES,verbose_name="وضعیت انتشار")
    publish     = models.DateTimeField(default=timezone.now,verbose_name="تاریخ انتشار مقاله")
    created     = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ایجاد مقاله")
    updated     = models.DateTimeField(auto_now=True,verbose_name="آخرین تاریخ آپدیت")
    category    = models.ManyToManyField(Category, verbose_name='دسته بندی',related_name='articles')
    thunbnail   = models.ImageField(upload_to="images",verbose_name="تصویر مقاله")
    description = models.TextField(verbose_name= "محتوا")
    
    #این برای این هست که ایا مقاله خاص هست یا نه؟ دیفالت میدیم برای همه فالس
    is_special  = models.BooleanField(default=False, verbose_name="مقاله ویژه")
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IpAddress, through="ArticleHit", blank=True, related_name="hits", verbose_name="بازدیدها")
    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ['-publish']
    def __str__(self) -> str:
        return self.title
    
    def jpublish(self):
        return jalali_converter(self.publish)
    
    jpublish.short_description = 'زمان انتشار'

    def category_published(self):
        return self.category.filter(status=True)
    
    def get_absolute_url(self):
        return reverse("account:home")
    
    def thunbnail_tag(self):
        return format_html("<img width='100' height='75' style='border-radius: 5px;' src = '{}'>".format(self.thunbnail.url))
    thunbnail_tag.short_description = 'عکس'

    def category_to_str(self):
        return ','.join([category.title for category in self.category.active()])
    category_to_str.short_description = 'دسته بندی'

    objects = ArticleManager()


class ArticleHit(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	ip_address = models.ForeignKey(IpAddress, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)



