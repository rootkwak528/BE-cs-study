from django.db import models
from django.conf import settings


class Subject(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    title = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'


class Article(models.Model):
    # foreign keys
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='my_articles')
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voting_articles')
    pinner = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='pinned_articles')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    # limit_choices_to = Chapter.objects.filter(subject=subject)
    # print(Chapter.objects.filter(subject=subject))
    # limit_choices_to = {'subject': True}
    # chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, limit_choices_to=limit_choices_to)

    # normal keys
    title = models.CharField(max_length=150)
    is_select = models.BooleanField(default=False)
    this_week = models.BooleanField(default=False) # 이번주 문제인가
    upcoming = models.BooleanField(default=False)  # 다음주 문제 후보인가
    history = models.BooleanField(default=False)   # 이전에 뽑혔던 문제인가
    select_week = models.CharField(max_length=20, blank=True)  # 언제 뽑혔는가
    answer = models.TextField(blank=True)  # 답안들
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # to be update
    # - markdown
    # https://github.com/agusmakmun/django-markdown-editor
    # https://github.com/agusmakmun/django-markdown-editor/wiki

    def __str__(self):
        return f'{self.subject} / {self.chapter} / {self.title}'
