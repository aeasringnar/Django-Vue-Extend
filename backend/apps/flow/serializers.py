
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from base.serializers import BaseModelSerializer
from rest_framework.utils import model_meta
import threading
from .models import *
import time
import datetime
from user.serializers import AddUserSerializer
                


# 新增 审批组 序列化器
class AddFlowGroupSerializer(serializers.ModelSerializer, BaseModelSerializer):
    class Meta:
        model = FlowGroup
        exclude = ('deleted',)

# 修改 审批组 序列化器
class UpdateFlowGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowGroup
        exclude = ('deleted',)

# 返回 审批组 序列化器
class ReturnFlowGroupSerializer(serializers.ModelSerializer):
    users = AddUserSerializer(many=True)
    class Meta:
        model = FlowGroup
        exclude = ('deleted',)
                


class ApprovalFlowUseFucSerializer(serializers.ModelSerializer, BaseModelSerializer):
    class Meta:
        model = ApprovalFlowFuc
        fields = ['flowfuc_grade','flow_group']


# 新增 审批设置 序列化器
class AddApprovalFlowSerializer(serializers.ModelSerializer, BaseModelSerializer):
    approval_flow_fucs = ApprovalFlowUseFucSerializer(many=True)

    class Meta:
        model = ApprovalFlow
        exclude = ('deleted',)
        validators = [UniqueTogetherValidator(queryset=ApprovalFlow.objects.all(), fields=['name',], message='该审批流已经存在')]

    def create(self, validated_data):
        func_datas = validated_data.pop('approval_flow_fucs')
        father = ApprovalFlow.objects.create(**validated_data)
        # 创建子的方法
        for item in func_datas:
            ApprovalFlowFuc.objects.create(approval_flow=father, **item)
        return father

    def update(self, instance, validated_data):
        if validated_data.get('approval_flow_fucs'):
            func_datas = validated_data.pop('approval_flow_fucs')
            # 修改时创建权限菜单的方法
            need_dels = ApprovalFlowFuc.objects.filter(approval_flow_id=instance.id)
            for item in need_dels:
                item.delete()
            for item in func_datas:
                # print('查看：', item)
                # print('查看id：', item.get('id'))
                ApprovalFlowFuc.objects.create(approval_flow=instance, **item)

        # 继承自父类的方法
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

# 修改 审批设置 序列化器
class UpdateApprovalFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalFlow
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
# 返回 审批设置 序列化器
class ReturnApprovalFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalFlow
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
                


# 新增 审批主体 序列化器
class AddFlowBodySerializer(serializers.ModelSerializer, BaseModelSerializer):
    class Meta:
        model = FlowBody
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
# 修改 审批主体 序列化器
class UpdateFlowBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowBody
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
# 返回 审批主体 序列化器
class ReturnFlowBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowBody
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
                