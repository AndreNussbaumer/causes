from django.urls import path
from causes.views import (

    create_causes_view,
    detail_causes_view,
    edit_causes_view,
    delete_causes_view,
    CauseLikeToggle,
)

app_name = 'causes'

urlpatterns = [
    path('create/', create_causes_view, name="create"),
    path('<slug>/', detail_causes_view, name='detail'),
    path('<slug>/like', CauseLikeToggle.as_view(), name='like-toggle'),
    path('<slug>/edit', edit_causes_view, name='edit'),
    path('<slug>/delete', delete_causes_view, name='delete'),

]
