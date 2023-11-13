from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.generics import get_object_or_404
from django.urls import reverse_lazy
from .forms import TodoForm
from .models import Todo


class UserListView(ListView):
    model = User
    template_name = 'user/users.html'
    context_object_name = 'users'


@login_required
def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('/')
    else:
        form = TodoForm()
    return render(request, 'todo/todo-form.html', {"form": form})


def todo_list(request):
    # Assuming Todo.objects is a manager
    todos = Todo.objects.all()
    return render(request, 'todo/todo-list.html', {'todos': todos})


class TodoListView(ListView):
    template_name = 'todo/this-user.html'
    context_object_name = 'clay'

    def get_queryset(self):
        try:
            fk = self.kwargs['fk']
            queryset = Todo.objects.filter(user=fk)
        except:
            queryset = Todo.objects.all()
        return queryset


class TodoUpdateView(UpdateView):
    model = Todo
    template_name = 'todo/todo_update.html'
    fields = ['title', 'description', 'start_time', 'end_time', 'bio', 'status']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo.user != self.request.user:
            return render(request, 'todo/update_denied.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('this-user', kwargs={'fk': self.object.pk})


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todo/delete_todo.html'

    def get_success_url(self):
        return reverse_lazy('this-user', kwargs={'fk': self.object.pk})
