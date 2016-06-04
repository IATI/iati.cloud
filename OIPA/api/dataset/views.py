from api.dataset.serializers import DatasetSerializer, SimpleDatasetSerializer
from iati_synchroniser.models import IatiXmlSource, Publisher
from rest_framework.generics import RetrieveAPIView
from rest_framework.filters import OrderingFilter, DjangoFilterBackend
from api.dataset.filters import DatasetFilter
from api.aggregation.views import AggregationView, Aggregation, GroupBy
from django.db.models import Sum, Count
from api.generics.views import DynamicListView, DynamicDetailView
from api.publisher.serializers import PublisherSerializer


class DatasetList(DynamicListView):
    """
    Returns a list of IATI datasets stored in OIPA.

    ## Request parameters

    - `ref` (*optional*): ref to search for.
    - `type` (*optional*): Filter datasets by type (activity or organisation).
    - `publisher` (*optional*): List of publisher refs.


    ## Result details

    Each result item contains full information about datasets including URI
    to dataset details.

    URI is constructed as follows: `/api/datasets/{ref}`

    """
    queryset = IatiXmlSource.objects.all()
    serializer_class = DatasetSerializer
    filter_class = DatasetFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = '__all__'

    fields = (
        'ref',
        'title',
        'type',
        'publisher',
        'url',
        'source_url',
        'activities',
        'activity_count',
        'date_created',
        'date_updated',
        'last_found_in_registry',
        'iati_standard_version',
        'note_count')


class DatasetDetail(RetrieveAPIView):
    """
    Returns detailed information about the dataset.

    ## URI Format

    ```
    /api/datasets/{ref}
    ```

    """
    queryset = IatiXmlSource.objects.all()
    serializer_class = DatasetSerializer

    fields = (
        'ref',
        'title',
        'type',
        'publisher',
        'url',
        'activities',
        'activity_count',
        'date_created',
        'date_updated',
        'last_found_in_registry',
        'iati_standard_version',
        'note_count',
        'notes')


class DatasetAggregations(AggregationView):
    """
    Returns aggregations based on the item grouped by, and the selected aggregation.

    ## Group by options

    API request has to include `group_by` parameter.
    
    This parameter controls result aggregations and
    can be one or more (comma separated values) of:

    - `dataset`
    - `publisher`
    

    ## Aggregation options

    API request has to include `aggregations` parameter.
    
    This parameter controls result aggregations and
    can be one or more (comma separated values) of:

    - `note_count` Indicator period target. Currently breaks on non number results.

    ## Request parameters

    All filters available on the Activity List, can be used on aggregations.

    """

    queryset = IatiXmlSource.objects.all()

    filter_backends = ( DjangoFilterBackend,)
    filter_class = DatasetFilter
    
    allowed_aggregations = (
        Aggregation(
            query_param='note_count',
            field='note_count',
            annotate=Count('iatixmlsourcenote__id'),
        ),
    )

    allowed_groupings = (
        GroupBy(
            query_param="dataset",
            fields=("id"),
            renamed_fields="dataset",
            queryset=IatiXmlSource.objects.all(),
            serializer=SimpleDatasetSerializer,
            serializer_main_field='id'
        ),
        GroupBy(
            query_param="publisher",
            fields=("publisher__org_id"),
            renamed_fields="publisher",
            queryset=Publisher.objects.all(),
            serializer=PublisherSerializer,
        ),
        GroupBy(
            query_param="exception_type",
            fields=("iatixmlsourcenote__exception_type"),
            renamed_fields="exception_type",
        ),
        GroupBy(
            query_param="field",
            fields=("iatixmlsourcenote__field"),
            renamed_fields="field",
        ),
    )

