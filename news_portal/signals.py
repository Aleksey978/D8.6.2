from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Post

@receiver(pre_save, sender=Post)
def limit_news_per_user(sender, instance, **kwargs):
    if instance.pk is None:  # Проверяем, что это новая новость
        user = instance.author
        if Post.objects.filter(author=user).count() >= 3:
            raise ValueError("Вы не можете создать больше 3 новостей.")