# HackDay Project API Reference

```python
全局状态码：
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
```


## 发送验证码
POST /api/user/message

### 请求参数
|参数      |说明                   |
|:-------|:--------------------|
|phone_num|手机号|
~~|nickname|昵称，发送短信的称呼|~~

### 响应示例
{
  "status": 0
}

## 用户注册
POST /api/user/register

### 请求参数
|参数      |说明     |
|:-------|:------|
|phone_num   |手机号     |
|password  |密码     |
|nickname   |昵称     |
|verify_code|验证码|

### 响应示例
{
  "status": 0
}

## 用户登陆
POST /api/user/login

### 请求参数
|参数      |说明     |
|:-------|:------|
|phone_num   |手机号     |
|password  |密码     |

### 响应示例
{
  "status": 0
}



