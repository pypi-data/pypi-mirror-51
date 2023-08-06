#  BSD 3-Clause License
#
#  Copyright (c) 2012, the Sentry Team, see AUTHORS for more details
#  Copyright (c) 2019, Elasticsearch BV
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  * Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE


from __future__ import absolute_import

import json
import logging

import django
import xmltodict
from django.conf import settings as django_settings
from django.core.exceptions import DisallowedHost
from django.db import DatabaseError
from django.http import HttpRequest

from elasticapm.base import Client
from elasticapm.conf import constants
from elasticapm.contrib.django.utils import iterate_with_template_sources
from elasticapm.utils import compat, encoding, get_url_dict
from elasticapm.utils.module_import import import_string
from elasticapm.utils.wsgi import get_environ, get_headers

__all__ = ("DjangoClient",)


default_client_class = "elasticapm.contrib.django.DjangoClient"
_client = (None, None)


def get_client(client=None):
    """
    Get an ElasticAPM client.

    :param client:
    :return:
    :rtype: elasticapm.base.Client
    """
    global _client

    tmp_client = client is not None
    if not tmp_client:
        config = getattr(django_settings, "ELASTIC_APM", {})
        client = config.get("CLIENT", default_client_class)

    if _client[0] != client:
        client_class = import_string(client)
        instance = client_class()
        if not tmp_client:
            _client = (client, instance)
        return instance
    return _client[1]


class DjangoClient(Client):
    logger = logging.getLogger("elasticapm.errors.client.django")

    def __init__(self, config=None, **inline):
        if config is None:
            config = getattr(django_settings, "ELASTIC_APM", {})
        if "framework_name" not in inline:
            inline["framework_name"] = "django"
            inline["framework_version"] = django.get_version()
        super(DjangoClient, self).__init__(config, **inline)

    def get_user_info(self, request):
        user_info = {}

        if not hasattr(request, "user"):
            return user_info
        try:
            user = request.POST or request.GET
            if hasattr(user, "is_authenticated"):
                if callable(user.is_authenticated):
                    user_info["is_authenticated"] = user.is_authenticated()
                else:
                    user_info["is_authenticated"] = bool(user.is_authenticated)
            if hasattr(user, "get_username"):
                user_info["username"] = encoding.keyword_field(encoding.force_text(user.get_username()))
            elif hasattr(user, "username"):
                user_info["username"] = encoding.keyword_field(encoding.force_text(user.username))

            if hasattr(user, "email"):
                user_info["email"] = encoding.force_text(user.email)
        except DatabaseError:
            # If the connection is closed or similar, we'll just skip this
            return {}

        return user_info

    def get_data_from_request(self, request, initial_body):
        result = {
            "env": dict(get_environ(request.META)),
            "method": request.method,
            "socket": {"remote_address": request.META.get("REMOTE_ADDR"), "encrypted": request.is_secure()},
            "cookies": dict(request.COOKIES),
        }
        if self.config.capture_headers:
            result["headers"] = dict(get_headers(request.META))
        result["body"] = initial_body

        if hasattr(request, "get_raw_uri"):
            # added in Django 1.9
            url = request.get_raw_uri()
        else:
            try:
                # Requires host to be in ALLOWED_HOSTS, might throw a
                # DisallowedHost exception
                url = request.build_absolute_uri()
            except DisallowedHost:
                # We can't figure out the real URL, so we have to set it to
                # DisallowedHost
                result["url"] = {"full": "DisallowedHost"}
                url = None
        if url:
            result["url"] = get_url_dict(url)
        return result

    def get_data_from_response(self, response):
        result = {"status_code": response.status_code}

        if self.config.capture_headers and hasattr(response, "items"):
            result["headers"] = dict(response.items())
        return result

    @staticmethod
    def internationalize_phone_number(phone_number):
        return "{}{}".format('00', phone_number)

    def get_orange_params(self, request):
        data = request.GET.dict()
        data.update({'msisdn': request.META['HTTP_USER_MSISDN']})
        if not data.get('NomVariable'):
            data.update({'new-session': True})
        else:
            data.update({'new-session': False})
        return data

    def read_soap_xml_payload(self, request):
        return xmltodict.parse(request.body.decode('utf-8'))

    def get_dynamic_menu(self, request):
        xml = self.read_soap_xml_payload(request=request)
        dynamic_menu_request = xml.get('USSDDynMenuRequest')
        return dynamic_menu_request

    def get_equity_data(self, request):
        phone_number = self.internationalize_phone_number(self.get_dynamic_menu(request=request).get('msisdn', ''))
        request_id = self.get_dynamic_menu(request=request).get('requestId', '')
        user_input = self.get_dynamic_menu(request=request).get('userData', '')
        star_code = self.get_dynamic_menu(request=request).get('starCode', '')

        new_session = False if user_input else True

        return {'msisdn': phone_number, 'session_id': request_id,
                'user_input': user_input, 'star_code': star_code,
                'new-session': new_session}

    def get_body(self, request):
        path = request.path
        if 'ivory_coast' in path:
            return self.get_orange_params(request=request)
        elif 'api' in path:
            data = json.loads(request.body.decode('utf-8'))
            data.update({'password': '*' * 4})
            return data
        elif 'kenya/equitel/ussd' in path:
            return self.get_equity_data(request=request)
        elif 'payment' in path:
            data = json.loads(self.initial_request_body.decode('utf-8'))
            data.update({'password': '*' * 4})
            return data
        else:
            return 'REDACTED'

    def capture(self, event_type, request=None, **kwargs):
        if "context" not in kwargs:
            kwargs["context"] = context = {}
        else:
            context = kwargs["context"]

        is_http_request = isinstance(request, HttpRequest)
        if is_http_request:
            context["request"] = self.get_data_from_request(
                request, initial_body=self.get_body(request=request)
            )
            context["user"] = self.get_user_info(request)

        result = super(DjangoClient, self).capture(event_type, **kwargs)

        if is_http_request:
            # attach the elasticapm object to the request
            request._elasticapm = {"service_name": self.config.service_name, "id": result}

        return result

    def _get_stack_info_for_trace(
        self,
        frames,
        library_frame_context_lines=None,
        in_app_frame_context_lines=None,
        with_locals=True,
        locals_processor_func=None,
    ):
        """If the stacktrace originates within the elasticapm module, it will skip
        frames until some other module comes up."""
        return list(
            iterate_with_template_sources(
                frames,
                with_locals=with_locals,
                library_frame_context_lines=library_frame_context_lines,
                in_app_frame_context_lines=in_app_frame_context_lines,
                include_paths_re=self.include_paths_re,
                exclude_paths_re=self.exclude_paths_re,
                locals_processor_func=locals_processor_func,
            )
        )

    def send(self, url, **kwargs):
        """
        Serializes and signs ``data`` and passes the payload off to ``send_remote``

        If ``server`` was passed into the constructor, this will serialize the data and pipe it to
        the server using ``send_remote()``.
        """
        if self.config.server_url:
            return super(DjangoClient, self).send(url, **kwargs)
        else:
            self.error_logger.error("No server configured, and elasticapm not installed. Cannot send message")
            return None


