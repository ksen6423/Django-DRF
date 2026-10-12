from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, CourseSubscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        """ Создание тестового пользователя для авторизации. """

        self.moderator = User.objects.create(
            email='moderator@email.com',
            is_staff=True
        )
        self.moderator.set_password('password123')
        self.moderator.save()

        self.owner = User.objects.create(
            email='owner@email.com',
            is_staff=True
        )
        self.owner.set_password('password123')
        self.owner.save()

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
        self.subscribe_url = reverse('materials:subscription')
        self.lesson_detail_url = reverse('materials:lessons_retrieve', kwargs={'pk': self.lesson.pk})

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

    def test_get_lesson_success(self):
        """
        Тест на успешное получение урока.
        Отправляет GET-запрос на эндпоинт урока и проверяет, что статус-код ответа равен 200.
        """
        course = Course.objects.create(name="Test_Lesson_3", description="Описание курса")

        lesson = Lesson.objects.create(
            name="Test_Lesson_3",
            description="Тестовый урок",
            course=course,
            owner=self.user
        )

        lesson_id = lesson.pk
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_retrieve", kwargs={'pk': lesson_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        lesson_data = response.json()
        self.assertEqual(lesson_data['id'], lesson_id)
        self.assertEqual(lesson_data['name'], self.lesson.name)

    def test_get_lesson_not_found(self):
        """
        Тест на получение несуществующего урока.
        """
        lesson_id = 999  # Несуществующий ID
        url = reverse('materials:lessons_retrieve', kwargs={'pk': lesson_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_add_subscription_success(self):
        """
        Тест на успешное добавление подписки.
        Отправляет POST-запрос для подписки на другого пользователя.
        """
        self.client.force_login(self.user)

        data = {
            'target_user_id': self.user.id,
            "course_id": self.course.id
        }

        response = self.client.post(self.subscribe_url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Подписка добавлена"})

        self.assertTrue(
            CourseSubscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

        self.assertIn('Подписка добавлена', response.json().get('message', ''))

    def test_repeat_subscription_handling(self):

        self.client.force_authenticate(user=self.user)

        data = {
            "course_id": self.course.id
        }

        self.client.post(self.subscribe_url, data)

        response = self.client.post(self.subscribe_url, data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {"message": "Подписка удалена"})

    def test_unauthorized_lesson_access(self):
        """
        Тестирует доступ к защищенному ресурсу (уроку) без аутентификации.
        """

        self.client.logout()

        response = self.client.get(self.lesson_detail_url)

        self.assertIn(response.status_code, [401, 403])

        response_data = response.json()
        self.assertIn('detail', response_data)
        self.assertEqual(response_data['detail'], 'Authentication credentials were not provided.')

    def test_owner_permissions(self):
        """
        Проверяет, что владелец имеет полный доступ.
        """
        self.client.force_authenticate(user=self.owner)

    def test_moderator_permissions(self):
        """
        Проверяет, что модератор имеет ограниченные права (например, модерация).
        """
        self.client.force_authenticate(user=self.moderator)

    def test_regular_user_permissions(self):
        """
        Проверяет, что обычный пользователь имеет ограниченный доступ.
        """
        self.client.force_authenticate(user=self.user)
