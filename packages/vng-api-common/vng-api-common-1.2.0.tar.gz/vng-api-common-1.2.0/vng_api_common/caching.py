import functools
import hashlib

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import mixins, serializers
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.settings import api_settings

from .utils import get_subclasses

CACHE_HEADER = "ETag"


def has_cache_header(view: GenericAPIView) -> bool:
    if view.request.method not in ("GET", "HEAD"):
        return False

    if hasattr(view, "detail") and not view.detail:
        return False

    if not isinstance(view, mixins.RetrieveModelMixin):
        return False

    return True


class ETagMixin(models.Model):
    """
    Automatically calculate the (new) ETag value on save.
    """

    _etag = models.CharField(
        _("etag value"),
        max_length=32,
        help_text=_("MD5 hash of the resource representation in its current version."),
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self._etag = calculate_etag(self)
        super().save(*args, **kwargs)


class APICache:
    def __init__(self, view: GenericAPIView, etag_field: str = "_etag"):
        """
        API Cache interface.

        :param view: the view or viewset instance currently used in the request
        """
        self.view = view
        self.etag_field = etag_field

    @property
    def headers(self) -> dict:
        if not has_cache_header(self.view):
            return {}

        try:
            obj = self.view.get_object()
        except APIException:
            return {}

        etag = getattr(obj, self.etag_field)
        return {CACHE_HEADER: etag}


@functools.lru_cache(maxsize=None)
def _get_serializer_for_models():
    """
    Map models to the serializer to use.

    If multiple serializers exist for a model, it must be explicitly defined.
    """
    model_serializers = {}
    for serializer_class in get_subclasses(serializers.ModelSerializer):
        if not hasattr(serializer_class, "Meta"):
            continue

        model = serializer_class.Meta.model
        if model in model_serializers:
            continue

        model_serializers[model] = serializer_class
    return model_serializers


class StaticRequest(HttpRequest):
    def get_host(self) -> str:
        site = Site.objects.get_current()
        return site.domain

    def _get_scheme(self) -> str:
        return "https" if settings.IS_HTTPS else "http"


def calculate_etag(instance: models.Model) -> str:
    model_class = type(instance)
    serializer_class = _get_serializer_for_models()[model_class]

    # build a dummy request with the configured domain, since we're doing STRONG
    # comparison. Required as context for hyperlinked serializers
    request = Request(StaticRequest())
    request.version = api_settings.DEFAULT_VERSION
    request.versioning_scheme = api_settings.DEFAULT_VERSIONING_CLASS()

    serializer = serializer_class(instance=instance, context={"request": request})

    # render the output to json, which is used as hash input
    renderer = CamelCaseJSONRenderer()
    rendered = renderer.render(serializer.data, "application/json")

    # calculate md5 hash
    return hashlib.md5(rendered).hexdigest()
