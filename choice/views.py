from django.shortcuts import (
    render,
    reverse,
    get_list_or_404,
    get_object_or_404,
    redirect
)
from django.views.generic import(
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import IndividualChoiceForm, InstitutionChoiceForm
from .models import IndividualChoice, InstitutionChoice
from question.models import IndividualQuestion

#===============================================
# Views for CRUD operations on Individual Choices Instances.
#===============================================


class IndividualChoiceCreateView(LoginRequiredMixin, CreateView):
    model = IndividualChoice
    form_class = IndividualChoiceForm
    template_name = 'choice/choice_form.html'

    def get_success_url(self, **kwargs):
        return reverse(
            'cbt:individual-assessment-detail',
            kwargs={'pk':self.get_question_object().assessment.id}
        )

    def get_question_object(self):
        ''' Returns the Question object whose choices are created.'''
        question_object_id = self.kwargs.get('pk')
        question_object = get_object_or_404(
            IndividualQuestion,
            id=question_object_id
        )
        return question_object

    def form_valid(self, form):
        form.instance.question = self.get_question_object()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.get_question_object()
        try:
            context['choices'] = IndividualChoice.objects.filter(
                question_id=self.get_question_object().id
            )
        except IndividualChoice.DoesNotExist:
            context['choices'] = None
        return context


class IndividualChoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = IndividualChoice
    form_class = IndividualChoiceForm
    template_name = 'choice/choice_update_form.html'
    context_object_name = 'choice'

    def get_success_url(self):
        return reverse(
            'cbt:individual-assessment-detail',
            kwargs={'pk':self.get_object().question.assessment.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['choices'] = IndividualChoice.objects.filter(
                question_id=self.get_object().question.id
            )
        except IndividualChoice.DoesNotExist:
            context['choices'] = None
        return context


class IndividualChoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = IndividualChoice
    form_class = IndividualChoiceForm
    template_name = 'choice/choice_delete_confirm.html'
    context_object_name = 'choice'

    def get_success_url(self):
        return reverse(
            'cbt:individual-assessment-detail',
            kwargs={'pk':self.get_object().question.assessment.id}
        )
