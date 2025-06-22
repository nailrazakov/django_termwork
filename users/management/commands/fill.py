from django.core.management import BaseCommand
import json
from users.models import User, Payments
from models.models import Course, Lesson


class Command(BaseCommand):
    @staticmethod
    def from_file(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def handle(self, *args, **options):
        """Запись чистой базы данных"""
        # Удалите все платежи
        Payments.objects.all().delete()
        # Удалите все уроки
        Lesson.objects.all().delete()
        # Удалите все курсы
        Course.objects.all().delete()
        # Удалите пользователей
        User.objects.all().delete()

        data = self.from_file("db_fill.json")
        payments_list = []
        lesson_list = []
        course_list = []
        user_list = []
        user_dict = {}
        course_dict = {}
        lesson_dict = {}

        for item in data:
            if item['model'] == 'users.user':
                fields = item["fields"]
                fields.pop('groups') # с этим полем TypeError: Direct assignment to the forward side of a many-to-many set is prohibited.
                fields.pop('user_permissions') # с этим полем TypeError: Direct assignment to the forward side of a many-to-many set is prohibited. Use user_permissions.set() instead.
                object_user = User(pk=item['pk'], **fields)
                user_list.append(object_user)
                user_dict[item['pk']] = object_user
            elif item['model'] == 'models.course':
                object_course = Course(pk=item['pk'], **item["fields"])
                course_list.append(object_course)
                course_dict[item['pk']] = object_course
        for item in data:
            if item['model'] == 'models.lesson':
                fields = item["fields"]
                key_course = fields.pop("course")
                object_lesson = Lesson(pk=item['pk'], course=course_dict[key_course], **fields)
                lesson_list.append(object_lesson)
                lesson_dict[item['pk']] = object_lesson
        for item in data:
            if item['model'] == 'users.payments':
                fields = item["fields"]
                key_course = fields.pop("course")
                if key_course is None:
                    course = None
                else:
                    course = course_dict[key_course]
                key_lesson = fields.pop("lesson")
                if key_lesson is None:
                    lesson = None
                else:
                    lesson = lesson_dict[key_lesson]
                key_user = fields.pop("user")
                object_payments = Payments(course=course, lesson=lesson,
                                           user=user_dict[key_user], **fields)
                payments_list.append(object_payments)
        User.objects.bulk_create(user_list)
        Course.objects.bulk_create(course_list)
        Lesson.objects.bulk_create(lesson_list)
        Payments.objects.bulk_create(payments_list)
