---
layout: post
title: Redirecting HTTP to HTTPS with Node.js & Express on IBM Bluemix
date: '2014-09-05T19:23:00.001-05:00'
author: Tony Erwin
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
modified_time: '2014-09-15T00:51:29.325-05:00'
blogger_id: tag:blogger.com,1999:blog-5914472037415701789.post-8325991612350778889
blogger_orig_url: http://www.tonyerwin.com/2014/09/redirecting-http-to-https-with-nodejs.html
image:
    feature: "2014-09-05-redirecting-http-to-https-with-nodejs/Padlock-gold-small_with_label.png"
    thumb: "2014-09-05-redirecting-http-to-https-with-nodejs/Padlock-gold-small-72_with_label.png"
---

![Redirecting HTTP to HTTPS with Node.js on IBM Bluemix](/images/2014-09-05-redirecting-http-to-https-with-nodejs/Padlock-gold-small_with_label.png){: .paragraph-thumbnail }

Colleague <a href="https://twitter.com/jsloyer" target="_blank">Jeff Sloyer</a> points out in his recent blog post, <a href="https://developer.ibm.com/bluemix/2014/08/18/inbound-ssl-bluemix/" target="_blank"><em>Inbound SSL in Bluemix</em></a>, that an app using the default domain for <a href="https://www.bluemix.net/" target="_blank">IBM Bluemix</a> (which is `mybluemix.net`) gets SSL support automatically. This means without taking any other action, the app is accessible via `https` and traffic is secured by a fully trusted certificate provided by IBM. However, if not careful, your app will continue to be accessible via `http`, which completely bypasses SSL. In this post, I'll show code for a simple approach (which differs from Sloyer's) to make a <a href="http://nodejs.org/" target="_blank">Node.js</a> app redirect `http` requests to `https` by leveraging parts of the <a href="http://expressjs.com/" target="_blank">Express</a> web app framework. In addition, I'll touch on issues with custom domains that occur when using the built-in, default SSL certificate.

## Taking a Closer Look at Default Behavior

To show what happens "out-of-the-box", I've created an app in the Bluemix UI using the <a href="https://ace.ng.bluemix.net/#/store/cloudOEPaneId=store&amp;appTemplateGuid=nodejsHelloWorld" target="_blank">SDK for Node.js™</a> starter. You can access it for yourself via the links below (using either `http` or `https`):

- <a href="http://node-default.mybluemix.net/" target="_blank">http://node-default.mybluemix.net</a>
- <a href="https://node-default.mybluemix.net/" target="_blank">https://node-default.mybluemix.net</a>

In either case, you'll see a web page like the following:

[![Screenshot of Node.js Starter App](/images/2014-09-05-redirecting-http-to-https-with-nodejs/nodeStarterApp.png){: .center-image }](/images/2014-09-05-redirecting-http-to-https-with-nodejs/nodeStarterApp.png)

However, when you use `https`, notice that the browser shows a lock icon in the address bar. And, if you dig into the certificate details, you should see something like the following (which happens to be from Chrome):

[![Certificate info for mybluemix.net](/images/2014-09-05-redirecting-http-to-https-with-nodejs/mybluemixCertInfo.png){: .center-image }](/images/2014-09-05-redirecting-http-to-https-with-nodejs/mybluemixCertInfo.png)

This indicates that the certificate for `*.mybluemix.net` was issued by <a href="https://www.digicert.com/" target="_blank">DigiCert</a> and is trusted. You can rest assured the web site is coming from a server running on `mybluemix.net`, and the data is encrypted. On the other hand, if you use `http` there is no certificate info, and web traffic is unencrypted.

## Redirecting HTTP to HTTPS

<div class="tonySidebar">
    <h4>Where Will It Run?</h4>
    <div style="margin-bottom: 0px; margin-top: 5px;">While the Node.js app has been tested only on Bluemix, it should also run anywhere the app is sitting behind a reverse proxy. In particular, since Bluemix is a Platform-as-a-Service (PaaS) built on top of the <a href="http://www.cloudfoundry.org/" target="_blank">Cloud Foundry</a> open source framework, I'd expect the code to run without change in any other Cloud Foundry-based environment.
    </div>
</div>

If we want to guarantee all of our traffic uses SSL, we need to ensure `http` requests are redirected to `https`. I've written a small Node.js application demonstrating how to do this when running on Bluemix. The code makes use of the Express framework, and this really simplifies the work. The key components of the solution are:

