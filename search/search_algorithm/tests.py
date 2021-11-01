from django.test import TestCase

from findTutor.models import *

from .search import *


class SearchAllRoomTestCase(TestCase):
    def setUp(self):
        ParentRoomModel.objects.create()
