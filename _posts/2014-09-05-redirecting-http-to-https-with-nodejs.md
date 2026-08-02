---
layout: post
title: Redirecting HTTP to HTTPS with Node.js & Express on IBM Bluemix
date: '2014-09-05T19:23:00.001-05:00'

description: "Both http and https is enabled for IBM Bluemix apps using the default mybluemix.net domain. Code is presented for a Node.js app that uses the Express web app framework to cause http requests to be redirected to https. This ensures data shared between your app and the user's browser is trusted and encrypted. A pointer to the deployable sample on GitHub is also provided."
tags:
- custom domain
- bluemix
- security
- ssl
- paas
- cloud foundry
- express
- https
- code samples
- ibm
- node.js
- github
categories: [Architecture]
modified_time: '2014-09-15T00:51:29.325-05:00'
blogger_id: tag:blogger.com,1999:blog-5914472037415701789.post-8325991612350778889
blogger_orig_url: http://www.tonyerwin.com/2014/09/redirecting-http-to-https-with-nodejs.html

image:
  path: "/images/2014-09-05-redirecting-http-to-https-with-nodejs/Padlock-gold-small-72_with_label.png"
  show: false
---

![Redirecting HTTP to HTTPS with Node.js on IBM Bluemix](/images/2014-09-05-redirecting-http-to-https-with-nodejs/Padlock-gold-small_with_label.png)

