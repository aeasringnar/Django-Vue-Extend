
import uuid
import os
import requests
import json
import re
import time
import datetime
import random
import hashlib
import xml
import threading
from django.db.models import F, Q
from rest_framework import serializers, status, generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
# 官方JWT
# from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler ,jwt_response_payload_handler
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# 缓存配置
from django.core.cache import cache
# 自定义的JWT配置 公共插件
from utils.utils import jwt_decode_handler,jwt_encode_handler,jwt_payload_handler,jwt_payload_handler,jwt_response_payload_handler,google_otp,VisitThrottle,getDistance,NormalObj
from utils.jwtAuth import JWTAuthentication
from utils.pagination import Pagination
from utils.permissions import JWTAuthPermission, AllowAllPermission, BaseAuthPermission
from .models import *
from .serializers import *
# from .filters import *
from functools import reduce
from urllib.parse import unquote_plus
'''
serializers 常用字段
name = serializers.CharField(required=False, label='描述', max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
name = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
name = serializers.FloatField(max_value=None, min_value=None)
name = serializers.IntegerField(max_value=None, min_value=None)
name = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None)
name = serializers.DateField(format=api_settings.DATE_FORMAT, input_formats=None)
name = serializers.BooleanField()
name = serializers.ListField(child=serializers.IntegerField(min_value=0, max_value=100))
name = serializers.DictField(child=<A_FIELD_INSTANCE>, allow_empty=True)  DictField(child=CharField())
(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,generics.GenericAPIView,viewsets.GenericViewSet)
Q(name__icontains=keyword) 内部是like模糊搜索
__gt 大于 
__gte 大于等于
__lt 小于 
__lte 小于等于
__in 在某某范围内
is null / is not null 为空/非空
.exclude(age=10) 查询年龄不为10的数据
'''
                


# 审批组表 ModelViewSet视图
class FlowGroupViewset(ModelViewSet):
    '''
    修改局部数据
    create:  创建审批组表
    retrieve:  检索某个审批组表
    update:  更新审批组表
    destroy:  删除审批组表
    list:  获取审批组表列表
    '''
    queryset = FlowGroup.objects.all().order_by('-updated')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ReturnFlowGroupSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    # search_fields = ('field01', 'field02', 'field03',)
    # filter_fields = ('field01', 'field02', 'field03',)
    ordering_fields = ('updated', 'sort_time', 'created',)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == 'create':
            return AddFlowGroupSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return UpdateFlowGroupSerializer
        return ReturnFlowGroupSerializer

    def get_queryset(self):
        if bool(self.request.auth) and self.request.user.group_id == 1:
            return FlowGroup.objects.all().order_by('-updated')
        else:
            return FlowGroup.objects.filter(user_id=self.request.user.id).order_by('-updated')
                


# 审批组子表 ModelViewSet视图
class FlowUserViewset(ModelViewSet):
    '''
    修改局部数据
    create:  创建审批组子表
    retrieve:  检索某个审批组子表
    update:  更新审批组子表
    destroy:  删除审批组子表
    list:  获取审批组子表列表
    '''
    queryset = FlowUser.objects.all().order_by('-updated')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ReturnFlowUserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    # search_fields = ('field01', 'field02', 'field03',)
    # filter_fields = ('field01', 'field02', 'field03',)
    ordering_fields = ('updated', 'sort_time', 'created',)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == 'create':
            return AddFlowUserSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return UpdateFlowUserSerializer
        return ReturnFlowUserSerializer

    def get_queryset(self):
        if bool(self.request.auth) and self.request.user.group_id == 1:
            return FlowUser.objects.all().order_by('-updated')
        else:
            return FlowUser.objects.filter(user_id=self.request.user.id).order_by('-updated')



class TestManyToManyView(generics.GenericAPIView):
    serializer_class = TestManyToManySerializer
    def post(self, request):
        '''
        测试ManyToMany接口
        '''
        try:
            json_data = {"message": "ok", "errorCode": 0, "data": {}}
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": str(serializer.errors), "errorCode": 4, "data": {}})
            flowuser = serializer.data.get('flowuser')
            flowgroup = serializer.data.get('flowgroup')
            flowuser_obj = FlowUser.objects.filter(id=flowuser).first()
            flowgroup_obj = FlowGroup.objects.filter(id=flowgroup).first()
            print(flowuser_obj)
            if flowuser_obj:
                print('正向查找：通过fowuser找到所有flowgroup：')
                print(flowuser_obj.flow_group.all())
            if flowgroup_obj:
                print('正向查找：通过flowgroup找到所有fowuser：')
                print(flowgroup_obj.flow_users.all())
            return Response(json_data)
        except Exception as e:
            print('发生错误：',e)
            return Response({"message": "出现了无法预料的view视图错误：%s" % e, "errorCode": 1, "data": {}})



from drf_haystack.serializers import HaystackSerializer
from drf_haystack.viewsets import HaystackViewSet
from .search_indexes import FlowGroupIndex


class FlowGroupSerializer(HaystackSerializer):

    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [FlowGroupIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = [
            "name"
        ]


class FlowGroupSearchView(HaystackViewSet):

    # `index_models` is an optional list of which models you would like to include
    # in the search result. You might have several models indexed, and this provides
    # a way to filter out those of no interest for this particular view.
    # (Translates to `SearchQuerySet().models(*index_models)` behind the scenes.
    index_models = [FlowGroup]

    serializer_class = FlowGroupSerializer
                