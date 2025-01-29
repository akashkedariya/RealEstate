from django.shortcuts import render
from .models import CustomUser, Property    
from .serializers import CustomuserSerializers, PropertySerializers, CustomUserloginSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Customuserlist(APIView):

    def post(self, request):
        serializer = CustomuserSerializers(data = request.data)
        print('====dhua')
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class UserLoginView(APIView):
#     def post(self, request):
#         user = authenticate(email = request.data['email'], password=request.data['password'])
#         if user:
#             # print('===user===',user)
#             token = get_tokens_for_user(user)
#             print('===token==',token)
#             return Response({'message' :'login successfully','token': token})
#         else:
#             return Response({'error': 'Invalid credentials'}, status=401)


class UserLoginView(APIView) :

    def post(self,request,format=None):
        serializer = CustomUserloginSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):

            email = serializer.data.get('email')
            password = serializer.data.get('password')
           
            user = authenticate(email=email,password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg':'login success','token':token},status=status.HTTP_200_OK)
            
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid. ']}},status=status.HTTP_200_OK)  
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class Propertyview(APIView) :

    # permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise Http404

    def get(self,request,pk=None):
        if pk:
            data = self.get_object(pk)
            serilizer = PropertySerializers(data)
            return Response(serilizer.data)

        data = Property.objects.all()
        serilizer = PropertySerializers(data, many = True)
        return Response(serilizer.data)

    def post(self, request) :
        serializer = PropertySerializers(data = request.data)
                                                                
        if serializer.is_valid():
            serializer.save()
                                                                            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Propertydetailes(APIView) :

#     def get_object(self, pk):
#         try:
#             return Property.objects.get(pk=pk)
#         except Property.DoesNotExist:
#             raise Http404

#     def get(self,request,pk=None):

#         if pk:
#             data = self.get_object(pk)
#             serilizer = PropertySerializers(data)
#             return Response(serilizer.data)

#         data = Property.objects.all()
#         serilizer = PropertySerializers(data, many = True)
#         return Response(serilizer.data)



class MultiAPISearchView(generics.ListAPIView):
    queryset = Property.objects.all()
    queryset = Property.objects.order_by('title')
    serializer_class = PropertySerializers

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter
    ]

    search_fields = ['title','location']        
    # filterset_fields = ['title', 'location']      
    ordering_fields = ['title']     

# from django.contrib.postgres.search import SearchQuery, SearchRank

# class MultiAPISearchView(generics.ListAPIView):
#     serializer_class = PropertySerializers
    
#     def get_queryset(self):
#         query = self.request.query_params.get('query', '')
#         if query:
#             data = Property.objects.annotate(
#                 rank=SearchRank('search_vector', SearchQuery(query))
#             ).filter(rank__gte=0.1).order_by('-rank')
#             print('===data=1==',data)

#             return data
        
#         data = Property.objects.all()
#         print('===data=2==',data)
#         return data