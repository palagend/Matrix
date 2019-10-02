---
title: Go语言源码分析
date: 2018-12-18T20:09:44+08:00
draft: false
categories:
- general
- 技术
---

## net/http
### client.go
结构: Client  
变量: DefaultClient  
接口: RoundTripper  
函数: //TODO  

`Client`指的是http客户端. 它的默认值是`DefaultClient`. 其中,  `DefaultClient`以`DefaultTransport`作为传输层的.

典型的客户端传输层, 其内部具有缓存的TCP连接, 所以客户端应该优先重用, 而不是重新创建. 使用`goroutines`可以实现安全的客户端并发请求.

`Client`是比`RoundTripper`(`Transport`只是`RounderTripper`的一个实现)更高一级的存在, 用来处理重定向、cookie等HTTP细节.

> • when forwarding sensitive headers like "Authorization",
> "WWW-Authenticate", and "Cookie" to untrusted targets.
> These headers will be ignored when following a redirect to a domain
> that is not a subdomain match or exact match of the initial domain.
> For example, a redirect from "foo.com" to either "foo.com" or "sub.foo.com"
> will forward the sensitive headers, but a redirect to "bar.com" will not.
>
> • when forwarding the "Cookie" header with a non-nil cookie Jar.
> Since each redirect may mutate the state of the cookie jar,
> a redirect may possibly alter a cookie set in the initial request.
> When forwarding the "Cookie" header, any mutated cookies will be omitted,
> with the expectation that the Jar will insert those mutated cookies
> with the updated values (assuming the origin matches).
> If Jar is nil, the initial cookies are forwarded without change.
