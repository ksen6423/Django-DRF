from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название",
        help_text="Введите название курса",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание курса",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="course/photo",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите изображение",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание урока",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="lesson/photo",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите изображение",
    )
    video_url = models.URLField()
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
