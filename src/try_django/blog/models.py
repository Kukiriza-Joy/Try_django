from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Q

User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):
        lookup = (Q(title__icontains=query)|
                  Q(content__icontains=query)|
                  Q(slug__icontains=query)|
                  Q(user__first_name__icontains=query)|
                  Q(user__last_name__icontains=query)|
                  Q(user__username__icontains=query)
                  )
        return self.filter(lookup)

class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)

# Create your models here.
class BlogPost(models.Model):
    user    = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    image   = models.ImageField(upload_to='image/', blank=True,null=True)
    title   = models.TextField(max_length=120)
    slug    = models.SlugField(unique=True)
    content = models.TextField(null=True,blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BlogPostManager()

    class Meta:
        ordering = ['-publish_date', '-updated', '-timestamp']

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url}/delete"
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")
class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()
    STATUS_CHOICES = {
        ('draft', 'Draft'),
        ('published', 'Published')
    }

    title    = models.CharField(max_length=100)
    slug     = models.SlugField(max_length=120)
    author   = models.ForeignKey(User, related_name='blog_post', null=True, on_delete=models.SET_NULL)
    body     = models.TextField()
    likes    = models.ManyToManyField(User, related_name='likes', blank=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post      = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    user      = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    content   = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))
