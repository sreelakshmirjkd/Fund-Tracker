from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView

from api.serializers import UserSerializer, TransactionSerializer

from rest_framework.response import Response

from rest_framework import authentication, permissions

from expense.models import Transaction

from rest_framework import serializers

from api.permissions import IsOwnerOnly

from rest_framework.generics import CreateAPIView

# Create your views here.


# new method -- inbuilt
# =====================

class ApiSignupView(CreateAPIView):

    serializer_class = UserSerializer

# -------------------------------------------------

# old method
# -----------

# class ApiSignupView(CreateAPIView):

    # def post(self, request, *args, **kwargs):

    #     serializer_instance = UserSerializer(data=request.data)

    #     if serializer_instance.is_valid():

    #         serializer_instance.save() # encryption is given in serializers.py

    #         return Response(data=serializer_instance.data)
        
    #     else:

    #         return Response(data=serializer_instance.errors)




class TransactionListCreateView(APIView):

    serializer_class = TransactionSerializer

    # authentication_classes = [authentication.BasicAuthentication]

    authentication_classes =[authentication.TokenAuthentication]
    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        qs = Transaction.objects.filter(owner=request.user)

        serializer_instance = TransactionSerializer(qs, many=True)

        return Response(data=serializer_instance.data)
    
    def post(self, request, *args, **kwargs):

        serialiser_instance = self.serializer_class(data=request.data) 

        if serialiser_instance.is_valid():

            serialiser_instance.save(owner=request.user) # this line is different from create.

            return Response(data=serialiser_instance.data)
        
        else:

            return Response(data=serialiser_instance.errors)
        
class TransactionRetrieveUpdateDestroyView(APIView):

    serializer_class = TransactionSerializer

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [IsOwnerOnly]

    def get(self, request, *args, **kwargs):

        id = kwargs.get("pk")

        transaction_object = get_object_or_404(Transaction, id=id) # To not get the program stopped whwn error response comes.

        self.check_object_permissions(request, transaction_object) # To move into IsOwnerOly. checking the permission over the object

        serializer_instance = self.serializer_class(transaction_object, many=False)

        return Response(data=serializer_instance.data)
    
    def delete(self, request, *args, **kwargs):

        id = kwargs.get("pk")

        transaction_object = get_object_or_404(Transaction, id=id)

        self.check_object_permissions(request, transaction_object)

        transaction_object.delete()

        return Response(data={"message": "Deleted"})

    def put(self, request, *arga, **kwargs):

        id = kwargs.get("pk")

        transaction_object = get_object_or_404(Transaction, id=id)


        serializer_instance = TransactionSerializer(data=request.data, instance=transaction_object)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)
        

    def patch(self, request, *args, **kwargs):

        id = kwargs.get("pk")

        transaction_object = get_object_or_404(Transaction, id=id)

        if transaction_object.owner != request.user:

            raise serializers.ValidationError("You are not permitted to perform this action")

        serializer_instance = TransactionSerializer(data=request.data, instance=transaction_object)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)
        
        

            





