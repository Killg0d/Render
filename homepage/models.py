from django.db import models
from users.models import CustomUser
# Create your models here.


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_heading = models.CharField(max_length=255, blank=True, null=True)
    category_description = models.TextField(blank=True, null=True)
    flaticon = models.TextField()

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'categories'
        verbose_name_plural = "categories"


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')  # Add the image field
    # Add the foreign key to Category
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def get_comments(self):
        return self.comments.all()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Blogs'
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.content[:50]


class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField()
    message = models.TextField()
    given = models.BooleanField(default=False)  # Add a boolean field
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user}"

    class Meta:
        db_table = 'Feedbacks'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
