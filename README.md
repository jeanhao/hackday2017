# HackDay Project API Reference


## 获取发布者联系方式
POST /user/message

### 请求参数
|参数      |说明                   |
|:-------|:--------------------|
|phone_num|手机号|
|nickname|昵称，发送短信的称呼|

### 返回参数


## 发布悬赏任务
POST /task/add

### 请求参数
| 参数 | 说明 |
|--------|--------|
|title|标题|
|detail|详情|
|money|金额|
|end_date|截止时间|
|pub_wxid|发布者微信id|

### 响应
| 参数 | 说明 |
|--------|--------|
|task_id|任务id|



