# NaiveMailScript
A naive mail script to download, forward, and delete emails

这个脚本用于在邮件客户端功能孱弱时进行邮件的批量下载、转发和删除

脚本使用pop3接收邮件并保存至本地，使用smtp发送邮件至指定邮箱

# How to use

#### 设置校园邮箱账号信息

在脚本开头填写校园邮箱的账号密码

```python
address = '@shanghaitech.edu.cn' # 校园邮箱账号
password = '' # 校园邮箱密码
```

#### 设置接受邮箱信息

在脚本开头填写接受邮箱的相关信息

`emai_user` 发送邮件的邮箱账户

`emai_recver` 接收邮件的邮箱账户（建议和发送账户填写相同的账户，即自己发给自己，否则可能会被拦截或者退信）

`emai_passwd`  发送邮件的邮箱账户授权码

`emai_server`  smtp邮箱服务器

其中授权码和服务器两项可以参考以下教程

#### 接受邮箱的配置

以网易163邮箱举例，从设置页面进入SMTP服务器设置

<img src="https://github.com/YzyParry/NaiveMailScript/blob/master/img/guide1.png" style="zoom:50%;" />

在设置中开启 POP3/SMTP 服务，这个页面一般会给出SMTP服务器地址，填写在`emai_server`中即可

<img src="https://github.com/YzyParry/NaiveMailScript/blob/master/img/guide2.png" style="zoom:50%;" />

可能需要手机发送短信进行验证

<img src="https://github.com/YzyParry/NaiveMailScript/blob/master/img/guide3.png" style="zoom:50%;" />

随即将获得的授权码填写在 `emai_passwd` 即可