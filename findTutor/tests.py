from django.test import TestCase

# Create your tests here.
# for test
def who_is(request):
	print("\nrequest")
	print(request)

	print("\ndir request")
	print(dir(request))

	print("\nuser")
	print(request.user)

	print("\ndir user")
	print(dir(request.user))

	try:
		print(request.user.password)
	except:
		print("khong co mat khau")