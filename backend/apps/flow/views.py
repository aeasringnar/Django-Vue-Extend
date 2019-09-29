
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
from django.db import transaction
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
    queryset = FlowGroup.objects.all().order_by('-update_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ReturnFlowGroupSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('name', )
    # filter_fields = ()
    ordering_fields = ('update_time', 'sort_time', 'create_time',)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == 'create':
            return AddFlowGroupSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return UpdateFlowGroupSerializer
        return ReturnFlowGroupSerializer

    def get_queryset(self):
        if bool(self.request.auth) and self.request.user.group_id == 1:
            return FlowGroup.objects.all().order_by('-update_time')
        elif bool(self.request.auth):
            return FlowGroup.objects.filter().order_by('-update_time')
        else:
            return FlowGroup.objects.filter(id=0).order_by('-update_time')


# 审批组 ModelViewSet视图
class FlowGroupListViewset(mixins.RetrieveModelMixin,mixins.ListModelMixin,GenericViewSet):
    '''
    create:  创建审批组
    retrieve:  检索某个审批组
    list:  获取审批组列表
    '''
    queryset = FlowGroup.objects.all().order_by('-update_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [JWTAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ReturnFlowGroupSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('name', )
    # filter_fields = ()
    ordering_fields = ('update_time', 'sort_time', 'create_time',)
    pagination_class = Pagination
                

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
    queryset = ApprovalFlow.objects.all().order_by('-update_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ReturnApprovalFlowSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('name', )
    # filter_fields = ('flow_group', )
    ordering_fields = ('update_time', 'sort_time', 'create_time',)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return AddApprovalFlowSerializer
        return ReturnApprovalFlowSerializer   


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
    queryset = FlowBody.objects.all().order_by('-update_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ReturnFlowBodySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('abstract', 'content', )
    filter_fields = ('user', 'object_flow__name', )
    ordering_fields = ('update_time', 'sort_time', 'create_time',)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == 'create':
            return AddFlowBodySerializer
        if self.action == 'update' or self.action == 'partial_update':
            return UpdateFlowBodySerializer
        return ReturnFlowBodySerializer

    def get_queryset(self):
        if bool(self.request.auth) and self.request.user.group_id == 1:
            return FlowBody.objects.all().order_by('-update_time')
        elif bool(self.request.auth):
            return FlowBody.objects.filter(user_id=self.request.user.id).order_by('-update_time')
        else:
            return FlowBody.objects.filter(id=0).order_by('-update_time')  

    def create(self, request, *args, **kwargs):
        print('查看data：', request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        flowbody = FlowBody.objects.filter(abstract=request.data.get('abstract')).first()
        json_data = ReturnFlowBodySerializer(flowbody).data
        return Response(json_data, status=status.HTTP_201_CREATED)


# 返回所有我需要审批的审批主体
class FlowBodyNeedFlowViewset(mixins.RetrieveModelMixin,mixins.ListModelMixin,GenericViewSet):
    '''
    retrieve:  检索某个审批主体
    list:  获取审批主体列表
    '''
    queryset = FlowBody.objects.all().order_by('-update_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [JWTAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ReturnFlowBodySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('abstract', 'content', )
    filter_fields = ('user', 'object_flow', )
    ordering_fields = ('update_time', 'sort_time', 'create_time',)
    pagination_class = Pagination

    def get_queryset(self):
        if bool(self.request.auth):
            # 反向查找出用户所在的flowgroup
            all_flowgroup_ids = [item.id for item in self.request.user.flow_groups.all()]
            all_obj_flow_ids = [item.object_flow_id for item in ObjectFlowFuc.objects.filter(flow_group_id__in=all_flowgroup_ids)]
            return FlowBody.objects.filter(object_flow_id__in=all_obj_flow_ids).order_by('-update_time')
        else:
            return FlowBody.objects.filter(id=0).order_by('-update_time')  


class ObjectFlowViewSerializer(serializers.Serializer):
    # 审批接口使用
    id = serializers.IntegerField() # 审批的ID
    flowfuc_type = serializers.IntegerField() # 审批标志 1：通过；2：驳回


class ObjectFlowView(generics.GenericAPIView):
    serializer_class = ObjectFlowViewSerializer
    authentication_classes = (JWTAuthentication,)

    @transaction.atomic
    def patch(self, request):
        '''
        审批
        '''
        try:
            if not request.auth:
                return Response({"message": "请先登录", "errorCode": 2, "data": {}})
            print('group_id:', request.user.group.id)
            print('user_id:', request.user.id)
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": str(serializer.errors), "errorCode": 4, "data": {}})
            flow_fuc_id = serializer.data.get('id')
            flowfuc_type = serializer.data.get('flowfuc_type')
            json_data = {"message": '审批成功' if flowfuc_type == 1 else '驳回成功', "errorCode": 0, "data": {}}
            # 找到需要审批的审批日志记录
            print('查看用户的flow_groups：', request.user.flow_groups.all())
            object_flow_fuc = ObjectFlowFuc.objects.filter(flow_group_id__in=[item.id for item in request.user.flow_groups.all()], id=flow_fuc_id).first()
            print(object_flow_fuc)
            # 没有对应数据时报错
            if not object_flow_fuc:
                return Response({"message": "未找到属于当前用户的该审批流", "errorCode": 1, "data": {}})
            top_flow_obj = FlowBody.objects.filter(object_flow_id=object_flow_fuc.object_flow.id).first()
            if top_flow_obj.status in [1,2]:
                return Response({"message": "当前审批主体已审批，无需重复审批。", "errorCode": 1, "data": {}})
            if top_flow_obj.status in [3]:
                return Response({"message": "当前审批主体已撤回，无法审批。", "errorCode": 1, "data": {}})
            # 存在时 改状态
            object_flow_fuc.flowfuc_type = flowfuc_type
            object_flow_fuc.save()
            # 找到排序后的全部审批流
            object_flow_fucs = ObjectFlowFuc.objects.filter(object_flow_id=object_flow_fuc.object_flow.id).order_by('flowfuc_grade')
            # 找到归属审批流名称
            flow_type_name = object_flow_fuc.object_flow.name
            # 当这是最后一级审批时
            if object_flow_fucs.last().id == flow_fuc_id:
                top_flow_obj.status = flowfuc_type
                top_flow_obj.save()
            else:
                # 找到下一级的审批流
                next_object_flow_fuc = ObjectFlowFuc.objects.filter(object_flow_id=object_flow_fuc.object_flow.id, flowfuc_grade=(object_flow_fuc.flowfuc_grade + 1)).first()
                print(next_object_flow_fuc)
                # 修改下一级审批里的上级审批意见
                next_object_flow_fuc.upper_flow_result = flowfuc_type
                next_object_flow_fuc.save()
                if flowfuc_type in [2, '2']:
                    top_flow_obj.status = flowfuc_type
                    top_flow_obj.save()
            return Response(json_data)
        except Exception as e:
            print('发生错误：',e)
            return Response({"message": "出现了无法预料的view视图错误：%s" % e, "errorCode": 1, "data": {}})