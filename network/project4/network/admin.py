from django.contrib import admin
from .models import Posts, Following, Followers, Likes
# Register your models here.

admin.site.register(Posts),
admin.site.register(Following),
admin.site.register(Followers),
admin.site.register(Likes)

