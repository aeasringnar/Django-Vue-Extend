from django.db import models
from soft_delete_it.models import SoftDeleteModel
from base.models import BaseModel

class FlowGroup(SoftDeleteModel, BaseModel):
    name = models.CharField(max_length=255, verbose_name='审批组名称')

    class Meta:
        db_table = 'A_FlowGroup_Table'
        verbose_name = '审批组表'
        verbose_name_plural = verbose_name