from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status, permissions,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PetSerializer, UserSerializer
from .models import Pet
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, PermissionDenied

class PetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'  # user can change page size
    max_page_size = 50

class PetListView(generics.ListCreateAPIView):
    queryset=Pet.objects.all()
    serializer_class=PetSerializer
    filterset_fields=['species','status','location']
    pagination_class = PetPagination
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'location', 'color']
    ordering_fields = ['created_at', 'species']
    ordering = ['-created_at'] 
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)
  
class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Pet.objects.all()
    serializer_class=PetSerializer

    def get_object(self):
        try:
            pet=Pet.objects.get(pk=self.kwargs['pk'])
        except Pet.DoesNotExist:
            raise NotFound("Pet not found")
        if pet.posted_by !=self.request.user:
            raise PermissionDenied("You don't own this pet")
        return pet
class ClaimPetView(APIView):
    def post(self,request,pk):
        pet=get_object_or_404(Pet, pk=pk)
        pet.status="claimed"
        pet.saved()
        return Response({
            "status":"claimed"
        })
class MyPetView(generics.ListAPIView):
    serializer_class=PetSerializer
    def get_queryset(self):
        return Pet.bjects.filter(posted_by=self.request.user)

