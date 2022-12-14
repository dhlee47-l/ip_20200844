from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/tag/{self.slug}/'

#다대일 관계
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

#다대일 관계
class Company(models.Model):
    #제조사명
    name = models.CharField(max_length=50, unique=True)
    #주소
    address = models.TextField()
    #연락처
    phone = models.CharField(max_length=11, unique=True)
    #이메일(추가 필드)
    email = models.TextField(max_length=254, unique=True)

    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/company/{self.slug}/'

    class Meta:
        verbose_name_plural = 'companies'

class Post(models.Model):
    #상품명
    title = models.CharField(max_length=30)
    #간단한 설명
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    #상품 이미지
    images = models.ImageField(upload_to='shop/images/%Y/%m/%d/', blank=True)
    #상품 가격
    price = models.IntegerField()
    #그 외의 필드(상품코드)
    product_code= models.CharField(max_length=30, blank=True)
    #제조사 포함
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
    #Category 포함
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    #다대다 관계 필드 포함
    tags = models.ManyToManyField(Tag, blank=True)

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'