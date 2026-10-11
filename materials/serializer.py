from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, CourseSubscription
from materials.validators import validate_no_external_links


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    video_url = serializers.URLField(validators=[validate_no_external_links], required=False, allow_blank=True)

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "course", "video_url"]


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "description", "lessons", "lesson_count"]

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CourseSubscription
        fields = ['user_subscription', 'course_subscription', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        course = obj.course_subscription
        return CourseSubscription.objects.filter(user_subscription=user, course_subscription=course).exists()
