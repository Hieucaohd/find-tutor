from findTutor.permissions import isTutor, isParent
from findTutor.models import TutorModel, ParentModel

def inforAboutUser(user):
    
    token = user.tokens()
    
    dict_return = {
        'email': user.email,
        'username': user.username,
        'token': token.get('access', ''),
        'refresh_token': token.get('refresh', ''),
        'id': user.id,
        'type_tutor': False,
        'type_parent': False,
    }

    type_tutor = isTutor(user)
    type_parent = isParent(user)

    if type_tutor:
        dict_return['type_tutor'] = True
        dict_return['id_tutor'] = TutorModel.objects.get(user=user).id
    else:
        dict_return['type_tutor'] = False

    if type_parent:
        dict_return['type_parent'] = True
        dict_return['id_parent'] = ParentModel.objects.get(user=user).id
    else:
        dict_return['type_parent'] = False

    return dict_return
