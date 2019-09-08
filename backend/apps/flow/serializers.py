
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueValidator
from base.serializers import BaseModelSerializer
from rest_framework.utils import model_meta
import threading
from .models import *
import time
import datetime
                

class FlowGroupUseFlowUserSerializer(serializers.ModelSerializer, BaseModelSerializer):
    class Meta:
        model = FlowUser
        exclude = ('deleted','flow_group',)


# 新增 审批组表 序列化器
class AddFlowGroupSerializer(serializers.ModelSerializer, BaseModelSerializer):
    class Meta:
        model = FlowGroup
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
# 修改 审批组表 序列化器
class UpdateFlowGroupSerializer(serializers.ModelSerializer, BaseModelSerializer):
    class Meta:
        model = FlowGroup
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
# 返回 审批组表 序列化器
class ReturnFlowGroupSerializer(serializers.ModelSerializer, BaseModelSerializer):
    flow_users = FlowGroupUseFlowUserSerializer(many=True, read_only=True)
    class Meta:

        model = FlowGroup
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
                


# 新增 审批组子表 序列化器
class AddFlowUserSerializer(serializers.ModelSerializer, BaseModelSerializer):
    class Meta:
        model = FlowUser
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
# 修改 审批组子表 序列化器
class UpdateFlowUserSerializer(serializers.ModelSerializer, BaseModelSerializer):
    class Meta:
        model = FlowUser
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
# 返回 审批组子表 序列化器
class ReturnFlowUserSerializer(serializers.ModelSerializer, BaseModelSerializer):
    flow_group = AddFlowGroupSerializer(many=True, read_only=True) # 以对象的方式返回 父级审批组
    class Meta:
        model = FlowUser
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
                

class TestManyToManySerializer(serializers.Serializer):
    flowuser = serializers.IntegerField()
    flowgroup = serializers.IntegerField()