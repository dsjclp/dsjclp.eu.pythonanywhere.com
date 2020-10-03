
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic

from quote.forms import (
    ScheduleModelForm,
    StepFormset
)
from quote.models import Schedule, Step
from django.http import JsonResponse

def create_quote(request):
    template_name = 'quote/create_quote.html'
    if request.method == 'GET':
        scheduleform = ScheduleModelForm(request.GET or None)
        formset = StepFormset(queryset=Step.objects.none())
    elif request.method == 'POST':
        scheduleform = ScheduleModelForm(request.POST)
        formset = StepFormset(request.POST)
        if scheduleform.is_valid() and formset.is_valid():
            schedule = scheduleform.save(commit=False)
            schedule.user=request.user
            schedule = scheduleform.save()
            i=1
            for form in formset:
                step = form.save(commit=False)
                step.schedule = schedule
                step.rank = i
                step.save()
                i=i+1
            return redirect('home')
    return render(request, template_name, {
        'scheduleform': scheduleform,
        'formset': formset,
    })