from django.shortcuts import render
from .models import ScrollingImage
from django.views.generic import(
    ListView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from question.models import (
    IndividualQuestionPassage,
    IndividualQuestion,
    )
from choice.models import(
    IndividualChoice
)



class ScrollingImageListView(ListView):
    ''' View to render list of ScrollingImage Instances. '''

    model = ScrollingImage

    def get(self, request):
        images = self.get_queryset()
        image_urls = []
        for image in images:
            image_urls.append(image.image.url)

        data = {
            'scrolling_images': list(self.get_queryset().values()),
            'image_urls': image_urls
        }
        return JsonResponse(data)

    def get_queryset(self, **kwargs):
        try:
            scrolling_images = ScrollingImage.objects.all()
        except ScrollingImage.DoesNotExist:
            scrolling_images = ()
        return scrolling_images


class ScrollingSampleQuestionPassageListView(ListView):
    ''' View to render list of sample Questions with passage.  '''
    model = IndividualQuestionPassage

    def get(self, request):
        questions = self.get_related_questions(tuple(self.get_queryset().values()))
        choices = self.get_related_choices(questions)
        data = {
            'passages': list(self.get_queryset().values()),
            'questions': questions,
            'choices': choices,
        }
        return JsonResponse(data)

    def get_queryset(self, **kwargs):
        ''' Returns first 4 of the available passages.'''
        queryset = ()
        try:
            queryset = IndividualQuestionPassage.objects.filter(
                assessment__is_sample=True,
                body__isnull=False
            )[0:4]
        except IndividualQuestionPassage.DoesNotExist:
            pass
        return queryset


    def get_related_questions(self, passage_queryset):
        ''' Returns question belonging to each passage in the passage queryset.'''
        question_queryset = []
        for passage in passage_queryset:
            try:
                question_queryset += list(IndividualQuestion.objects.filter(
                        passage__id=passage.get('id')
                    ).values())

            except IndividualQuestion.DoesNotExist:
                pass
        return question_queryset

    def get_related_choices(self, question_queryset):
        ''' Returns choices belonging to each question in the question queryset.'''
        choice_queryset = []
        for question in question_queryset:
            try:
                choice_queryset += list(IndividualChoice.objects.filter(
                        question__id=question.get('id')
                    ).values())

            except IndividualChoice.DoesNotExist:
                pass
        return choice_queryset


class ScrollingSampleQuestionListView(ListView):
    ''' Returns list of questions belong to a passage '''
    pass