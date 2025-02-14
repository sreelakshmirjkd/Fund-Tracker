from rest_framework import serializers

from django.contrib.auth.models import User

from expense.models import Transaction

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ["id", "username", "email", "password"]

        read_only_fields = ["id"]   

    def create(self, validated_data): # method overriding of the existing function -- ModelSerialzer -- def create. This is for password encryption.

        return User.objects.create_user(**validated_data) # for password encryption 

class TransactionSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField(read_only=True) # To get the username as a string instead of number -- if there is a relation with owner and a model(here User model, so that "def __str" will work) inside models.py file.

    class Meta:

        model = Transaction    

        fields = "__all__" # double underscore

        read_only_fields = ["id", "created_date", "owner"] 