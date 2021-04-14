from django.urls import path
from . import views


app_name = 'articles'
urlpatterns = [
    # read
    path('this_week/', views.this_week, name='this_week'),
    path('upcoming/', views.upcoming, name='upcoming'),
    path('history/', views.history, name='history'),

    # chapter related
    path('<int:subject_pk>/', views.chapter, name='chapter'),
    path('<int:subject_pk>/create_chapter/', views.create_chapter, name='create_chapter'),

    # article related
    path('<int:subject_pk>/<int:chapter_pk>/create/', views.create, name='create'),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    path('<int:article_pk>/update/', views.delete, name='delete'),
    path('<int:article_pk>/vote/', views.vote, name='vote'),
    path('<int:article_pk>/pin/', views.pin, name='pin'),
]
