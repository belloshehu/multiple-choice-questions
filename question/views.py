from django.shortcuts import render, reverse
from django.views.generic import (
    TemplateView,
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import IndividualQuestion, InstitutionQuestion
from .forms import IndividualQuestionForm, InstitutionQuestionForm
from cbt.models import PersonalCBT
from cbt.views import IndividualAssessmentDetailView


# ====================
# Individual Questions Views for CRUD operation and ListView.
# ====================


class IndividualQuestionCreateView(LoginRequiredMixin, CreateView):
    ''' View to create Question   '''
    model = IndividualQuestion
    form_class =IndividualQuestionForm
    template_name = 'question/question_form.html'

    def get_success_url(self, **kwargs):
        return reverse(
            'cbt:individual-assessment-detail',
            kwargs={'pk':self.get_assessment_object().id}
        )

    def get_assessment_object(self):
        ''' Returns the assessment object whose questions are created.'''
        assessment_object_id = self.kwargs.get('pk')
        assessment_object = get_object_or_404(
            PersonalCBT,
            id=assessment_object_id
        )
        return assessment_object

    def form_valid(self, form):
        form.instance.assessment = self.get_assessment_object()
        return super().form_valid(form)

    def get_context_data(self, *args,**kwargs ):
        '''Add assessment to the context. '''
        context = super().get_context_data(*args, **kwargs)
        context['assessment'] = self.get_assessment_object()
        return context

class IndividualQuestionListView(LoginRequiredMixin, ListView):
    model = IndividualQuestion
    template_name = 'question/question_list.html'
    context_object_name = 'questions'


class IndividualQuestionDetailView(LoginRequiredMixin, DetailView):
    model = IndividualQuestion
    template_name = 'question/question_detail.html'


class IndividualQuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = IndividualQuestion
    form_class = IndividualQuestionForm
    template_name = 'question/question_update_form.html'
    context_object_name = 'question'

    def get_success_url(self, **kwargs):
        return reverse(
            'cbt:individual-assessment-detail',
            kwargs={'pk':self.get_object().assessment.id}
        )

class IndividualQuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = IndividualQuestion
    template_name = 'question/question_delete_confirm.html'
    context_object_name = 'question'

    def get_success_url(self):
        return reverse(
            'cbt:individual-assessment-detail',
            kwargs={'pk':self.get_object().assessment.id}
        )