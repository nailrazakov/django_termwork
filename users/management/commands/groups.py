from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        user_admin = User.objects.create(
            email='admin@test.test',
            first_name='Admin',
            last_name='Test',
        )
        user_admin.set_password('test')
        user_admin.is_staff = True
        user_admin.is_superuser = True
        user_admin.save()
        self.stdout.write(self.style.SUCCESS(f"Успешно создан пользователь с именем {user_admin.email}"))

        user_visitor = User.objects.create(
            email='visitor@test.test',
            first_name='Visitor',
            last_name='Test',
        )
        user_visitor.set_password('test')
        user_visitor.is_staff = False
        user_visitor.is_superuser = False
        user_visitor.save()
        self.stdout.write(self.style.SUCCESS(f"Успешно создан пользователь с именем {user_visitor.email}"))

        user_moderator = User.objects.create(
            email='moderator@test.test',
            first_name='Moderator',
            last_name='Test',
        )
        perm_blog_add = Permission.objects.get(codename='add_blog')
        perm_blog_change = Permission.objects.get(codename='change_blog')
        perm_blog_to_remove = Permission.objects.get(codename='delete_blog')
        moderator_blog_group = Group.objects.create(name='Контент-менеджер')
        moderator_blog_group.permissions.add(perm_blog_add, perm_blog_change, perm_blog_to_remove)
        moderator_blog_group.save()

        permission_to_remove = Permission.objects.get(codename='delete_product')
        permission_publicate = Permission.objects.get(codename='can_unpublish_product')
        moderator_group = Group.objects.create(name='Модератор продуктов')
        moderator_group.permissions.add(permission_to_remove, permission_publicate)
        moderator_group.save()

        user_moderator.set_password('test')
        user_moderator.is_staff = False
        user_moderator.is_superuser = False
        user_moderator.groups.add(moderator_group, moderator_blog_group)
        user_moderator.save()
        self.stdout.write(self.style.SUCCESS(f"Успешно создан пользователь с именем {user_moderator.email}\n"
                                             f"Успешно создана группа {moderator_group.name}\n"
                                             f"Успешно создана группа {moderator_blog_group.name}\n"
                                             f"{user_moderator.email} добавлен в группы {moderator_group.name}"
                                             f" и {moderator_blog_group.name}"))
