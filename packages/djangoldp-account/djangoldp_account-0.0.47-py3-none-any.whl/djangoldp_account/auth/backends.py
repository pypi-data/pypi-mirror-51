import json

from django.contrib.auth.backends import ModelBackend, UserModel
from django.core.exceptions import PermissionDenied
from jwkest import BadSyntax
from jwkest.jwt import JWT

from djangoldp_account.auth.solid import Solid
from djangoldp_account.errors import LDPLoginError


class ExternalUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        user = None
        if 'HTTP_AUTHORIZATION' in request.META:
            jwt = request.META['HTTP_AUTHORIZATION']
            if jwt.startswith("Bearer"):
                jwt = jwt[7:]
            username = kwargs.get(UserModel.USERNAME_FIELD)
            _jwt = JWT()
            try:
                unpacked = json.loads(_jwt.unpack(jwt).part[1])
            except BadSyntax:
                return
            try:
                id_token = json.loads(_jwt.unpack(unpacked['id_token']).part[1])
            except KeyError:
                id_token = unpacked
            try:
                Solid.check_id_token_exp(id_token['exp'])


                Solid.confirm_webid(id_token['sub'], id_token['iss'])
            except LDPLoginError as e:
                raise PermissionDenied(e.description)
            userinfo = {
                'sub': id_token['sub']
            }
            user = Solid.get_or_create_user(userinfo, id_token['sub'])
        else:
            if username is None:
                username = kwargs.get(UserModel.USERNAME_FIELD)
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a non-existing user (#20760).
                UserModel().set_password(password)

        if self.user_can_authenticate(user):
            return user

