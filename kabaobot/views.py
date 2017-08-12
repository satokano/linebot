from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Entry
from .serializer import EntrySerializer

# Create your views here.
class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

