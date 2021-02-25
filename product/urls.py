from django.urls import path
from .views      import CategoryListView, ModelDetailView, FilterListView

urlpatterns = [
    path('/category', CategoryListView.as_view()),
    path('/model', ModelDetailView.as_view()),
    path('/filter', FilterListView.as_view())
    ]