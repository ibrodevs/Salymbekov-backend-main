from django import forms
from django.contrib import admin
from .models import DevelopmentCouncilMember, ScientificTechnicalCouncilMember

LANGUAGE_CHOICES = [
    ('ru', 'Русский'),
    ('en', 'English'),
    ('kg', 'Кыргызча'),
]


class DevelopmentCouncilForm(forms.ModelForm):
    current_language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        label="Язык для заполнения",
        initial='ru'
    )

    class Meta:
        model = DevelopmentCouncilMember
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        lang = cleaned_data.get('current_language', 'ru')

        full_name = cleaned_data.get(f'full_name_{lang}')
        role = cleaned_data.get(f'role_{lang}')

        if not full_name:
            self.add_error(f'full_name_{lang}', f'Поле ФИО ({lang}) обязательно для заполнения!')
        if not role:
            self.add_error(f'role_{lang}', f'Поле Должность ({lang}) обязательно для заполнения!')

        return cleaned_data

@admin.register(DevelopmentCouncilMember)
class DevelopmentCouncilAdmin(admin.ModelAdmin):
    form = DevelopmentCouncilForm
    list_display = ('full_name_ru', 'is_council_member', 'is_active', 'order')
    list_filter = ('is_active', 'is_council_member')
    ordering = ('order',)



class ScientificTechnicalCouncilForm(forms.ModelForm):
    current_language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        label="Язык для заполнения",
        initial='ru'
    )

    class Meta:
        model = ScientificTechnicalCouncilMember
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        lang = cleaned_data.get('current_language', 'ru')

        full_name = cleaned_data.get(f'full_name_{lang}')
        role = cleaned_data.get(f'role_{lang}')

        if not full_name:
            self.add_error(f'full_name_{lang}', f'Поле ФИО ({lang}) обязательно для заполнения!')
        if not role:
            self.add_error(f'role_{lang}', f'Поле Должность ({lang}) обязательно для заполнения!')

        return cleaned_data

@admin.register(ScientificTechnicalCouncilMember)
class ScientificTechnicalCouncilAdmin(admin.ModelAdmin):
    form = ScientificTechnicalCouncilForm
    list_display = ('full_name_ru', 'is_head', 'is_active', 'order')
    list_filter = ('is_head', 'is_active')
    ordering = ('order',)
