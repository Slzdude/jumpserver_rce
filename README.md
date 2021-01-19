# jumpserver_rce

根据官方报告，这个漏洞的影响版本如下:

```
< v2.6.2
< v2.5.4
< v2.4.5
= v1.5.9
```

经过测试v1.5.8的Koko无法进行利用，因为它在创建WebSocket连接之后对用户身份进行了鉴权，具体代码看：[https://github.com/jumpserver/koko/blob/44d519b40110d208874c147a4c05f267aa75cf95/pkg/httpd/wsmanager.go#L53](https://github.com/jumpserver/koko/blob/44d519b40110d208874c147a4c05f267aa75cf95/pkg/httpd/wsmanager.go#L53)

## 判断JumpServer的版本

有个比较简单的办法，就是访问/luna/页面的js进行提取，具体实现放在了`luna_version.py`中

## 有限的文件读取漏洞

限制主要如下

- 只能读取以 log 结尾的文件

首先需要使用`readlog.py`读取日志文件，看其中有没有必要的信息

主要是三个信息

- user id
- asset id
- system user id

这三个 ID 都是自动生成的 UUID，没法进行遍历

如果jumpserver的日志目录等级是 INFO，拿到的信息就很少了

可以利用这个漏洞去读取一些系统上其它的日志，看看有没有什么价值

## 任意命令执行漏洞

在获取到上面讲的三个 ID 之后，填充到`rce.py`中，即可进行全交互式的命令执行

话说回来，拿不到三个 ID 就没价值

## 私钥读取

在权限足够的账号下，可以读取缓存中存储的系统私钥，但是要求的权限太高了，本来就可以为所欲为了

```
http://localhost/api/v1/authentication/connection-token/?token=_SETTING_TERMINAL_HOST_KEY
```
