from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, default="")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(default="")

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        help_text="Enter the text of post"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Author",
        related_name="posts"
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
        verbose_name="Group",
        help_text="Choose the group"
    )
    image = models.ImageField(
        "Post Image",
        upload_to="post_maker/img",
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    def __str__(self):
        return self.text[:15]
