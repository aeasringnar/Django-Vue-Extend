from django.db import models
from soft_delete_it.models import SoftDeleteModel
from base.models import BaseModel
from user.models import User


class FlowGroup(SoftDeleteModel, BaseModel):
    name = models.CharField(max_length=255, verbose_name='审批组名称')
    users = models.ManyToManyField(User, verbose_name='组内用户', blank=True, related_name='flow_groups')

    class Meta:
        db_table = 'A_FlowGroup_Table'
        verbose_name = '审批组表'
        verbose_name_plural = verbose_name


class ApprovalFlow(SoftDeleteModel, BaseModel):
    name = models.CharField(max_length=255, verbose_name='审批名称')

    class Meta:
        db_table = 'A_ApprovalFlow_Table'
        verbose_name = '审批流设置主表'
        verbose_name_plural = verbose_name


class ApprovalFlowFuc(SoftDeleteModel, BaseModel):
    flowfuc_grade = models.IntegerField(default=1, verbose_name='审批级别')
    approval_flow = models.ForeignKey(ApprovalFlow, on_delete=models.PROTECT, verbose_name='所属审批流', related_name='approval_flow_fucs')
    flow_group = models.ForeignKey(FlowGroup, on_delete=models.PROTECT, null=True, blank=True, verbose_name='所属审批组')

    class Meta:
        db_table = 'A_ApprovalFlowFuc_Table'
        verbose_name = '审批流设置子表'
        verbose_name_plural = verbose_name


class ObjectFlow(SoftDeleteModel, BaseModel):
    name = models.CharField(max_length=255, verbose_name='审批名称')

    class Meta:
        db_table = 'A_ObjectFlow_Table'
        verbose_name = '项目中用审批表'
        verbose_name_plural = verbose_name


class ObjectFlowFuc(SoftDeleteModel, BaseModel):
    flowfuc_type_choices = (
        (0, '审批中'),
        (1, '已审批'),
        (2, '已驳回'),
        (3, '已撤回'),
    )
    flowfuc_grade = models.IntegerField(default=1, verbose_name='审批级别')
    flowfuc_type = models.IntegerField(default=0, choices=flowfuc_type_choices, verbose_name='审批结果')
    upper_flow_result = models.IntegerField(default=0, choices=flowfuc_type_choices, verbose_name='上级审批结果')
    object_flow = models.ForeignKey(ObjectFlow, on_delete=models.PROTECT, verbose_name='所属项目审批', related_name='object_flow_fucs')
    flow_group = models.ForeignKey(FlowGroup, on_delete=models.PROTECT, null=True, blank=True, verbose_name='所属审批组')

    class Meta:
        db_table = 'A_ObjectFlowFuc_Table'
        verbose_name = '项目中用审批子表'
        verbose_name_plural = verbose_name


class FlowBody(SoftDeleteModel, BaseModel):
    abstract = models.CharField(max_length=255, verbose_name='摘要')
    flow_file = models.CharField(max_length=255, null=True, blank=True, verbose_name='附件')
    object_flow = models.OneToOneField(ObjectFlow, on_delete=models.PROTECT, verbose_name='所属审批流', related_name='all_flows')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='用户')
    status_type_choices = (
        (0, '审批中'),
        (1, '已审批'),
        (2, '已驳回'),
        (3, '已撤回'),
    )
    status = models.IntegerField(default=0, choices=status_type_choices, verbose_name='审批结果')

    class Meta:
        db_table = 'A_FlowBody_Table'
        verbose_name = '被审批主体表'
        verbose_name_plural = verbose_name