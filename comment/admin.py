from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CommentAboutTutorModel)
admin.site.register(CommentAboutParentModel)
admin.site.register(CommentAboutParentRoomModel)