# coding: utf-8

from django.conf.urls import url
from rest_framework import routers
from . import views
from . import funcviews

router = routers.DefaultRouter()
router.register(r'entries', views.EntryViewSet)

