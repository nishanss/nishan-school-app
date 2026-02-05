from django.contrib import admin
from .models import Grade, Section

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'capacity')
    list_filter = ('grade',)