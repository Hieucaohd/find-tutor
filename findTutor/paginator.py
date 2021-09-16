from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginator_function(query_set, num_in_page, page):
	paginator = Paginator(query_set, num_in_page)

	try:
		list_item = paginator.page(page)
	except PageNotAnInteger:
		print("not integer")
		list_item = paginator.page(1)
	except EmptyPage:
		print("empty page")
		list_item = paginator.page(paginator.num_pages)

	return list_item