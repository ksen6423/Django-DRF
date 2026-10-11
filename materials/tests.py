from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        """ Создание тестового пользователя для авторизации. """

        self.user = User.objects.create(
            email='admin@email.com'
        )

        self.course = Course.objects.create(
            name='Test_Course_1',
            description='Test_Course_1',
            owner=self.user)

        self.lesson = Lesson.objects.create(
            name='Test_Lesson_3',
            description='Test_Lesson_3',
            owner=self.user,
            course=self.course,
        )

        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        """Тест создания курса."""

        url = reverse("materials:courses-list")

        data = {
            "name": "Test_Course_1",
            "description": "Test_Course_1"
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("name"), self.course.name)
        self.assertEqual(data.get("description"), self.course.description)

    def test_create_lesson(self):
        """Тест создания урока."""

        url = reverse("materials:lessons_create")

        data = {
            "name": "Test_lesson",
            "description": "Test_lesson",
            "course": self.course.pk,
            "video_url": "https://youtube.com",
            "owner": self.user.pk
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        lesson_id = response.data['id']
        created_lesson = Lesson.objects.get(pk=lesson_id)
        self.assertEqual(created_lesson.name, 'Test_lesson')
        self.assertEqual(created_lesson.description, 'Test_lesson')
        self.assertEqual(created_lesson.owner, self.user)
        self.assertEqual(created_lesson.course, self.course)

    def test_update_lesson(self):
        """ Тест обновление урока. """

        updated_data = {
            'name': 'Updated_test_lesson',
            'description': 'Updated_test_description',
            'owner': self.user.id,
            'course': self.course.id,
        }

        url = reverse("materials:lessons_update", kwargs={"pk": self.lesson.pk})

        response = self.client.put(url, data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_lesson = Lesson.objects.get(id=self.lesson.id)

        self.assertEqual(updated_lesson.name, 'Updated_test_lesson')
        self.assertEqual(updated_lesson.description, 'Updated_test_description')

    def test_delete_lesson(self):
        url = reverse("materials:lessons_delete", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=self.lesson.id)
