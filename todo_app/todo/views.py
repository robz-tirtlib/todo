from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView,
                                       FormView)
from django.views.generic.base import RedirectView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.shortcuts import redirect

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.models import User

from .models import Todo

from .forms import UserUpdateForm


class RegisterView(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todos')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todos')
        return super().get(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse('todos')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = UserUpdateForm
    template_name = 'todo/user_update.html'
    success_url = reverse_lazy('todos')

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        form = UserUpdateForm(self.request.POST, instance=user)
        if form.is_valid():
            form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserUpdateForm(instance=self.request.user)
        return context

    def test_func(self):
        user = User.objects.get(username=self.request.user)
        return user.username == self.kwargs['username']


class HomeView(RedirectView):
    url = 'todos'


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/todos.html'
    context_object_name = 'todos'
    ordering = ['complete', '-date_added']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos'] = context['todos'].filter(user=self.request.user)
        context['count'] = context['todos'].filter(complete=False)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['todos'] = context['todos'].filter(
                title__icontains=search_input)
        context['search_input'] = search_input
        return context


class TodoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Todo
    fields = ['title', 'body', 'complete']
    template_name = 'todo/todos_update.html'
    pk_url_kwarg = 'todo_pk'
    success_url = reverse_lazy('todos')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        todo = Todo.objects.get(pk=self.kwargs['todo_pk'])
        return todo.user == self.request.user


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'body']
    template_name = 'todo/todos_create.html'
    success_url = reverse_lazy('todos')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy('todos')
    template_name = 'todo/todos_delete_confirm.html'
    pk_url_kwarg = 'todo_pk'

    def test_func(self):
        todo = Todo.objects.get(pk=self.kwargs['todo_pk'])
        return todo.user == self.request.user
