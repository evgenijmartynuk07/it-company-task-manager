import datetime
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.core.paginator import Paginator

from task_manager.forms import WorkerCreateForm, TaskCreateForm, TaskCompletedUpdateForm, WorkerUpdateForm
from task_manager.models import Task


@login_required
def index(request):
    tasks = Task.objects.prefetch_related(
        "assignees"
    ).select_related(
        "owner"
    ).select_related(
        "task_type"
    ).filter(
        assignees=request.user.id
    )

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    paginator = Paginator(tasks, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "num_visits": num_visits + 1,
        "paginator": paginator,
        "page_obj": page_obj,
    }

    return render(request, "task_manager/index.html", context=context)


class WorkerCreateView(generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreateForm
    success_url = reverse_lazy("task_manager:index")


class WorkerUpdateView(generic.CreateView):
    model = get_user_model()
    form_class = WorkerUpdateForm
    # success_url = reverse_lazy("task_manager:index")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    queryset = get_user_model().objects.prefetch_related(
        "tasks"
    ).select_related(
        "position"
    )
    paginate_by = 5


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.prefetch_related("tasks").select_related("position")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("task_manager:index")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees").select_related("owner")
    paginate_by = 4


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ("name", "description", "deadline", "priority", "task_type", "assignees")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:index")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees").select_related("task_type")
    form_class = TaskCompletedUpdateForm

    def get_context_data(self, **kwargs):
        self.task = Task.objects.get(id=self.object.pk)
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()

        if self.task.deadline < datetime.date.today():
            context["valid_data"] = False
        else:
            context["valid_data"] = True
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        form = TaskCompletedUpdateForm(request.POST)

        if request.POST.get("is_completed") == "1":
            self.task.is_completed = True
            self.task.save()

        if request.POST.get("assignees") == f"{self.request.user.id}":
            self.task.assignees.add(self.request.user.id)
            self.task.save()

        return redirect("task_manager:task-detail", pk=self.object.pk)
