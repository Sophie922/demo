from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    fio = models.CharField("ФИО", max_length=255)
    phone = models.CharField("Телефон", max_length=20)

    def __str__(self):
        return self.username


class Course(models.Model):
    title = models.CharField("Название курса", max_length=255)
    category = models.CharField("Категория", max_length=100, default='Общее')

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    start_date = models.DateField("Дата начала")
    payment_method = models.CharField("Способ оплаты", max_length=50)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка #{self.id}"


class Review(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='review')
    text = models.TextField("Отзыв")
    created_at = models.DateTimeField(auto_now_add=True)