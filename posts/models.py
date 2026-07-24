from django.db import models
from django.contrib.auth.models import User

# Create your models here.



    

class Pet(models.Model):
    SPECIES_CHOICES =[
        ('cat','Cat'),
        ('dog','Dog'),
        ('other','Other'),
    ]
    species=models.CharField(max_length=100, choices=SPECIES_CHOICES)
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='pets/', blank=True, null=True)
    posted_by=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES =[
        ('lost','Lost'),
        ('stray','Stray'),
        ('fostered','Fostered'),
    ]
    status=models.CharField(max_length=100, choices= STATUS_CHOICES)
    COLOR_CHOICES = [
        ('black','Black'),
        ('white','White'),
        ('orange','Orange'),
        ('grey', 'Grey'),
        ('other', 'Other'),
    ]
    color=models.CharField(max_length=100, choices=COLOR_CHOICES)
    def __str__(self):
        return self.name
    