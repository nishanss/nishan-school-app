from django.contrib import admin
from .models import TimeSlot, TimetableEntry

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'is_break')

@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ('day', 'time_slot', 'section', 'subject', 'teacher')
    list_filter = ('day', 'section', 'teacher')