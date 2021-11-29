from django.contrib import admin

from reducer.models import Domain, Users, URLs


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'domain',
                    )


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_uuid',
                    'is_banned',
                    'last_visited'
                    )


@admin.register(URLs)
class URLSAdmin(admin.ModelAdmin):
    list_display = ('user_uuid',
                    'domain',
                    'url',
                    'url_destination',
                    'created'
                    )
