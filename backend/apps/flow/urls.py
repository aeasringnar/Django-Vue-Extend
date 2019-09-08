from flow.views import FlowGroupViewset, FlowUserViewset, 
# 审批组表管理
router.register(r'flowgroup', FlowGroupViewset, base_name='审批组表管理')
                
# 审批组子表管理
router.register(r'flowuser', FlowUserViewset, base_name='审批组子表管理')
                