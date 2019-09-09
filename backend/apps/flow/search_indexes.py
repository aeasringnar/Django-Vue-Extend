from django.utils import timezone
from haystack import indexes
# from .models import Location
from flow.models import FlowGroup,FlowUser
# class FlowGroupIndex(indexes.SearchIndex, indexes.Indexable):     # 类名必须为需要检索的Model_name+Index，这里需要检索Note，所以创建NoteIndex
#     text = indexes.CharField(document=True, use_template=True)  # 创建一个text字段
 
#     author = indexes.CharField(model_attr='user')   # 创建一个author字段
 
#     pub_date = indexes.DateTimeField(model_attr='pub_date')  # 创建一个pub_date字段
 
#     def get_model(self):          # 重载get_model方法，必须要有！
#         return FlowGroup
 
#     def index_queryset(self, using=None):   # 重载index_..函数
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())

class FlowGroupIndex(indexes.SearchIndex, indexes.Indexable):
    
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    # autocomplete = indexes.EdgeNgramField()
    # coordinates = indexes.LocationField(model_attr="coordinates")

    # @staticmethod
    # def prepare_autocomplete(obj):
    #     return " ".join((
    #         obj.name
    #     ))

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