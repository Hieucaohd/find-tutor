from authentication.graphqlQuery import user_by_id_query

class RoomNotificationMessage:
    message_type = {
        "parent_create_room": {
            "id": 1,
            "notify_user_following_parent": {
                "id": "1.1",
            },
        },
        "tutor_apply_in_room": {
            "id": 2,
            "notify_parent": {
                "id": "2.1",
            }
        },
        "tutor_out_from_waiting_list": {
            "id": 3,
            "notify_parent": {
                "id": "3.1",
            }
        },
        "parent_agree_for_tutor_teaching": {
            "id": 4,
            "notify_tutor": {
                "id": "4.1",
            },
        },
        "parent_delete_tutor_from_waiting_list": {
            "id": 5,
            "notify_tutor": {
                "id": "5.1",
            }
        },
        "parent_invite_tutor": {
            "id": 6,
            "notify_tutor": {
                "id": "6.1",
            }
        },
        "tutor_not_agree_parent_invite": {
            "id": 7,
            "notify_parent": {
                "id": "7.1"
            }
        },
        "tutor_agree_for_parent_to_teaching": {
            "id": 8,
            "notify_parent": {
                "id": "8.1",
            },
        },
        "parent_delete_tutor_from_teaching": {
            "id": 9,
            "notify_tutor": {
                "id": "9.1",
            },
        },
        "tutor_out_from_teaching": {
            "id": 10,
            "notify_parent": {
                "id": "10.1",
            },
        },
        "parent_cancel_invite_to_tutor": {
            "id": 11,
            "notify_tutor": {
                "id": "11.1",
            }
        },
        "room_has_tutor_teaching": {
            "id": 12,
            "notify_tutors_in_waiting_list_and_invited_list": {
                "id": "12.1"
            }
        },
        "room_expired_with_tutor_teaching": {
            "id": 13,
            "notify_tutors_in_waiting_list_and_invited_list": {
                "id": "13.1"
            }
        }
    }

    @staticmethod
    def generate_text(id, user_send):
        text = {}
        text["id"] = id["id"]
        text["user_send"] = user_by_id_query(user_send)["result"]
        return text