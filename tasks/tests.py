from datetime import timedelta

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Task


@override_settings(ALLOWED_HOSTS=['testserver'])
class TaskListViewTests(TestCase):
    def test_upcoming_count_includes_tasks_beyond_preview_limit(self):
        due_date = timezone.localdate() + timedelta(days=1)
        Task.objects.bulk_create([
            Task(title=f'Task {index}', due_date=due_date)
            for index in range(7)
        ])

        response = self.client.get(reverse('task_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['upcoming_count'], 7)
        self.assertEqual(len(response.context['upcoming_tasks']), 5)
