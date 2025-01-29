from .models import CustomUser, Property
from rest_framework import serializers


class CustomuserSerializers(serializers.ModelSerializer) :
    class Meta :
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            # phone_number=validated_data['phone_number']
        )
        user.phone_number=validated_data['phone_number']
        user.set_password(validated_data['password'])
        user.save()

        return user
    

class CustomUserloginSerializers(serializers.ModelSerializer) :
    email=serializers.EmailField(max_length=255)
    class Meta :

        model = CustomUser
        fields = [ 'email', 'password' ]


class PropertySerializers(serializers.ModelSerializer):
    class Meta :
        model = Property
        fields = "__all__"


        
             
    
