from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.views import login_required
from django.views.decorators.http import require_POST, require_http_methods, require_safe

from .forms import ArticleForm, ChapterForm

from .models import Article, Chapter, Subject

from pprint import pprint
import random

max_vote = 2
index_images = [
    # 'https://images.unsplash.com/photo-1471180625745-944903837c22?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
    # 'https://images.unsplash.com/photo-1467106130188-af373dea5412?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=564&q=80',
    # 'https://images.unsplash.com/photo-1497278090167-1a9312e6e74c?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80',
    # 'https://images.unsplash.com/photo-1590421694065-7c56f3344c2f?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NzB8fHJlbGF4fGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    # 'https://images.unsplash.com/photo-1597822759274-7718de15a8b9?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80',
    # 'https://images.unsplash.com/photo-1599579519578-d14054a6b57f?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80',
    'https://images.unsplash.com/photo-1560172355-7aef0ac9eb6a?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=2732&q=80',
    # 'https://images.unsplash.com/photo-1583279697952-625317da8d00?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80',
    # 'https://images.unsplash.com/photo-1559613447-aa2ed3e6e6fa?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=704&q=80',
    # 'https://images.unsplash.com/photo-1584961630907-3fdb471c2848?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80',
]


def get_index_data():
    subjects = Subject.objects.all()
    index_datas = [{
        'subject': subject,
        'chapters': Chapter.objects.filter(subject=subject),
    } for subject in subjects]

    return {
        'index_datas': index_datas,
    }


def get_chapter_data(subject):
    chapters = Chapter.objects.filter(subject=subject)
    chapter_datas = [{
        'chapter': chapter,
        'articles': Article.objects.filter(chapter=chapter),
    } for chapter in chapters]

    return {
        'subject': subject,
        'chapter_datas': chapter_datas,
    }


@require_safe
def index(request):
    context = get_index_data()
    context.update({
        'image_path': random.choice(index_images),
    })
    return render(request, 'articles/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create_chapter(request, subject_pk):
    # 권한 체크
    if request.user.level < 3:
        context = get_index_data()
        context.update({
            'error': '챕터 작성 권한이 없습니다. 관리자에게 문의하세요.',
        })
        return render(request, 'articles/index.html', context)

    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.subject = get_object_or_404(Subject, pk=subject_pk)
            article.save()
            return redirect('index')
    else:
        form = ChapterForm()
    context = get_index_data()
    context.update({
        'form': form,
    })
    return render(request, 'articles/form.html', context)


@require_safe
def chapter(request, subject_pk):
    subject = get_object_or_404(Subject, pk=subject_pk)
    
    # context update
    context = get_index_data()
    context.update(get_chapter_data(subject))

    return render(request, 'articles/chapter.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request, subject_pk, chapter_pk):
    # 권한 체크
    if request.user.level < 2:
        context = get_index_data()
        context.update({
            'error': '문제 작성 권한이 없습니다. 관리자에게 문의하세요.',
        })
        return render(request, 'articles/index.html', context)

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.subject = get_object_or_404(Subject, pk=subject_pk)
            article.chapter = get_object_or_404(Chapter, pk=chapter_pk)
            article.save()
            return redirect('index')
    else:
        form = ArticleForm()
    context = get_index_data()
    context.update({
        'form': form,
    })
    return render(request, 'articles/form.html', context)


@login_required
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    chapter_pk = article.chapter.pk
    article.delete()
    return redirect('articles:chapter', f'#chapter-{chapter_pk}')


@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            chapter_pk = article.chapter.pk
            form.save()
            return redirect('articles:chapter', f'#chapter-{chapter_pk}')
    else:
        form = ArticleForm(instance=article)
    context = get_index_data()
    context.update({
        'form': form,
    })
    return render(request, 'articles/form.html', context)


@require_safe
def vote(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        
        # 권한 체크
        if request.user.level < 1:
            # context update
            context = get_index_data()
            context.update(get_chapter_data(article.subject))
            context.update({
                'error': '투표 권한이 없습니다. 관리자에게 문의하세요.',
            })
            return render(request, 'articles/chapter.html', context)

        # 투표 취소
        if article.voter.filter(pk=request.user.pk).exists():
            article.voter.remove(request.user)

        # 투표 추가
        else:
            if request.user.voting_articles.filter(chapter=article.chapter, is_select=False).count() < max_vote:
                article.voter.add(request.user)
            else:
                # context update
                context = get_index_data()
                context.update(get_chapter_data(article.subject))
                context.update({
                    'error': f'최대 {max_vote}개까지만 투표할 수 있습니다.',
                })
                return render(request, 'articles/chapter.html', context)
        return redirect('articles:chapter', article.subject.pk)
    else:
        return redirect('accounts:login')


def this_week(request):
    articles = Article.objects.filter(this_week=True)
    context = get_index_data()
    context.update({
        'articles': articles,
    })
    return render(request, 'articles/article_list.html', context)


def upcoming(request):
    articles = Article.objects.filter(upcoming=True)
    context = get_index_data()
    context.update({
        'articles': articles,
    })
    return render(request, 'construction.html', context)


def history(request):
    articles = Article.objects.filter(history=True)
    context = get_index_data()
    context.update({
        'articles': articles,
    })
    return render(request, 'construction.html', context)
