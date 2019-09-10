from flow.views import FlowGroupViewset, ApprovalFlowViewset, FlowBodyViewset, 
# 审批组管理
router.register(r'flowgroup', FlowGroupViewset, base_name='审批组管理')
                
# 审批设置管理
router.register(r'approvalflow', ApprovalFlowViewset, base_name='审批设置管理')
                
# 审批主体管理
router.register(r'flowbody', FlowBodyViewset, base_name='审批主体管理')
                