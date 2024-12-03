# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import View
from datetime import timedelta
import tweepy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import AuthenticationForm

from .forms import LoginForm, CustomUserCreationForm, UserProfileForm, TaskForm
from .models import Task, StudySession

from datetime import datetime

def my_other_view(request):
    # セッションから文字列として保存した日時を取得
    date_string = request.session.get('last_accessed')

    if date_string:
        # 文字列をdatetimeオブジェクトに変換
        last_accessed = datetime.fromisoformat(date_string)
        # 必要な処理
    else:
        # 'last_accessed'がセッションにない場合の処理
        pass

    # datetimeオブジェクトを文字列に変換して保存
    request.session['last_accessed'] = datetime.now().isoformat()

    return render(request, 'template_name.html')
# 不要なaxes関連のインポートを削除
# from axes.utils import get_failure_limit, get_client_username, get_client_ip_address
# from axes.attempts import get_user_attempts
# from axes.utils import reset

# ログイン試行回数とロックアウト時間を定数として定義
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_TIME = 30  # 秒単位

# 新規登録ビュー
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('登録が完了しました！'))  # メッセージを国際化
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# ログインビュー
def login_view(request):
    # セッションから試行回数を取得または初期化
    login_attempts = request.session.get('login_attempts', 0)
    lockout_until = request.session.get('lockout_until')

    # ロックアウト中かどうかを確認
    if lockout_until and timezone.now() < lockout_until:
        # ロックアウト画面を表示
        return render(request, 'accounts/lockout.html')

    # フォームオブジェクトの初期化
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # ユーザーの認証を行う
            user = form.get_user()
            if user is not None:
                # 認証に成功した場合、ログインしてセッションをリセット
                login(request, user)
                request.session['login_attempts'] = 0
                return redirect('home')  # ホームページへのリダイレクト
        else:
            # 認証に失敗した場合、試行回数を増やす
            login_attempts += 1
            request.session['login_attempts'] = login_attempts

            if login_attempts >= MAX_LOGIN_ATTEMPTS:
                # ロックアウトタイムを設定し、ロックアウト画面にリダイレクト
                request.session['lockout_until'] = timezone.now() + timedelta(seconds=LOCKOUT_TIME)
                return render(request, 'accounts/lockout.html')

    # 残りの試行回数を表示するための変数
    remaining_attempts = MAX_LOGIN_ATTEMPTS - login_attempts
    return render(request, 'accounts/login.html', {
        'form': form,
        'remaining_attempts': remaining_attempts,
    })

# ログアウトビュー
def logout_view(request):
    logout(request)
    messages.info(request, "操作がないためログアウトしました")
    return redirect("login")

# ホームビュー
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("ログインが必要です。"))
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.success(request, _("ホームページへようこそ！"))
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context

# タスクの一覧表示
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'accounts/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

# タスクの新規作成
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'accounts/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# タスクの詳細表示
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'accounts/task_detail.html'
    context_object_name = 'task'

# タスクの編集
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'accounts/task_form.html'
    success_url = reverse_lazy('task_list')

# タスクの削除
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'accounts/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

def get_twitter_api():
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET_KEY,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)
    return api

def fetch_and_calculate_time(user):
    api = get_twitter_api()
    tasks = Task.objects.filter(user=user)
    for task in tasks:
        tweets = api.user_timeline(screen_name=user.twitter_username, count=100)
        start_time = None
        for tweet in tweets:
            if task.start_tag in tweet.text:
                start_time = tweet.created_at
            elif task.end_tag in tweet.text and start_time:
                end_time = tweet.created_at
                duration = (end_time - start_time).total_seconds() / 3600
                StudySession.objects.create(
                    task=task,
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration
                )
                post_automatic_tweet(api, user, task, duration)
                start_time = None

def post_automatic_tweet(api, user, task, duration):
    if task.target_hours:
        total_duration = sum(session.duration for session in task.sessions.all())
        remaining_hours = task.target_hours - total_duration
        message = f"本日 {task.title} {duration:.2f}時間 達成！\n目標時間まで あと {remaining_hours:.2f}時間"
    elif task.target_date:
        remaining_days = (task.target_date - timezone.now().date()).days
        message = f"本日 {task.title} {duration:.2f}時間 達成！\n目標日まで あと {remaining_days}日"
    else:
        message = f"本日 {task.title} {duration:.2f}時間 達成！"

    if duration >= 2:
        message += "\n順調！！"
    elif duration >= 1:
        message += "\nこのままでは、、、"
    else:
        message += "\n負け犬め"

    api.update_status(status=message)

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールが更新されました')
            return redirect('home')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})
