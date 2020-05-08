from django.contrib import admin
from .models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated', 'views', 'likes')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
