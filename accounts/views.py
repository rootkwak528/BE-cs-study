from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator

from django.contrib.auth.views import login_required
from django.views.decorators.http import require_POST, require_http_methods, require_safe

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserChangeForm, CustomUserCreationForm

from .models import User

from articles.views import get_index_data


@require_http_methods(['GET', 'POST'])
def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect('index')
        else:
            form = AuthenticationForm()
            
        context = get_index_data()
        context.update({
            'form': form,
        })
        return render(request, 'accounts/form.html', context)
    else:
        return redirect('index')


@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')


@require_http_methods(['GET', 'POST'])
def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('index')
        else:
            form = CustomUserCreationForm()

        context = get_index_data()
        context.update({
            'form': form,
        })
        return render(request, 'accounts/form.html', context)
    else:
        return redirect('index')


@require_POST
def unregister(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.pk)
        auth_logout(request)
        user.delete()
    return redirect('index')


@login_required
@require_http_methods(['GET', 'POST'])
def edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    context = get_index_data()
    context.update({
        'form': form,
    })
    return render(request, 'accounts/form.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
    
    context = get_index_data()
    context.update({
        'form': form,
    })
    return render(request, 'accounts/form.html', context)


@require_safe
def profile(request, username):
    user = get_object_or_404(User, username=username)
    
    # pagination - my_articles
    my_articles = user.my_articles.all()
    paginator_my = Paginator(my_articles, 5)
    page_number_my = request.GET.get('page_my')
    page_obj_my = paginator_my.get_page(page_number_my)

    # pagination - pinned_articles
    pinned_articles = user.pinned_articles.all()
    paginator_pin = Paginator(pinned_articles, 5)
    page_number_pin = request.GET.get('page_pin')
    page_obj_pin = paginator_pin.get_page(page_number_pin)

    context = get_index_data()
    context.update({
        'user': user,
        'page_obj_my': page_obj_my,
        'page_obj_pin': page_obj_pin,
    })
    return render(request, 'accounts/profile.html', context)
