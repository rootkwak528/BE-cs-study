from django import forms
from .models import Article, Chapter


class ArticleForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ('title', )


class ChapterForm(forms.ModelForm):
    
    class Meta:
        model = Chapter
        fields = ('title', )
