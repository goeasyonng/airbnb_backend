# from django.shortcuts import render
# from django.http import JsonResponse
# from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer

class Categories(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serializer= CategorySerializer(all_categories, many=True)
        return Response(serializer.data,)
    
    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(
                CategorySerializer(new_category).data,
            )
        else:
            return Response(serializer.errors)
        

class Category(APIView):
        def get(self,request, pk):
            serializer=CategorySerializer(category)
            return Response(serializer.data)
        
        def put(self,request, pk):
            serializer=CategorySerializer(
                category,data=request.data, partial=True,
            )
        
        def delete(self,request, pk):
            pass
        
            

# @api_view(["GET","POST"])
# def categories(request):
    
#     if request.method =="GET":
#         all_categories = Category.objects.all()
#         serializer= CategorySerializer(all_categories, many=True)
#         return Response(serializer.data,)
#     elif request.method =="POST":
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             new_category = serializer.save()
#             return CategorySerializer(new_category).data,
#             # return Response({'created':True})
#         else:
#             return Response(serializer.errors)
        
    
    
@api_view(["GET","PUT","DELETE"])
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)
    
