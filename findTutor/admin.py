from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TutorModel)
admin.site.register(ParentModel)
admin.site.register(ParentRoomModel)
admin.site.register(PriceModel)
admin.site.register(WaitingTutorModel)
admin.site.register(TutorTeachingModel)
admin.site.register(NotifiedParentModel)
admin.site.register(NotifiedTutorModel)
admin.site.register(CommentAboutTutorModel)
admin.site.register(ListInvitedModel)
admin.site.register(TryTeachingModel)
admin.site.register(OldLocationModel)