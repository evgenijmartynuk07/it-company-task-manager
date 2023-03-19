from django.urls import path

from task_manager.views import index, TaskCreateView, TaskUpdateView, TaskDetailView, TaskDeleteView, WorkerCreateView, \
    WorkerListView, TaskListView

urlpatterns = [
    path("", index, name="index"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]

app_name = "task_manager"
