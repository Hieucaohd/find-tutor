def parent_room_by_id_query(parent_room_id):
    from findTeacherProject.schema import schema

    result = schema.execute(
        """
        query get_parent_room($id: ID!) {
            room_by_id(id: $id) {
                id
                parent {
                    id
                    user {
                        username
                    }
                }
                subject
            }
        }
        """
        , variables={'id': parent_room_id}
    )
    return result.data["room_by_id"]

def wating_by_id_query(waiting_item_id):
    from findTeacherProject.schema import schema

    result = schema.execute(
        """
        query get_waiting_item($id: ID!) {
            waiting_by_id(id: $id) {
                id
                tutor {
                    id
                    user {
                        id
                        username
                        imageprivateusermodel {
                            avatar
                        } 
                    }
                    first_name
                    last_name 
                    province_code
                    district_code
                    ward_code
                    profession
                    number_teaching
                    birthday
                    university
                }
            }
        }
        """
    , variables={'id': waiting_item_id})
    new_dict = {}
    new_dict['result'] = result.data["waiting_by_id"]
    return new_dict


def tutor_teaching_by_id_query(tutor_teaching_item_id):
    from findTeacherProject.schema import schema

    result = schema.execute(
        """
        query get_tutor_teaching_item($id: ID!) {
            tutor_teaching_by_id(id: $id) {
                id
                tutor {
                    id
                    user {
                        id
                        username
                        imageprivateusermodel {
                            avatar
                        } 
                    }
                    first_name
                    last_name 
                    province_code
                    district_code
                    ward_code
                    profession
                    number_teaching
                    birthday
                    university
                }
            }
        }
        """
    , variables={'id': tutor_teaching_item_id})
    new_dict = {}
    new_dict['result'] = result.data["tutor_teaching_by_id"]
    return new_dict












