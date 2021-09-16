import graphene


class PriceInput(graphene.InputObjectType):
	time_in_one_day = graphene.Int(required=True)
	money_per_day = graphene.Int(required=True)
	type_teacher = graphene.List(graphene.String, required=True)
	sex_of_teacher = graphene.List(graphene.String, required=True)


class ParentRoomInput(graphene.InputObjectType):
	province_code = graphene.Int(required=True)
	district_code = graphene.Int(required=True)
	ward_code = graphene.Int(required=True)

	detail_location = graphene.String(required=False)

	subject = graphene.String(required=True)
	lop = graphene.Int(required=True)
	day_can_teach = graphene.List(graphene.Int, required=True)
	other_require = graphene.String(required=False)

	prices = graphene.List(PriceInput, required=False)