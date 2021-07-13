from ..models import TutorModel
from ..serializers import TutorSerializer

from .peopleBaseView import *


class TutorList(PeopleList):
    modelBase = TutorModel
    serializerBase = TutorSerializer


class TutorRetrieve(PeopleRetrieveView):
    modelBase = TutorModel
    serializerBase = TutorSerializer


class TutorUpdate(PeopleUpdateView):
    modelBase = TutorModel
    serializerBase = TutorSerializer


class TutorDetail(PeopleDetail):
    modelBase = TutorModel
    serializerBase = TutorSerializer
