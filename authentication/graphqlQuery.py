def user_by_id_query(user):
    from findTeacherProject.schema import schema

    result = schema.execute(
        """
        query get_user($id: Int!) {
            user_by_id(id: $id) {
                id
                username
                imageprivateusermodel {
                    avatar
                }
                first_name
                last_name
            }
        }
        """
    , variables={'id': user.id})
    new_dict = {}
    new_dict['result'] = result.data["user_by_id"]
    return new_dict