Colleague [Jeff Sloyer](https://twitter.com/jsloyer) points out in his recent blog post, *Inbound SSL in Bluemix* *(link no longer available)*, that an app using the default domain for IBM Bluemix (which is `mybluemix.net`) gets SSL support automatically. This means without taking any other action, the app is accessible via `https` and traffic is secured by a fully trusted certificate provided by IBM. However, if not careful, your app will continue to be accessible via `http`, which completely bypasses SSL. In this post, I'll show code for a simple approach (which differs from Sloyer's) to make a [Node.js](http://nodejs.org/) app redirect `http` requests to `https` by leveraging parts of the [Express](http://expressjs.com/) web app framework. In addition, I'll touch on issues with custom domains that occur when using the built-in, default SSL certificate.

## Taking a Closer Look at Default Behavior

To show what happens "out-of-the-box", I created a demo app in the Bluemix UI using the SDK for Node.js™ starter. The demo app is no longer running, but the screenshot below shows what you would have seen:

[![Screenshot of Node.js Starter App](/images/2014-09-05-redirecting-http-to-https-with-nodejs/nodeStarterApp.png)](/images/2014-09-05-redirecting-http-to-https-with-nodejs/nodeStarterApp.png)

However, when you use `https`, notice that the browser shows a lock icon in the address bar. And, if you dig into the certificate details, you should see something like the following (which happens to be from Chrome):

[![Certificate info for mybluemix.net](/images/2014-09-05-redirecting-http-to-https-with-nodejs/mybluemixCertInfo.png)](/images/2014-09-05-redirecting-http-to-https-with-nodejs/mybluemixCertInfo.png)

This indicates that the certificate for `*.mybluemix.net` was issued by [DigiCert](https://www.digicert.com/) and is trusted. You can rest assured the web site is coming from a server running on `mybluemix.net`, and the data is encrypted. On the other hand, if you use `http` there is no certificate info, and web traffic is unencrypted.

## Redirecting HTTP to HTTPS

<div class="tonySidebar">
    <h4>Where Will It Run?</h4>
    <div style="margin-bottom: 0px; margin-top: 5px;">While the Node.js app has been tested only on Bluemix, it should also run anywhere the app is sitting behind a reverse proxy. In particular, since Bluemix is a Platform-as-a-Service (PaaS) built on top of the [Cloud Foundry](https://www.cloudfoundry.org/) open source framework, I'd expect the code to run without change in any other Cloud Foundry-based environment.
    </div>
</div>

If we want to guarantee all of our traffic uses SSL, we need to ensure `http` requests are redirected to `https`. I've written a small Node.js application demonstrating how to do this when running on Bluemix. The code makes use of the Express framework, and this really simplifies the work. The key components of the solution are:

- Enabling [`trust proxy`](http://expressjs.com/api#app-settings) to turn on reverse proxy support
- Using [`req.secure`](http://expressjs.com/api#req.secure) to determine if `http` or `https` was requested
    - NOTE: `req.secure` provides a shortcut to doing a string compare against [`req.protocol`](http://expressjs.com/api#req.protocol). The `req.protocol` flag is set by Express based on the `X-Forwarded-Proto` request header.

The full code listing is shown below. And, a complete package that can be deployed to Bluemix (including instructions on how to do so) is [available on GitHub](https://github.com/aerwin/https-redirect-demo).

<script src="http://gist-it.appspot.com/github.com/aerwin/https-redirect-demo/blob/master/server.js"></script>

The screenshot below shows what the live Bluemix deployment of the code looked like _(demo app no longer running)_:

[![Screenshot of HTTPS Redirect Demo](/images/2014-09-05-redirecting-http-to-https-with-nodejs/httpsRedirectDemo.png)](/images/2014-09-05-redirecting-http-to-https-with-nodejs/httpsRedirectDemo.png)

<h4>Alternative Approach: Inspect X-Forwarded-Proto</h4>

In my code, I enabled `trust proxy` and then left most of the work to the Express framework. A slightly lower-level, "long hand" approach is described by Sloyer in his previously mentioned post. His code example is illustrative as he manually inspects the `X-Forwarded-Proto` request header. This gives a sense of what's going on behind the scenes, and is especially useful if not using Express.

## What About Custom Domains?

To this point, I've only been talking about URL's using the default `mybluemix.net` domain. The reason is that if you use a [custom domain](https://www.ng.bluemix.net/docs/#manageapps/index-gentopic3.html#genTopProcId4), things don't come together quite as smoothly. You still technically get `https` for free, but the browser will complain about a domain mismatch after inspecting the certificate.

To allow you to easily see this for yourself, I've added a route to the `https-redirect-demo` app which uses the `tonyerwin.com` domain:

- `http://redirect-demo.bluemix2.tonyerwin.com` _(demo app no longer running)_

If you follow that link, the redirect from `http` to `https` still occurs. But, your browser is going to tell you that you can't trust the identity of the site. For example, here's what I see in Chrome:

[![Security Warning in Chrome With Custom Domain](/images/2014-09-05-redirecting-http-to-https-with-nodejs/sslErrorWithCustomDomain_annotated.png)](/images/2014-09-05-redirecting-http-to-https-with-nodejs/sslErrorWithCustomDomain_annotated.png)

Basically, the same certificate that was present for the `*.mybluemix.net` domain is still being served, but its domain info doesn't match my `tonyerwin.com` custom domain. So, Chrome tells me I should probably stay clear and not continue.

Clearly, you wouldn't want this kind message appearing for your production apps. The only way to solve this problem is to upload an SSL certificate which matches `*.tonyerwin.com`. You can learn all about using your own SSL certificates in my post called [*Bluemix UI: SSL Certificates and Custom Domains*](https://www.tonyerwin.com/2014/09/bluemix-ui-ssl-certificates-and-custom.html).

## Conclusion

In this post, you saw how both `http` and `https` is enabled for Bluemix apps using the default `mybluemix.net` domain. Then, you saw how a few lines of code in a Node.js app allows you to redirect all `http` requests to `https` (which then ensures data shared between your app and the user's browser is trusted and encrypted). Finally, you learned that more work is needed to avoid SSL certificate errors when using `https` with a custom domain. The additional work to upload your own SSL certificates will be the subject of a follow-up post in the near future.

_Updated, Sept. 15, 2014 to include link to my new post entitled "Bluemix UI: SSL Certificates and Custom Domains."_
