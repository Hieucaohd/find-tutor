import graphene

from findTutor.inputs import *
from findTutor.types import *
from findTutor.models import *

class CreateParentRoomMutation(graphene.Mutation):
	class Arguments:
		input_fields = ParentRoomInput(required=True)


	parent_room = graphene.Field(ParentRoomType)

	@classmethod
	def mutate(cls, root, info, input_fields):
		parent = ParentModel.objects.get(user=info.context.user)
		parent_room = ParentRoomModel.objects.create(province_code   = input_fields.province_code, 
													 district_code   = input_fields.district_code,
													 ward_code 	     = input_fields.ward_code,
													 detail_location = input_fields.detail_location,
													 subject 		 = input_fields.subject,
													 lop 			 = input_fields.lop, 
													 day_can_teach 	 = input_fields.day_can_teach,
													 other_require 	 = input_fields.other_require,
													 parent 		 = parent)
		if input_fields.prices:
			for price in input_fields.prices:
				PriceModel.objects.create(parent_room 	  = parent_room,
										  time_in_one_day = price.time_in_one_day,
										  money_per_day   = price.money_per_day,
										  type_teacher    = price.type_teacher,
										  sex_of_teacher  = price.sex_of_teacher)
		return CreateParentRoomMutation(parent_room=parent_room)