from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.serializers import ModelSerializer


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100, blank=True, verbose_name="Name")
    date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name="Date of Birth")
    location = models.CharField(max_length=100, blank=True, verbose_name="Location")
    bio = models.TextField(blank=True, verbose_name="About myself")
    profile_image = models.ImageField(upload_to="users/img", blank=True, verbose_name="Avatar")

    def __str__(self):
        return f"Profile: {self.user.username}"

    # Метод для збереження шляху до фото
    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return '/static/default_avatar.jpg'

    # Автоматично створювати профіль після реєстрації
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'name', 'date_of_birth', 'location', 'bio', 'profile_image')

