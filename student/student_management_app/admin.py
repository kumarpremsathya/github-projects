from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

# from student_management_app.models import CustomUser
from student_management_app.models import *

class UserModel(UserAdmin):
    list_display = [field.name for field in CustomUser._meta.fields]
    pass

admin.site.register(CustomUser,UserModel)
# admin.site.register(AdminHOD)
# admin.site.register(Staffs)
# admin.site.register(Courses)
# admin.site.register(Subjects)
# admin.site.register(Students)
# admin.site.register(Attendance)



# Define a function to dynamically get all field names of a model
def get_all_field_names(model):
    field_names = [field.name for field in model._meta.fields]
    if 'course_id' in field_names:
        try:
            # Try to replace 'course_id' with 'course_name'
            field_names[field_names.index('course_id')] = 'get_course_name'
        except ValueError:
            # If 'course_id' is present but 'course_name' is not, just return the original field names
            pass
    return field_names

# Register CustomUser model
# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'user_type')
#     list_filter = ('user_type',)

# Register AdminHOD model
@admin.register(AdminHOD)
class AdminHODAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(AdminHOD)

# Register Staffs model
@admin.register(Staffs)
class StaffsAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Staffs)

# Register Courses model
@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Courses)

# Register Subjects model
@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Subjects)

    def get_course_name(self, obj):
        return obj.course_id.course_name
    get_course_name.short_description = 'Course Name'

# Register Students model
@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Students)

    def get_course_name(self, obj):
        return obj.course_id.course_name
    get_course_name.short_description = 'Course Name'

# Register Attendance model
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Attendance)