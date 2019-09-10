
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
                


# 审批组 ModelViewSet视图
class FlowGroupViewset(ModelViewSet):
    '''
    修改局部数据
    create:  创建审批组
    retrieve:  检索某个审批组
    update:  更新审批组
    destroy:  删除审批组
    list:  获取审批组列表
    '''
    queryset = FlowGroup.objects.all().order_by('-updated')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ReturnFlowGroupSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    # search_fields = ('name', )
    # filter_fields = ()
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
                


# 审批设置 ModelViewSet视图
class ApprovalFlowViewset(ModelViewSet):
    '''
    修改局部数据
    create:  创建审批设置
    retrieve:  检索某个审批设置
    update:  更新审批设置
    destroy:  删除审批设置
    list:  获取审批设置列表
    '''
    queryset = ApprovalFlow.objects.all().order_by('-updated')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ReturnApprovalFlowSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    # search_fields = ('name', )
    # filter_fields = ('flow_group', )
    ordering_fields = ('updated', 'sort_time', 'created',)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == 'create':
            return AddApprovalFlowSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return UpdateApprovalFlowSerializer
        return ReturnApprovalFlowSerializer

    def get_queryset(self):
        if bool(self.request.auth) and self.request.user.group_id == 1:
            return ApprovalFlow.objects.all().order_by('-updated')
        else:
            return ApprovalFlow.objects.filter(user_id=self.request.user.id).order_by('-updated')
                


# 审批主体 ModelViewSet视图
class FlowBodyViewset(ModelViewSet):
    '''
    修改局部数据
    create:  创建审批主体
    retrieve:  检索某个审批主体
    update:  更新审批主体
    destroy:  删除审批主体
    list:  获取审批主体列表
    '''
    queryset = FlowBody.objects.all().order_by('-updated')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ReturnFlowBodySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    # search_fields = ('abstract', 'content', )
    # filter_fields = ('user', 'object_flow', )
    ordering_fields = ('updated', 'sort_time', 'created',)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == 'create':
            return AddFlowBodySerializer
        if self.action == 'update' or self.action == 'partial_update':
            return UpdateFlowBodySerializer
        return ReturnFlowBodySerializer

    def get_queryset(self):
        if bool(self.request.auth) and self.request.user.group_id == 1:
            return FlowBody.objects.all().order_by('-updated')
        else:
            return FlowBody.objects.filter(user_id=self.request.user.id).order_by('-updated')
                