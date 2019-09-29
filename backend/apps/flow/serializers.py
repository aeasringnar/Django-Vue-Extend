
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
        exclude = ('deleted',)

class ReturnApprovalFlowUseFucSerializer(serializers.ModelSerializer, BaseModelSerializer):
    flow_group = AddFlowGroupSerializer()
    class Meta:
        model = ApprovalFlowFuc
        fields = ['flowfuc_grade','flow_group']

# 返回 审批设置 序列化器
class ReturnApprovalFlowSerializer(serializers.ModelSerializer):
    approval_flow_fucs = ReturnApprovalFlowUseFucSerializer(many=True)
    class Meta:
        model = ApprovalFlow
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
                


# 新增 审批主体 序列化器
class AddFlowBodySerializer(serializers.ModelSerializer, BaseModelSerializer):
    approval_flow = serializers.IntegerField(label='审批流ID')
    class Meta:
        model = FlowBody
        exclude = ('deleted','object_flow','user',)
        validators = [UniqueTogetherValidator(queryset=FlowBody.objects.all(), fields=['abstract',], message='该摘要已经存在')]

    def validate(self, attrs):
        print('查看attrs',attrs)
        print('查看user：', self.context['request'].user)
        attrs['user'] = self.context['request'].user
        approval_flow = ApprovalFlow.objects.filter(id=attrs['approval_flow']).first()
        if not approval_flow:
            raise serializers.ValidationError("审批流不存在")
        appflow_fucs = ApprovalFlowFuc.objects.filter(approval_flow_id=approval_flow.id)
        objectflow = ObjectFlow(name=approval_flow.name)
        objectflow.save()
        attrs['object_flow'] = objectflow
        print('asd', attrs['object_flow'])
        for item in appflow_fucs:
            if item.flowfuc_grade == 1:
                ObjectFlowFuc(flowfuc_grade=item.flowfuc_grade,upper_flow_result=1,object_flow=attrs['object_flow'],flow_group=item.flow_group).save()
            else:
                ObjectFlowFuc(flowfuc_grade=item.flowfuc_grade,object_flow=attrs['object_flow'],flow_group=item.flow_group).save()
        del attrs['approval_flow']
        return attrs
    

class ObjectFlowFucSerializer(serializers.ModelSerializer):
    flow_group = AddFlowGroupSerializer()
    class Meta:
        model = ObjectFlowFuc
        exclude = ('deleted',) 
        # depth = 1


class ObjectFlowSerializer(serializers.ModelSerializer):
    object_flow_fucs = ObjectFlowFucSerializer(many=True)
    class Meta:
        model = ObjectFlow
        exclude = ('deleted',) 


# 修改 审批主体 序列化器
class UpdateFlowBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowBody
        exclude = ('deleted','object_flow','user',)

    def validate(self, attrs):
        print('查看attrs',attrs)
        print(attrs.get('status'))
        if self.instance.status == 3:
            raise serializers.ValidationError("已撤回，无法操作。")
        if attrs.get('status') and attrs.get('status') in [0, '0']:
            object_flow_fucs = ObjectFlowFuc.objects.filter(object_flow_id=self.instance.object_flow.id)
            for item in object_flow_fucs:
                item.flowfuc_type = 0
                if item.flowfuc_grade == 1:
                    item.upper_flow_result = 1
                else:
                    item.upper_flow_result = 0
                item.save()
        return attrs

# 返回 审批主体 序列化器
class ReturnFlowBodySerializer(serializers.ModelSerializer):
    object_flow = ObjectFlowSerializer()
    user = AddUserSerializer()
    class Meta:
        model = FlowBody
        exclude = ('deleted',) # or fields = '__all__' or fields = ['field01','field01',]
        # read_only_fields = ('field01', )
                