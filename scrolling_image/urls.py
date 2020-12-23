from django.urls import path
from . import views
app_name = 'scrolling'

urlpatterns = [
    path(
        'list/',
        views.ScrollingImageListView.as_view(),
        name='scrolling-image-list'
    ),
    path(
        'sample-questions/',
        views.ScrollingSampleQuestionPassageListView.as_view(),
        name='scrolling-sample-questions'
    ),
]