- Enabling <a href="http://expressjs.com/api#app-settings" target="_blank">`trust proxy`</a> to turn on reverse proxy support
- Using <a href="http://expressjs.com/api#req.secure" target="_blank">`req.secure`</a> to determine if `http` or `https` was requested
    - NOTE: `req.secure` provides a shortcut to doing a string compare against <a href="http://expressjs.com/api#req.protocol" target="_blank">`req.protocol`</a>. The `req.protocol` flag is set by Express based on the `X-Forwarded-Proto` request header.

The full code listing is shown below. And, a complete package that can be deployed to Bluemix (including instructions on how to do so) is <a href="https://github.com/aerwin/https-redirect-demo" target="_blank">available on GitHub</a>.

<script src="http://gist-it.appspot.com/github.com/aerwin/https-redirect-demo/blob/master/server.js"></script>

You can access a live Bluemix deployment of the code with the URLs below (one using `http` and one using `https`):

- <a href="http://redirect-demo.mybluemix.net/" target="_blank">http://redirect-demo.mybluemix.net</a>
- <a href="https://redirect-demo.mybluemix.net/" target="_blank">https://redirect-demo.mybluemix.net</a>

In both cases, you should see a page like the one below (and using `https`):

[![Screenshot of HTTPS Redirect Demo](/images/2014-09-05-redirecting-http-to-https-with-nodejs/httpsRedirectDemo.png){: .center-image }](/images/2014-09-05-redirecting-http-to-https-with-nodejs/httpsRedirectDemo.png)

<h4>Alternative Approach: Inspect X-Forwarded-Proto</h4>

In my code, I enabled `trust proxy` and then left most of the work to the Express framework. A slightly lower-level, "long hand" approach is described by Sloyer in his previously mentioned post. His code example is illustrative as he manually inspects the `X-Forwarded-Proto` request header. This gives a sense of what's going on behind the scenes, and is especially useful if not using Express.

## What About Custom Domains?

To this point, I've only been talking about URL's using the default `mybluemix.net` domain. The reason is that if you use a <a href="https://www.ng.bluemix.net/docs/#manageapps/index-gentopic3.html#genTopProcId4" target="_blank">custom domain</a>, things don't come together quite as smoothly. You still technically get `https` for free, but the browser will complain about a domain mismatch after inspecting the certificate.

To allow you to easily see this for yourself, I've added a route to the `https-redirect-demo` app which uses the `tonyerwin.com` domain:

- <a href="http://redirect-demo.bluemix2.tonyerwin.com/" target="_blank">http://redirect-demo.bluemix2.tonyerwin.com</a>

If you follow that link, the redirect from `http` to `https` still occurs. But, your browser is going to tell you that you can't trust the identity of the site. For example, here's what I see in Chrome:

[![Security Warning in Chrome With Custom Domain](/images/2014-09-05-redirecting-http-to-https-with-nodejs/sslErrorWithCustomDomain_annotated.png){: .center-image }](/images/2014-09-05-redirecting-http-to-https-with-nodejs/sslErrorWithCustomDomain_annotated.png)

Basically, the same certificate that was present for the `*.mybluemix.net` domain is still being served, but its domain info doesn't match my `tonyerwin.com` custom domain. So, Chrome tells me I should probably stay clear and not continue.

Clearly, you wouldn't want this kind message appearing for your production apps. The only way to solve this problem is to upload an SSL certificate which matches `*.tonyerwin.com`. You can learn all about using your own SSL certificates in my post called <a target="_blank" href="http://www.tonyerwin.com/2014/09/bluemix-ui-ssl-certificates-and-custom.html"><i>Bluemix UI: SSL Certificates and Custom Domains</i></a>.

## Conclusion

In this post, you saw how both `http` and `https` is enabled for Bluemix apps using the default `mybluemix.net` domain. Then, you saw how a few lines of code in a Node.js app allows you to redirect all `http` requests to `https` (which then ensures data shared between your app and the user's browser is trusted and encrypted). Finally, you learned that more work is needed to avoid SSL certificate errors when using `https` with a custom domain. The additional work to upload your own SSL certificates will be the subject of a follow-up post in the near future.

_Updated, Sept. 15, 2014 to include link to my new post entitled "Bluemix UI: SSL Certificates and Custom Domains."_
