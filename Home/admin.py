from django.contrib import admin
# imports admin method
from .models import UserInformation, Posts, Comment
# imports all of the tables i want the admin to have access to


class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'year', 'interest', 'postcode', 'town')
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    list_filter = ['year', 'interest', 'postcode', 'town']


class PostsAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'publish')
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'title', 'content']
    list_filter = ['publish']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'publish')
    search_fields = ['post__title', 'post__content', 'user__username', 'user__first_name', 'user__last_name', 'user__email', 'content']
    list_filter = ['publish']

# above lines specify which fields to display in django admin
# and what the search field is specifically searching in and filters when displaying the records

admin.site.register(UserInformation, UserInformationAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Comment, CommentAdmin)
# registers specified database tables on the admin site for the admin to interact with
