import pytest
from django.test import RequestFactory
from iati.factory import iati_factory
from api.region import serializers


class TestRegionSerializers:

    request_dummy = RequestFactory().get('/')

    @pytest.mark.django_db
    def test_RegionSerializer(self):
        region = iati_factory.RegionFactory.build(
            code='10',
            name='Region A'
        )
        serializer = serializers.RegionSerializer(region, context={'request': self.request_dummy})
        assert serializer.data['code'] == region.code, \
            """
            the data in region.code should be serialized to a field named code
            inside the serialized object
            """
        assert serializer.data['name'] == region.name, \
            """
            the data in region.name should be serialized to a field named code
            inside the serialized object
            """