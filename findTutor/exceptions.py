class ParentNotOwnerRoom(Exception):

    def __str__(self):
        return f"Phụ huynh không phải là chủ của lớp học này"


class NeedAuthentication(Exception):

    def __str__(self):
        return f"Bạn cần đăng nhập để thực hiện hành động này"


class TutorWasInWaitingList(Exception):

    def __str__(self):
        return f"gia sư đã ở trong danh sách đợi của lớp học"

class TutorWasInListInvited(Exception):

    def __str__(self):
        return f"Gia sư đã ở trong danh sách mời của lớp học"

class TutorWasInTryTeaching(Exception):

    def __str__(self):
        return f"Gia sư đã ở trong danh sách dạy thử của lớp học"

class TutorWasInTutorTeaching(Exception):

    def __str__(self):
        return f"Gia sư đang dạy lớp học này"


class TutorNotInvited(Exception):

    def __str__(self):
        return f"Bạn không phải gia sư được mời dạy ở lớp học này"

class WrongInput(Exception):

    def __str__(self):
        return f"input cua ban co van de"


class ParentRoomIsTeaching(Exception):

    def __str__(self) -> str:
        return "lop hoc dang co nguoi day roi"
