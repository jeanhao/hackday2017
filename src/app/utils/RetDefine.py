# -*- coding: utf-8 -*-

class RetDefine():
    NO_ERR = 0  # 正常
    SYS_ERR = 1  # 系统出错
    REQUEST_INVALID = 2  # 请求不合法
    LACK_ARGS = 3  # 参数不足或名称有错
    SEND_ERROR = 4  # 短信发送失败

    VERIFY_CODE_NOT_EXIST = 50  # 验证码不存在
    VERIFY_CODE_ERROR = 51  # 验证码出错

    USER_NOT_EXIST = 101
    USER_NAME_USED = 102
    USERNAME_PASSWORD_NOT_MATCH = 103
    
    USER_NOT_LOGIN = 104
    USER_UNACTIVATE = 105
    PASSWORD_NOT_CHANGED = 106
#     EMAIL_USED = 102
#     EMAIL_NOT_REG = 103
#     EP_NOT_MATCH = 104
#     VER_CODE_ERR = 105
#     EMAIL_NOT_FOUND = 106
#     LEAVE_MSG_FAILED = 107
#
#     ADD_TASK_FAILED = 201
#     TASK_NOT_EXIST = 202
#     DELETE_TASK_FAILED = 203
#
#     REG_NOT_MATCH = 99

#     ret_message = {
#             NO_ERR:'Operate successfully',
#             SYS_ERR:'System error',
#             NO_LOGIN:'Not login',
#             LACK_ARGS:'Lack of parameters',
#             EMAIL_USED :'Email is used',
#             EMAIL_NOT_REG :'Email not register',
#             EP_NOT_MATCH : 'Email and password not match',
#             VER_CODE_ERR :'Verification code not match',
#             EMAIL_NOT_FOUND : 'email not found',
#             LEAVE_MSG_FAILED : 'leave message failed',
#             ADD_TASK_FAILED : 'Add task failed',
#             TASK_NOT_EXIST : 'Task not exist',
#             DELETE_TASK_FAILED :'delete task failed'
#         }
