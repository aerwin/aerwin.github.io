---
layout: post
title:  "IBM Cloud Console's Battle with Cookie Bloat on the Edge"
date: '2021-09-06T22:00:00.000-06:00'
author: Tony Erwin
description: "TODO"
tags:
- ibm cloud
- http cookies
- akamai
- edge platform
- performance
- nginx
- node.js
- kubernetes
- microservices
modified_time: '2021-09-06T22:00:00.000-06:00'
image:
    feature: "2021-09-06-ibm_cloud_console_cookies/console-cookie-monster.png"
---

# Introduction

If you're a web developer, you're no doubt familiar with cookies and have quite possibly encountered _cookie bloat_. I don't mean to imply that web developers are more prone than others to eat a lot of small, baked treats and to put on a few pounds. In this context, I referring to a set of [HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies){:target="_blank"} with large total size. Many kilobytes of cookies adds many kilobytes of HTTP headers passed along on any given HTTP request. This can lead to a couple different problems. In this post, I'll explain how we successfully handled some unique cookie bloat issues on my previous [IBM Cloud Console](https://cloud.ibm.com?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CookieBloatBattle){:target="_blank"} team using [Akamai](https://www.akamai.com/){:target="_blank"}.

As I was flying to Las Vegas today for a speaking engagement at [Akamai Edge World 2019](https://edgeworld.akamai.com/){:target="_blank"}, I thought I'd write about how the [IBM Cloud Console](https://cloud.ibm.com?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CookieBloatBattle){:target="_blank"} team has successfully used Akamai to win the battle against "cookie bloat." In this post, I'll explain:

- What I mean by cookie bloat
- How cookie bloat impacts performance and overloads proxies and web apps (like [NGINX](https://www.nginx.com/){:target="_blank"} and [Node.js](https://nodejs.org){:target="_blank"})
- How it occurs and steps to reduce it
- How we resolved our issues using a cookie whitelist on the edge

Hopefully, this information will be useful to many of you as you look to improve the performance and reliability of your own web applications.

 &nbsp;
[![IBM Cloud Console & Cookie Monster (Cookie Monster graphic courtesy of https://www.pngfind.com](/images/2021-09-06-ibm_cloud_console_cookies/console-cookie-monster.png){: .center-image }](/images/2021-09-06-ibm_cloud_console_cookies/console-cookie-monster.png)

# What is Cookie Bloat and Why Does It Matter?
Cookie bloat has nothing to do with weight gain from the kinds of cookies liked by the [Cookie Monster](https://en.wikipedia.org/wiki/Cookie_Monster){:target="_blank"}. Instead, it's referring to a set of [HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies){:target="_blank"} with large total size. Many kilobytes of cookies adds many kilobytes of HTTP headers passed along on any given HTTP request. This can lead to a couple different problems:

- Reduced network performance caused by passing extra bytes back and forth on every request. In his book [High Performance
Browser Networking](https://hpbn.co/){:target="_blank"}, author [Ilya Grigorik](https://twitter.com/igrigorik){:target="_blank"} talks about the importance of  
[eliminating unnecessary bytes](https://hpbn.co/optimizing-application-delivery/#eliminate-unnecessary-request-bytes){:target="_blank"}. HTTP/2 helps with header compression and by being able to identify a set of cookies with a key. But, as he points out, it doesn't eliminate the problem. 
- Diminished reliability as many proxies and app servers will fail when HTTP header size goes above 8192 bytes. I'll discuss NGINX and Node.js specifically below, but it's an issue that more generally occurs with other servers as well.

The first point is important, but it was the second point that finally drove us to find a solution. 

# How Does Cookie Bloat Impact NGINX?
As I've [described elsewhere](https://www.slideshare.net/tonyerwin/evolution-of-the-ibm-cloud-console-from-monolith-to-microservices-and-beyond){:target="_blank"}, the Console is composed of a complex distributed system of microservices that are hosted in a large number of clusters created with the [IBM Cloud Kubernetes Service](https://www.ibm.com/cloud/container-service?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CookieBloatBattle){:target="_blank"}. The front door to each of these Kube clusters is NGINX. The max header size allowed by NGINX is determined by the [`large_client_header_buffers`](http://nginx.org/en/docs/http/ngx_http_core_module.html#large_client_header_buffers){:target="_blank"} directive which defaults to 8192 bytes. If this limit is exceeded, NGINX will respond with a very frustrating `400 Bad Request – Request Header Or Cookie Too Large` error. Before implementing our solution, we were constantly trying to get teams owning all of the different proxies to override that directive.

# How Does Cookie Bloat Affect Node.js?
The vast majority of our microservices are written with Node.js. We were blindsided when Node 8.13 was released. All of the sudden microservices that had been inadvertently updated were dropping connections without any error messages. Once we finally realized the microservices had been upgraded, we found in the Node 8.13 release notes that a denial of service fix had been put in place capping the max allowed header size at 8192. This was obviously a breaking change for us and [others](https://github.com/nodejs/node/issues/24731){:target="_blank"}. Until we resolved the cookie bloat problem, we had to advise teams to stay on a back-level Node version.

In Node 8.15, a new [`--max-http-header-size`](https://nodejs.org/docs/latest-v8.x/api/cli.html#cli_max_http_header_size_size){:target="_blank"} param was added to override the default. But, just like with the NGINX configs, we didn't want to have to ask all of our Node app owners to set a higher value just to handle a lot of unneeded cookies. (NOTE: One caveat is that Node appears to include URL length in the calculation, so if you have particularly long URL's, you may still need to override `--max-http-header-size`.)
 
# What Causes Cookie Bloat?
The are a number of factors that lead to cookie bloat, including:

- **Many different teams sharing the same domain.** This has been one of our big issues. Any cookies set on the root domain are shared with domains using the root. So, for example, Console runs on `cloud.ibm.com` which shares the root `ibm.com` with all of the rest of IBM. So it's possible for any other app running on `ibm.com` (such as `www.ibm.com`) to set cookies that would eventually be sent to the Console. This makes it terribly difficult at times to know who is setting and using any given cookie. Deleting unknown cookies is likely to break someone else. This makes it important for apps to:
	- Set cookies on the most specific domain possible, rather than defaulting to the root.
	- Scope cookies to the most specific path possible. For example, if a cookie is only needed on the `/catalog` path of your app, then it should not be set on the the root (`\`) path.
- **Unneeded cookies.** This includes:
	- Cookies that none of your code still uses. If you don't explicitly delete them, they will last forever. So, it's important to set expiration times on all of your cookies.
	- Using cookies when better alternatives for your scenarios like the [Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API){:target="_blank"} can be used.
- **Individual cookies are too large.** When a cookie is legitimately needed, you should still be careful to consider how to represent your data in a size-efficient way.
- **Cookies only needed on the client.** Many marketing and analytics libraries set client side cookies that are really never needed on your backend but get sent there anyway.

You should definitely try to resolve any of the causes of cookie bloat mentioned above. But, even if you do, you may still have a bloat problem. That's the situation we found ourselves in. And, the reason we started working on a solution with Akamai.

# How Can Cookie Bloat Be Addressed On the Edge?
Akamai sits on the edge acting as a proxy for all requests to `cloud.ibm.com`. We decided to use Akamai to filter out any cookies we did not want to make it through to our origin. This was not a standard Akamai feature. But, as part of our professional service hours, the fine folks at Akamai created a self-service mechanism for us to create and modify our cookie whitelist. Any cookie not on the list is simply not passed along (behind the scenes Akamai rewrites the `Cookie` HTTP header if it contains non-whitelisted cookies).

 &nbsp;
[![IBM Cloud Console & Cookie Monster (Cookie Monster graphic courtesy of https://www.pngfind.com](/images/2021-09-06-ibm_cloud_console_cookies/akamai-proxy-for-console.png){: .center-image }](/images/2021-09-06-ibm_cloud_console_cookies/akamai-proxy-for-console.png)


Of course, we had to spend time doing some careful analysis and working with teams who contribute to `cloud.ibm.com` to ensure we had an accurate list so as to not break anyone. We chose a whitelisting approach as opposed to a blacklisting because:

1. It's far more future proof. Even if we could have identified a good initial set of cookies to block, as new cookies were created we'd have to keep updating the blacklist to block additional items. 
2. We wanted to have governance. Now anyone who wants to add a new cookie, must come to the console team and get approval to update the whitelist.

# How Effective Was the Akamai Solution?
- Example savings
     - Production
          - Cookie size on cloud.ibm.com = 6143 bytes (in browser dev tools)
          - Cookie size on server = 2945 bytes 
          - Savings  = 3198 bytes = 52.1%
          - Header size with all cookies = 7371
          - With only filtered cookies = 4173
          - Savings = 43.4% 
     - Test/staging
          -Cookie size on test.cloud.ibm.com (in broswer dev tools) = 9517
			- Cookie size on on server = 2845 
			- Savings = 6672 bytes = 70.1%
			- Header size with all cookies = 11080
			- With only filtered cookies = 2845
			- Savings = 60.2%
- Teams can now stop configuring NGINX and Node.js to accept large header sizes
- Other teams on ibm.com looking to use same approach now
- Akamai wants to promote solution to other companies


# Conclusion
The lessons apply whether using Akamai or another edge platform.

The net is battling cookies at the edge can be very useful in certain scenarios...

{: .button-link-container}
[Try Out the IBM Cloud Console!](https://cloud.ibm.com?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CookieBloatBattle){: .btn }{:target="_blank"}{: .center-text }

Finally, I'll finish up with a blatant plug for my engagements on June 13, 2019 at Akamai Edge World 2019 in Las Vegas:

- _Fireside Chat: Migrating Live Applications To A Microservice Architecture At IBM - Lessons Learned_ with [Marshall Lamb](https://www.linkedin.com/in/marshall-lamb){:target="_blank"} (IBM) and [Pavel Despot](https://www.linkedin.com/in/paveldespot/){:target="_blank"} (Akamai) at 11:00 am PDT. Come by and check it out if you're at the conference!
- Live video interview at 12:45 PM PDT on @Akamai TV with [Tara Bartley](https://www.linkedin.com/in/tarabartley){:target="_blank"} called _Big Blue's Front End to the Cloud_. Go to the [Akamai TV site](https://tv.akamai.com/config/browse/screen/home/){:target="_blank"} to check it out live, or to watch the recording later.
