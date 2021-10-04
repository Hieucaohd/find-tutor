from rest_framework_simplejwt.authentication import JWTAuthentication

from channels.auth import AuthMiddlewareStack

from django.contrib.auth.models import AnonymousUser

from django.conf import settings

import jwt

from authentication.models import User

from channels.middleware import BaseMiddleware

from asgiref.sync import sync_to_async

from channels.db import database_sync_to_async

from django.contrib import auth

from threading import Thread


class TokenAuthMiddleware(BaseMiddleware):
	def __init__(self, inner):
		self.inner = inner
		self.simple_jwt = JWTAuthentication()
		super().__init__(inner)

	async def __call__(self, scope, receive, send):
		headers = dict(scope['headers'])
		subprotocols = dict([scope['subprotocols']])
		try:
			token_prefix, token_key = None, None
			if b'authorization' in headers:
				token_prefix, token_key = headers[b'authorization'].decode().split()
			elif 'Token' in subprotocols:
				token_prefix, token_key = subprotocols['Token'].split()
			
			if token_prefix == settings.TOKEN_PREFIX:
				validated_token = await sync_to_async(self.simple_jwt.get_validated_token)(token_key)
				user = await sync_to_async(self.simple_jwt.get_user)(validated_token)
				scope['user'] = user
			else:
				raise Exception("invalid token prefix")
		except:
			scope['user'] = AnonymousUser()
		return await super().__call__(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
