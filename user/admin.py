from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import QuerySet

from user.models import Subscriber


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_followed_users')

    def get_queryset(self, request):
        qs: QuerySet = super().get_queryset(request)
        return qs.prefetch_related('followed_users')

    def get_followed_users(self, instance):
        return '\n'.join([user.username for user in instance.followed_users.all()])


# admin.site.unregister(Subscriber)
admin.site.register(Subscriber, SubscriberAdmin)
