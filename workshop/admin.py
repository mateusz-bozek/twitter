from django.contrib import admin

from workshop.models import Tweet, Message, Comment

# Register your models here.
admin.site.register(Tweet)
admin.site.register(Message)
admin.site.register(Comment)