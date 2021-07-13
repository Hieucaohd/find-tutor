from ..models import ParentModel
from ..serializers import ParentSerializer

from .peopleBaseView import *

from rest_framework.response import Response
from rest_framework import status


class ParentList(PeopleList):
    modelBase = ParentModel
    serializerBase = ParentSerializer


class ParentRetrieve(PeopleRetrieveView):
    modelBase = ParentModel
    serializerBase = ParentSerializer


class ParentUpdate(PeopleUpdateView):
    modelBase = ParentModel
    serializerBase = ParentSerializer


class ParentDetail(PeopleDetail):
    modelBase = ParentModel
    serializerBase = ParentSerializer

