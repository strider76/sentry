from __future__ import absolute_import

from django import template
from django.http import HttpRequest

from sentry.api.serializers.base import serialize as serialize_func
from sentry.api.serializers.models.organization import (
    DetailedOrganizationSerializer
)
from sentry.utils import json


register = template.Library()


@register.simple_tag(takes_context=True)
def serialize(context, obj):
    if 'request' in context:
        user = context['request'].user
    else:
        user = None

    return convert_to_json(serialize_func(obj, user))


@register.simple_tag
def convert_to_json(obj):
    return json.dumps_htmlsafe(obj)


@register.simple_tag(takes_context=True)
def serialize_detailed_org(context, obj):
    if 'request' in context:
        user = context['request'].user
    else:
        user = None

    context = serialize_func(
        obj,
        user,
        DetailedOrganizationSerializer(),
    )

    return convert_to_json(context)


@register.simple_tag
def get_user_context(request, escape=False):
    if isinstance(request, HttpRequest):
        user = getattr(request, 'user', None)
        result = {'ip_address': request.META['REMOTE_ADDR']}
        if user and user.is_authenticated():
            result.update({
                'email': user.email,
                'id': user.id,
            })
            if user.name:
                result['name'] = user.name
    else:
        result = {}
    return convert_to_json(result)
