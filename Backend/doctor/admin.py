from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Speciality)


class TimeRangeInline(admin.TabularInline):
    model = TimeRange
    extra = 0
    min_num = 1
    verbose_name = "Time Range"
    verbose_name_plural = "Time Ranges"


class DayScheduleInline(admin.TabularInline):
    model = DaySchedule
    extra = 0
    show_change_link = True
    fields = ("day", "available")
    readonly_fields = ()
    inlines = [TimeRangeInline]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    inlines = [DayScheduleInline]


@admin.register(DaySchedule)
class DayScheduleTime(admin.ModelAdmin):
    list_display = ("doctor", "day", "available")
    list_filter = ("doctor", "day", "available")
    inlines = [TimeRangeInline]
