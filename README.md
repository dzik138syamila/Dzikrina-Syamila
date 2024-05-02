# Django-Blog for Learning HTML/CSS

# Read more..

Untuk membuat model hingga menampilkan halaman template HTML di Django, Anda perlu mengikuti beberapa langkah dasar. Berikut adalah langkah-langkah umumnya:

1. **Membuat Aplikasi Django**: Pastikan Anda telah membuat aplikasi Django menggunakan perintah `django-admin startproject namaproyek`.
2. **Membuat Aplikasi**: Buat aplikasi di dalam proyek Django Anda dengan menggunakan perintah `python manage.py startapp namaaplikasi`.
(Langka 1, 2 telah dijelaskan dalam pertemuan sebelumnya)
3. **Definisikan Model**: Dalam file `models.py` di aplikasi Anda, definisikan model Anda dengan properti dan relasi yang sesuai.
>Model telah tersedia.. Scroll down.
4. **Migrasi Database**: Jalankan perintah `python manage.py makemigrations` dan `python manage.py migrate` untuk membuat dan menerapkan migrasi ke basis data.
5. **Membuat Tampilan (Views)**: Buat tampilan di file `views.py` aplikasi Anda untuk menangani permintaan HTTP dan berinteraksi dengan model.
>Views telah tersedia.. Scroll down.
6. **Definisikan URL**: Tentukan URL untuk tampilan Anda di dalam file `urls.py` aplikasi Anda atau proyek Anda. 
>URL telah tersedia.. Scroll down.
7. **Buat Template HTML**: Buat file template HTML di dalam direktori `templates` di dalam direktori aplikasi Anda.
>HTML telah tersedia.. Scroll down.

8. **Jalankan Server Django**: Jalankan server pengembangan Django dengan perintah `python manage.py runserver`.

9. **Akses Halaman**: Buka browser dan akses halaman yang sesuai dengan URL yang telah Anda tentukan, misalnya `http://localhost:8000/`.

Dengan mengikuti langkah-langkah ini, Anda dapat membuat model, menampilkan data dari model tersebut di halaman template HTML, dan menangani permintaan HTTP menggunakan Django. Pastikan untuk menyesuaikan nama model, tampilan, URL, dan template sesuai dengan kebutuhan aplikasi Anda.

# PROJECT BLOG

# Buat Model:

## 1. Definisikan kelas model:
[File Model.py](https://github.com/hermantoXYZ/django-blog/blob/main/blog/models.py)
```
# blog/models.py

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=100)
 
    def __str__(self):
        return self.category

class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='page_images/')
    slug = models.SlugField(unique=True, max_length=255)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.IntegerField(choices=[
        (0, 'Draft'),
        (1, 'Published'),
    ], default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

```
## 2. Migrasi Basis Data:

Buat migrasi dengan menjalankan perintah 
```
python manage.py makemigrations
```
Terapkan migrasi dengan menjalankan perintah 
```
python manage.py migrate
```


## 3. Untuk menampilkan model-model yang Anda buat di Django Admin, Anda dapat melakukan langkah-langkah berikut:

[File Admin.py](https://github.com/hermantoXYZ/django-blog/blob/main/blog/admin.py)
```
# blog/admin.py

from django.contrib import admin
from .models import Category, Page, Blog

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug')
    prepopulated_fields = {'slug': ('category',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_date', 'published_date')
    list_filter = ('category', 'status', 'created_date', 'published_date')
    search_fields = ('title', 'author', 'content')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Blog, BlogAdmin)

```

untuk memastikan, cek dashboard admin login ke 
- http://127.0.0.1:8000/admin/ 

![Admin Dashboard](https://github.com/hermantoXYZ/django-blog/blob/main/screnshoots/1.JPG)

## 4. Buat sebuah fungsi tampilan baru di views.py untuk menampilkan models.py

[File views.py](https://github.com/hermantoXYZ/django-blog/blob/main/blog/views.py)

```
# blog/views.py

from django.shortcuts import render, get_object_or_404
from .models import Category, Page, Blog

def home(request):
    categories = Category.objects.all()
    pages = Page.objects.filter(is_published=True)
    posts = Blog.objects.filter(status=1)
    return render(request, 'home.html', {'categories': categories, 'pages': pages, 'posts': posts})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def post_list(request):
    posts = Blog.objects.filter(status=1)
    return render(request, 'post_list.html', {'posts': posts})

def page_list(request):
    pages = Page.objects.filter(is_published=True)
    return render(request, 'page_list.html', {'pages': pages})

def post_detail(request, slug):
    post = get_object_or_404(Blog, slug=slug, status=1)
    return render(request, 'post_detail.html', {'post': post})

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'page_detail.html', {'page': page})

```


## 5 Tambahkan pola URL yang mengarah ke fungsi

```
# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.category_list, name='category_list'),
    path('posts/', views.post_list, name='post_list'),
    path('pages/', views.page_list, name='page_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
]


```

## 6 Menampilkan daftar halaman di template HTML

[File Template HTML](https://github.com/hermantoXYZ/django-blog/tree/main/templates)

![List HTMl](https://github.com/hermantoXYZ/django-blog/blob/main/screnshoots/2.JPG)

## Page website Blog
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/categories/ (list Categories)
- http://127.0.0.1:8000/posts/ (List Post)
- http://127.0.0.1:8000/pages/ (list pages)
- http://127.0.0.1:8000/post/url-post/ (Detail Post)
- http://127.0.0.1:8000/page/about/ contoh page dengan nama about


![List Galery](https://github.com/hermantoXYZ/django-blog/blob/main/screnshoots/3.JPG)
![List Galery](https://github.com/hermantoXYZ/django-blog/blob/main/screnshoots/4.JPG)
![List Galery](https://github.com/hermantoXYZ/django-blog/blob/main/screnshoots/5.JPG)
![List Galery](https://github.com/hermantoXYZ/django-blog/blob/main/screnshoots/6.JPG)
![List Galery](https://github.com/hermantoXYZ/django-blog/blob/main/screnshoots/7.JPG)
![List Galery](https://github.com/hermantoXYZ/django-blog/blob/main/screnshoots/8.JPG)

## License <a name="license"></a>
HermantoZYZ. Check `LICENSE`.
