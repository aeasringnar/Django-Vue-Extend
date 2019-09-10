from django.utils import timezone
from haystack import indexes
from flow.models import FlowGroup,FlowUser


class FlowGroupIndex(indexes.SearchIndex, indexes.Indexable):
    
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return FlowGroup

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class FlowUserIndex(indexes.SearchIndex, indexes.Indexable):
    
    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr="name")

    def get_model(self):
        return FlowUser

    def index_queryset(self, using=None):
        return self.get_model().objects.all()