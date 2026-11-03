from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q


# READ: Display all tasks
def task_list(request):
    all_tasks = Task.objects.all().order_by('-created_at')

    # Get search and filter values from the URL
    search_query = request.GET.get('q', '')
    selected_status = request.GET.get('status', '')

    # Search tasks by title or description
    tasks = all_tasks

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filter tasks by status
    if selected_status:
        tasks = tasks.filter(status=selected_status)

    # Calculate dashboard statistics
    total_count = all_tasks.count()
    pending_count = all_tasks.filter(status='pending').count()
    progress_count = all_tasks.filter(status='in_progress').count()
    completed_count = all_tasks.filter(status='completed').count()

    # Calculate completion percentage
    completion_rate = 0

    if total_count > 0:
        completion_rate = round((completed_count / total_count) * 100)

    # Identify overdue tasks
    today = timezone.localdate()

    overdue_tasks = all_tasks.filter(
        due_date__lt=today
    ).exclude(status='completed')

    # Identify tasks due within the next seven days
    next_week = today + timedelta(days=7)

    upcoming_tasks = all_tasks.filter(
        due_date__gte=today,
        due_date__lte=next_week
    ).exclude(status='completed').order_by('due_date')
    upcoming_count = upcoming_tasks.count()
    upcoming_tasks = upcoming_tasks[:5]

    context = {
        'tasks': tasks,
        'total_count': total_count,
        'pending_count': pending_count,
        'progress_count': progress_count,
        'completed_count': completed_count,
        'completion_rate': completion_rate,
        'overdue_count': overdue_tasks.count(),
        'overdue_tasks': overdue_tasks.order_by('due_date')[:5],
        'upcoming_tasks': upcoming_tasks,
        'upcoming_count': upcoming_count,
        'search_query': search_query,
        'selected_status': selected_status,
    }

    return render(request, 'tasks/task_list.html', context)


# CREATE: Add a new task
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('task_list')

    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'page_title': 'Add New Task'
    })


# UPDATE: Edit an existing task
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('task_list')

    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'page_title': 'Edit Task'
    })


# DELETE: Remove a task
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {
        'task': task
    })

# VIEW: Display the full details of a task
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    return render(request, 'tasks/task_detail.html', {
        'task': task
    })


# QUICK UPDATE: Change a task's status
def task_status_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        valid_statuses = [
            'pending',
            'in_progress',
            'completed'
        ]

        if new_status in valid_statuses:
            task.status = new_status
            task.save()

    return redirect('task_list')