class ProxyClient(object):
    """
    A proxy which represents the current client at all times.
    """

    # introspection support:
    __members__ = property(lambda x: x.__dir__())

    # Need to pretend to be the wrapped class, for the sake of objects that care
    # about this (especially in equality tests)
    __class__ = property(lambda x: get_client().__class__)

    __dict__ = property(lambda o: get_client().__dict__)

    __repr__ = lambda: repr(get_client())
    __getattr__ = lambda x, o: getattr(get_client(), o)
    __setattr__ = lambda x, o, v: setattr(get_client(), o, v)
    __delattr__ = lambda x, o: delattr(get_client(), o)

    __lt__ = lambda x, o: get_client() < o
    __le__ = lambda x, o: get_client() <= o
    __eq__ = lambda x, o: get_client() == o
    __ne__ = lambda x, o: get_client() != o
    __gt__ = lambda x, o: get_client() > o
    __ge__ = lambda x, o: get_client() >= o
    if compat.PY2:
        __cmp__ = lambda x, o: cmp(get_client(), o)  # noqa F821
    __hash__ = lambda x: hash(get_client())
    # attributes are currently not callable
    # __call__ = lambda x, *a, **kw: get_client()(*a, **kw)
    __nonzero__ = lambda x: bool(get_client())
    __len__ = lambda x: len(get_client())
    __getitem__ = lambda x, i: get_client()[i]
    __iter__ = lambda x: iter(get_client())
    __contains__ = lambda x, i: i in get_client()
    __getslice__ = lambda x, i, j: get_client()[i:j]
    __add__ = lambda x, o: get_client() + o
    __sub__ = lambda x, o: get_client() - o
    __mul__ = lambda x, o: get_client() * o
    __floordiv__ = lambda x, o: get_client() // o
    __mod__ = lambda x, o: get_client() % o
    __divmod__ = lambda x, o: get_client().__divmod__(o)
    __pow__ = lambda x, o: get_client() ** o
    __lshift__ = lambda x, o: get_client() << o
    __rshift__ = lambda x, o: get_client() >> o
    __and__ = lambda x, o: get_client() & o
    __xor__ = lambda x, o: get_client() ^ o
    __or__ = lambda x, o: get_client() | o
    __div__ = lambda x, o: get_client().__div__(o)
    __truediv__ = lambda x, o: get_client().__truediv__(o)
    __neg__ = lambda x: -(get_client())
    __pos__ = lambda x: +(get_client())
    __abs__ = lambda x: abs(get_client())
    __invert__ = lambda x: ~(get_client())
    __complex__ = lambda x: complex(get_client())
    __int__ = lambda x: int(get_client())
    if compat.PY2:
        __long__ = lambda x: long(get_client())  # noqa F821
    __float__ = lambda x: float(get_client())
    __str__ = lambda x: str(get_client())
    __unicode__ = lambda x: compat.text_type(get_client())
    __oct__ = lambda x: oct(get_client())
    __hex__ = lambda x: hex(get_client())
    __index__ = lambda x: get_client().__index__()
    __coerce__ = lambda x, o: x.__coerce__(x, o)
    __enter__ = lambda x: x.__enter__()
    __exit__ = lambda x, *a, **kw: x.__exit__(*a, **kw)


client = ProxyClient()


def _get_installed_apps_paths():
    """
    Generate a list of modules in settings.INSTALLED_APPS.
    """
    out = set()
    for app in django_settings.INSTALLED_APPS:
        out.add(app)
    return out
