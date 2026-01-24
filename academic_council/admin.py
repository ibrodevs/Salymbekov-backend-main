from django.contrib import admin
from .models import AcademicCouncil
from unfold.admin import ModelAdmin

@admin.register(AcademicCouncil)
class AcademicCouncilAdmin(ModelAdmin):
    pass