from django.shortcuts import render, reverse
from django.views.generic import (
    TemplateView,
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import (IndividualQuestion,
    InstitutionQuestion,
    IndividualQuestionPassage
)
from .forms import (
    IndividualQuestionForm,
    InstitutionQuestionForm,
    IndividualQuestionPassageForm
    )
from cbt.models import IndividualAssessment
from cbt.views import IndividualAssessmentDetailView


# ====================
# Individual Questions Views for CRUD operation and ListView.
# ====================


class IndividualQuestionFromPassageCreateView(LoginRequiredMixin, CreateView):
    ''' View to create Question with a Passage. '''
    model = IndividualQuestion
    form_class = IndividualQuestionForm
    template_name = 'question/question_form.html'

    def get_success_url(self, **kwargs):
        return reverse(
            'cbt:individual-assessment-detail',
            kwargs={'pk':self.get_passage_object().assessment.id}
        )
    def get_passage_object(self):
        ''' Returns the Passage object whose questions are created.'''
        return get_object_or_404(
            IndividualQuestionPassage,
            id=self.kwargs.get('pk')
        )

    def form_valid(self, form):
        form.instance.passage = self.get_passage_object()
        form.instance.assessment = self.get_passage_object().assessment
        return super().form_valid(form)

    def get_context_data(self, *args,**kwargs ):
        '''Add Passage to the context. '''
        context = super().get_context_data(*args, **kwargs)
        context['passage'] = self.get_passage_object()
        context['action_url'] = reverse_lazy(
            'question:individual-question-from-passage-create',
            kwargs={'pk':self.get_passage_object().id}
        )
        return context

class IndividualQuestionCreateView(LoginRequiredMixin, CreateView):
    ''' View to create Question without Passage  '''
    model = IndividualQuestion
    form_class = IndividualQuestionForm
    template_name = 'question/question_form.html'

    def get_success_url(self, **kwargs):
        return reverse(
            'cbt:individual-assessment-detail',
            kwargs={'pk':self.get_assessment_object().id}
        )
    def get_assessment_object(self):
        ''' Returns the Assessment object whose questions are created.'''
        return get_object_or_404(
            IndividualAssessment,
            id=self.kwargs.get('pk')
        )

    def form_valid(self, form):
        empty_passage = IndividualQuestionPassage.objects.create(
            title=None,
            body=None,
            no_of_questions=None,
            assessment=self.get_assessment_object(),
        )
        form.instance.passage = empty_passage
        form.instance.assessment = self.get_assessment_object()
        return super().form_valid(form)

    def get_context_data(self, *args,**kwargs ):
        '''Add Passage to the context. '''
        context = super().get_context_data(*args, **kwargs)
        context['assessment'] = self.get_assessment_object()
        context['action_url'] = reverse_lazy(
            'question:individual-create',
            kwargs={'pk':self.get_assessment_object().id}
        )
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


class IndividualQuestionChoiceView(LoginRequiredMixin, TemplateView):
    template_name = 'cbt/question_choice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assessment'] = self.get_assessment_object()
        context['with_passage_url'] = reverse_lazy(
            'question:individual-passage-create',
            kwargs={'pk':self.get_assessment_object().id}
        )
        context['without_passage_url'] = reverse_lazy(
            'question:individual-create',
            kwargs={'pk':self.get_assessment_object().id}
        )
        return context

    def get_assessment_object(self):
        return get_object_or_404(
            IndividualAssessment,
            id=self.kwargs.get('pk')
        )


class IndividualQuestionPassageCreateView(LoginRequiredMixin, CreateView):
    ''' Create Passage for set of questions.
        Returns to question form so questions can be added.
    '''
    model = IndividualQuestionPassage
    form_class = IndividualQuestionPassageForm
    template_name = 'passage/passage_form.html'

    def form_valid(self, form):
        # add assessment instance
        form.instance.assessment = self.get_assessment_object()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'question:individual-question-from-passage-create',
            kwargs={'pk':self.get_form().instance.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assessment'] = self.get_assessment_object()
        return context

    def get_assessment_object(self):
        return get_object_or_404(
            IndividualAssessment,
            id=self.kwargs.get('pk')
        )
