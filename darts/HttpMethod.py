from flask import Request

class HttpMethod(object):

	allowed_methods = frozenset([
		"GET",
		"HEAD",
		"POST",
		"DELETE",
		"PUT",
		"PATCH",
		"OPTIONS"
	])

	def __init__(self, app, input_name = "_method"):
		self.app = app
		self.input_name = input_name

	def __call__(self, environ, start_response):
		request = Request(environ)

		if self.input_name in request.form:
			method = request.form[self.input_name].upper()

			if method in self.allowed_methods:
				environ["REQUEST_METHOD"] = method

		return self.app(environ, start_response)
