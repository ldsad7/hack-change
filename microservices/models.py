from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField


class Author(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True,
                                  verbose_name="Имя ответственного за микросервис")
    last_name = models.CharField(max_length=255, blank=True, null=True,
                                 verbose_name="Фамилия ответственного за микросервис")
    phone_number = PhoneNumberField(blank=True, null=True, unique=True, verbose_name="Номер телефона")
    position = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name="Должность ответственного за микросервис")

    def __str__(self):
        return f"{self.last_name} {self.first_name}, {self.phone_number}"

    class Meta:
        verbose_name = "Ответственный"
        verbose_name_plural = "Ответственные"


class Microservice(TimeStampedModel):
    IDEA = 'idea'
    DESIGN = 'design'
    DEV = 'development'
    TEST = 'text'
    REVISION = 'revision'
    SUPPORT = 'support'
    STATUS = Choices(
        (IDEA, "Идея"), (DESIGN, "Проектирование"), (DEV, "Разработка"), (TEST, "Тестирование"),
        (REVISION, "В доработке"), (SUPPORT, "Поддержка")
    )

    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название микросервиса")
    description = models.TextField(blank=True, null=True, verbose_name="Описание микросервиса")
    author = models.ForeignKey(Author, blank=False, null=False, verbose_name="Ответственный за микросервис",
                               on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, default=DEV, max_length=32, verbose_name="Статус микросервиса")
    external_id = models.IntegerField(blank=False, null=False, verbose_name="ID микросервиса", unique=True)
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="Время начала работы над микросервисом")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Время завершения работы над микросервисом")
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.external_id}"

    class Meta:
        verbose_name = "Микросервис"
        verbose_name_plural = "Микросервисы"


class Tag(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название тега")
    description = models.TextField(blank=True, null=True, verbose_name="Описание тега")
    microservice = models.ManyToManyField(Microservice, blank=True)


class Pair(TimeStampedModel):
    A_TO_B = '>'
    B_TO_A = '<'
    A_EQ_B = '='
    STATUS = Choices(A_TO_B, B_TO_A, A_EQ_B)

    first_microservice = models.ForeignKey(
        Microservice, blank=False, null=False, related_name='first_microservices',
        verbose_name="Первый микросервис в паре", on_delete=models.CASCADE
    )
    second_microservice = models.ForeignKey(
        Microservice, blank=False, null=False, related_name='second_microservices',
        verbose_name="Второй микросервис в паре", on_delete=models.CASCADE
    )
    connection = models.CharField(choices=STATUS, default=A_TO_B, max_length=32, verbose_name="Направление связи")
