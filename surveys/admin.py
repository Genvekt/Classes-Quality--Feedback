from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CourseAndGroup, Professor
from .models import Courses

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Courses)
admin.site.register(Professor)