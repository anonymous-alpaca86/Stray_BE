from rest_framework import serializers
from .models import Pet,User


class UserSerializer(serializers.Serializer):
    class Meta:
        model=User
        fields=['id','username','email']
class PetSerializer(serializers.ModelSerializer):
    posted_by=UserSerializer(read_only=True)
    class Meta:
        model=Pet
        fields='__all__'
        read_only_fields='created_at'
    def validate_color(self,value):
        if len(value)<3:
            raise serializers.ValidationError("Color description too short")
        return value
    def validate(self,data):
        if data['status']=='lost' and not data.get('description'):
            raise serializers.ValidationError("Lost pet need a description")
        return data


