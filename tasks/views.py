from django.shortcuts import render, redirect, get_object_or_404

from .models import Task
from .forms import TaskForm


# Home page: Display all tasks
def home(request):

    tasks = Task.objects.all().order_by('-created_at')

    context = {
        'tasks': tasks,
    }

    return render(request, 'tasks/task_list.html', context)


# Add a new task
def add_task(request):

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = TaskForm()

    context = {
        'form': form,
    }

    return render(request, 'tasks/add_task.html', context)



# Edit an existing task
def edit_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = TaskForm(instance=task)

    context = {
        'form': form,
        'page_title': 'Edit Task',
    }

    return render(request, 'tasks/task_form.html', context)


# Mark a task as completed or pending
def toggle_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.completed = not task.completed
        task.save(update_fields=['completed'])

    return redirect('home')


# Delete a task
def delete_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()

    return redirect('home')
