from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueValidator
from base.serializers import BaseModelSerializer
from .models import *
import time
import datetime


# 登录view的表单验证
class LoginViewSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # test = serializers.DictField(child=serializers.CharField(required=True))

# 新增用户使用
class AddUserSerializer(serializers.ModelSerializer, BaseModelSerializer):

    class Meta:
        model = User
        exclude = ('deleted',)

# ReturnUserSerializer 使用的group序列化器
class UserUseGroupSerializer(serializers.ModelSerializer, BaseModelSerializer):

    class Meta:
        model = Group
        exclude = ('deleted',) 

# 新增权限菜单使用
class AddAuthPermissionSerializer(serializers.ModelSerializer, BaseModelSerializer):

    class Meta:
        model = AuthPermission
        exclude = ('deleted',)


# 新增权限菜单约束使用
class auth_permissions_ser(serializers.Serializer):
    object_name = serializers.CharField()
    object_name_cn = serializers.CharField()
    auth_list = serializers.NullBooleanField()
    auth_create = serializers.NullBooleanField()
    auth_update = serializers.NullBooleanField()
    auth_destroy = serializers.NullBooleanField()
# 新增权限使用
class AddAuthSerializer(serializers.ModelSerializer, BaseModelSerializer):
    auth_type = serializers.CharField(label="权限名称", help_text="权限名称", required=True, allow_blank=False,
                                       validators=[UniqueValidator(queryset=Group.all_objects.all(), message="该权限已经存在")])
    auth_permissions = auth_permissions_ser(many=True)

    class Meta:
        model = Auth
        exclude = ('deleted',)

    def validate(self, attrs):
        # 查看前端传来的所有数据
        print('查看attrs:', attrs)
        del attrs['auth_permissions']
        return attrs

# 返回权限使用
class ReturnAuthSerializer(serializers.ModelSerializer, BaseModelSerializer):
    auth_permissions = AddAuthPermissionSerializer(read_only=True, many=True)

    class Meta:
        model = Auth
        exclude = ('deleted',)


# 返回用户使用 userinfo 同时也试一把
class ReturnUserSerializer(serializers.ModelSerializer, BaseModelSerializer):
    group = UserUseGroupSerializer()
    auth = ReturnAuthSerializer()

    class Meta:
        model = User
        exclude = ('deleted', 'password',)