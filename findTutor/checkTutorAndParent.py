from .models import TutorModel, ParentModel


def isTutor(user):
    take_tutor_request = TutorModel.objects.filter(user=user)
    if take_tutor_request:
        return True
    return False


def isParent(user):
    take_parent_request = ParentModel.objects.filter(user=user)
    if take_parent_request:
        return True
    return False