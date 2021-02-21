from django.urls import path
from .views      import BackpackListView,ModelListView

urlpatterns = [
    path('/backpacks', BackpackListView.as_view()),
    path('/models', ModelListView.as_view())
    ]