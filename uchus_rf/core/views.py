from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, ApplicationForm, ReviewForm
from .models import Application


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация успешна! Войдите в систему.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Неверный логин или пароль")
    return render(request, 'core/login.html')


@login_required
def dashboard_view(request):
    applications = request.user.applications.all().order_by('-created_at')

    if request.method == 'POST' and 'app_id' in request.POST:
        app = get_object_or_404(Application, id=request.POST['app_id'], user=request.user)
        if app.status != 'new':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.application = app
                review.save()
                messages.success(request, "Отзыв успешно сохранен!")
        else:
            messages.warning(request, "Отзыв можно оставить только после начала обучения.")
        return redirect('dashboard')

    return render(request, 'core/dashboard.html', {'applications': applications})


@login_required
def create_application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request, "Заявка отправлена на согласование.")
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'core/application_form.html', {'form': form})


def admin_login_view(request):
    if request.method == 'POST':
        if request.POST.get('username') == 'Admin26' and request.POST.get('password') == 'Demo20':
            request.session['is_admin'] = True
            return redirect('admin_panel')
        messages.error(request, "Неверные данные администратора")
    return render(request, 'core/login.html', {'is_admin_page': True})


def admin_panel_view(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    apps = Application.objects.all()

    status_filter = request.GET.get('status')
    if status_filter:
        apps = apps.filter(status=status_filter)

    sort = request.GET.get('sort', '-created_at')
    apps = apps.order_by(sort)

    paginator = Paginator(apps, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        new_status = request.POST.get('status')
        app = get_object_or_404(Application, id=app_id)
        app.status = new_status
        app.save()
        messages.success(request, f"Статус заявки #{app.id} изменен на {app.get_status_display()}")
        return redirect('admin_panel')

    return render(request, 'core/admin_panel.html',
                  {'page_obj': page_obj, 'status_filter': status_filter, 'sort': sort})