# from django.shortcuts import render
from django.conf import settings
from django.db import transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import (
    NotFound,
    ParseError,
)
from rest_framework.response import Response
from categories.models import Category
from .models import Perk, Experience
from .serializers import (
    ExperienceDetailSerializer,
    PerkSerializer,
)


class Experiences(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceDetailSerializer(
            all_experiences,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceDetailSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            # category(id값 없음, room이 아닐때)
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("카테고리를 입력하세요")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("카테고리의 종류가 experience이어야 합니다")
            except Category.DoesNotExist:
                raise ParseError("카테고리를 찾을 수 없습니다")
            # start가 end보다 같거나 클때
            start = request.data.get("start")
            end = request.data.get("end")
            if start >= end:
                raise ParseError("시작시간(start)이 끝나는시간(end)보다 작아야합니다")
            with transaction.atomic():
                # save
                experience = serializer.save(host=request.user, category=category)

                # perks
                perks_pk = request.data.get("perks")

                if perks_pk:
                    if not isinstance(perks_pk, list):
                        raise ParseError("리스트 형식으로 입력해야합니다")
                    for pk in perks_pk:
                        try:
                            perk = Perk.objects.get(pk=pk)
                        except Perk.DoesNotExist:
                            raise ParseError("perks에 해당 id값은 없습니다")
                        experience.perks.add(perk)

                return Response(serializer.data)

        else:
            return Response(serializer.errors, status=400)


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(
                PerkSerializer(updated_perk).data,
            )
        else:
            return Response(serializer.data)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
