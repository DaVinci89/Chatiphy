from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
import telegram
from telegram.error import TelegramError
from telegram.constants import ParseMode
from django.conf import settings
import asyncio


User = get_user_model()
# Отримайте токен і ID каналу з налаштувань або змінних оточення
TELEGRAM_TOKEN = settings.TELEGRAM_BOT_TOKEN  # Збережіть токен у налаштуваннях
TELEGRAM_CHANNEL_ID = settings.TELEGRAM_CHANNEL_ID  # ID вашого каналу


class Group(models.Model):
    title = models.CharField(max_length=200, default="")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(default="")

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(
        max_length=250,
        default=''
    )
    text = models.TextField(
        help_text="Enter the text of post"
    )
    slug = models.SlugField(
        max_length=200,
        blank=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True
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
    tag = TaggableManager()

    class Meta:
        ordering = ('-pub_date',)
        indexes = [
            models.Index(fields=['-pub_date'])
        ]
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    def __str__(self):
        return self.text[:15]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not self.slug or slugify(self.title) != self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        if is_new:  # Якщо це новий публічний пост, відправляємо в Telegram
            self.send_post_to_telegram()

    def send_post_to_telegram(self):
        async def async_send():
            """Відправка поста в Telegram-канал"""
            bot = telegram.Bot(token=TELEGRAM_TOKEN)
            message = (
                f"📝 **{self.title}**\n\n"
                f"{self.text[:200]}...\n\n"  # Показуємо лише перші 200 символів
                f"🔗 [Читати більше на Chatiphy]({settings.SITE_URL}{self.get_absolute_url()})"
            )
            try:
                if self.image:
                    with open(self.image.path, 'rb') as image_file:
                        await bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID,
                                             photo=image_file,
                                             caption=message,
                                             parse_mode=ParseMode.MARKDOWN
                                             )
                else:
                    await bot.send_message(
                        chat_id=TELEGRAM_CHANNEL_ID,
                        text=message,
                        parse_mode=ParseMode.MARKDOWN
                    )
            except TelegramError as e:
                # Логування помилок (можна додати логер)
                print(f"Не вдалося надіслати повідомлення в Telegram: {e}")

        asyncio.run(async_send())
    def get_absolute_url(self):
        return reverse("post_maker:post_detail", args=[self.pk, self.slug])

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    image = models.ImageField(
        "Comment Image",
        upload_to="post_maker/img/comments",
        blank=True
    )
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created",]
        indexes = [
            models.Index(fields=["created",])
        ]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )
    sub_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribers"
    )

    class Meta:
        unique_together = ("subscriber", "sub_author")
        constraints = [
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F("sub_author")),
                name="prevent_self_subscription"
            )
        ]

    def __str__(self):
        return f"{self.subscriber.username} followed {self.sub_author.username}"