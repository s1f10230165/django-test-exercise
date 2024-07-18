from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from .models import Task
from .forms import TaskForm

def index(request):
    if request.method == 'POST':
        task = Task(
            title=request.POST['title'],
            due_at=make_aware(parse_datetime(request.POST['due_at'])),
            priority=request.POST['priority']
        )
        task.save()
        return redirect('/')  # リダイレクトを追加

    order = request.GET.get('order', 'post')
    if order == 'due':
        tasks = Task.objects.order_by('due_at')
    elif order == 'priority_asc':
        tasks = Task.objects.order_by('priority')
    elif order == 'priority_desc':
        tasks = Task.objects.order_by('-priority')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks': tasks,
        'form': TaskForm()
    }
    return render(request, 'todo/index.html', context)

def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)

def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect(index)

def close(request, task_id):
    try: 
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(index)

def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    
    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect(detail, task_id)

    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)

def todo_list(request):
    sort_by = request.GET.get('sort_by', 'priority')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = '-' + sort_by
    tasks = Task.objects.all().order_by(sort_by)
    return render(request, 'todo/todo_list.html', {'tasks': tasks})

def todo_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TaskForm()
    return render(request, 'todo/todo_form.html', {'form': form})

def todo_update(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/todo_form.html', {'form': form})
