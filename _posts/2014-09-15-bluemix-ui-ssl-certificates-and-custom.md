---
layout: post
title: 'Bluemix UI: SSL Certificates and Custom Domains'
date: '2014-09-15T00:40:00.000-05:00'
author: Tony Erwin
description: "Previously, I described how you automatically get basic SSL support in IBM Bluemix if you use the default domain for your apps. However, if you use a custom domain, you'll get a domain mismatch error when using https. In this post, I'll show you how to fix this by associating your SSL certificate with a custom domain. Along the way, you'll learn how add a custom domain, setup an app to use your domain, configure DNS for your domain, and finally upload an SSL certificate for your domain."
tags:
- custom domain
- bluemix
- bluemix ui
- dns
- security
- paas
- ssl certificate
- cloud
- cloud foundry
- ibm
- node.js
- user interface
modified_time: '2016-07-29T22:23:13.710-05:00'
blogger_id: tag:blogger.com,1999:blog-5914472037415701789.post-8278641163248189864
blogger_orig_url: http://www.tonyerwin.com/2014/09/bluemix-ui-ssl-certificates-and-custom.html
image:
    feature: "2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL6_nohead_annotated.png"
    thumb: "2014-09-15-bluemix-ui-ssl-certificates-and-custom/Padlock-gold-small-72_with_label.png"
---

![Bluemix UI: SSL Certificates for Custom Domains](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/mime-certificate300_withLabel.png){: .paragraph-thumbnail }

In my previous post [_Redirecting HTTP to HTTPS with Node.js &amp; Express on IBM Bluemix_](https://www.tonyerwin.com/2014/09/redirecting-http-to-https-with-nodejs.html){:target="_blank"}, I described how you automatically get basic SSL support if you use the default domain when configuring your apps to run on [IBM Bluemix](https://www.bluemix.net/){:target="_blank"}. However, if you use a custom domain, you'll get domain mismatch errors in the browser. These errors are ugly and likely to scare away users. In this post, I'll show you how to fix this problem by associating your own SSL certificate with your custom domain. This new functionality went live in the [August 2014 refresh](https://www.tonyerwin.com/2014/09/bluemix-ui-updates-august-2014.html){:target="_blank"} of the Bluemix UI. Along the way, you'll learn how to do the following:

1. [Add a custom domain.](#AddCustomDomain)
2. [Setup an app to use the custom domain.](#CreateAppUsingCustomDomain)
3. [Configure DNS so traffic is routed to your app.](#ConfigureDNS)
4. [Upload an SSL certificate for your domain.](#UploadAnSSLCertificate) _**NOTE:** There is a limit of one upload per organization for trial users and four uploads per organization for pay-as-you-go and subscription users (updated Dec. 7, 2014)._

## Prerequisites

Before we get into the more fun part of the post, let's cover some important prerequisites that will make things go more smoothly along the way. In particular, you will need to:

1. Have (or acquire) ownership of a registered Internet domain name
2. Obtain (or create) an SSL certificate, private key, and (optionally) an intermediate certificate

I'll say more about these requirements in the next couple of sections.

### Registered Domain Name

We will be creating a custom domain in Bluemix, and for it to function properly, you will need to own the domain name that you plan to use. In addition, it must be registered with a [DNS hosting service](http://en.wikipedia.org/wiki/DNS_hosting_service){:target="_blank"} that allows you to make configuration changes. For example, I own the `tonyerwin.com` domain (which points at the blog you're reading right now) and use [GoDaddy](https://www.godaddy.com/){:target="_blank"} for DNS hosting. (NOTE: GoDaddy is just one of many [suitable providers](http://www.digitaltrends.com/computing/best-domain-name-registrars/){:target="_blank"}.)

[![GoDaddy Domain Dashboard](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/dnsHostingProviderDashboard.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/dnsHostingProviderDashboard.png)

Even if you don't own a domain or have access to your DNS provider, you can still explore the functionality in this article. But, you will have to edit your `hosts` file. I'll say a little more about that option later on in the <a href="#ConfigureDNS">_Configuring DNS for Custom Domains_</a> section.

### SSL Certificates

<div class="tonySidebar">
    <h4>What If I Don't Have a Certificate?</h4>
    <div style="margin-bottom: 0px; margin-top: 5px;">So, you want to try this cool feature out, but you're not ready to purchase a certificate from a certificate authority? If so, self-signed certificates could be a good option for you. While not appropriate for production apps, they do have a place during development. Check out my companion post which describes three different ways to create self-signed certificates: <a target="_blank" href="https://www.tonyerwin.com/2014/09/generating-self-signed-ssl-certificates.html"><i>Generating Self-Signed SSL Certificates for Use with Bluemix Custom Domains</i></a>.
    </div>
</div>

When it comes time to associate a certificate with your domain, you will need the following files with the noted attributes:

- **Certificate**
    - Digital document that binds a public key to the identity of the certificate owner, thereby enabling the certificate owner to be authenticated.
    - Generally issued and signed by a [certificate authority](http://www.sslshopper.com/certificate-authority-reviews.html){:target="_blank"}. However, for testing and development purposes you may use a [self-signed certificate](http://www.sslshopper.com/article-when-are-self-signed-certificates-acceptable.html){:target="_blank"}.
    - File types supported:
        - PEM (`.pem`, `.crt`, `.cer`, and `.cert`)
        - DER (`.der` or `.cer` )
        - PKCS #7 (`.p7b`, `.p7r`, `.spc`)
            - Limitation: Bluemix supports only one certificate per file. That is, you cannot bundle a certificate and intermediate certificate into one PKCS #7 bundle.
- **Private key**
     - Algorithmic pattern used to encrypt messages that only the corresponding public key can decrypt. The private key is also used to decrypt messages that were encrypted by the corresponding public key.
     - File types supported:
          - PEM (`.pem`, `.key`)
          - PKCS #8 (`.p8`, `.pk8`)
- **Intermediate certificate**
    - You should use an intermediate certificate to verify the authenticity of the main certificate. Intermediate certificates are typically obtained from a trusted third-party. You might not require an intermediate certificate if using a self-signed certificate for testing your application prior to deploying it to production.

See the [_Securing Apps_](https://www.ng.bluemix.net/docs/#manageapps/index-gentopic4.html){:target="_blank"} article in the [Bluemix Documentation](https://www.ng.bluemix.net/docs){:target="_blank"} for the most current information on supported certificate types.

<h2 id="AddCustomDomain">Adding a Custom Domain</h2>

<div class="tonySidebar">
    <h4>What If I Already Have a Custom Domain?</h4>
    <div style="margin-bottom: 0px; margin-top: 5px;">You may already have a custom domain configured for Bluemix. If so, great! But, please pay attention to the upcoming section on <a href="#ConfigureDNS"><i>Configuring DNS for Custom Domains</i></a> as there are some special DNS setup considerations for SSL.
    </div>
</div>

Now that we have the prerequisites out of the way, let's start by adding a custom domain via the Bluemix UI. (NOTE: You can also create domains with the [`cf` command line tool](http://docs.cloudfoundry.org/devguide/deploy-apps/domains-routes.html){:target="_blank"}.)

1. Log in to the <a target="_blank" href="https://www.bluemix.net">Bluemix UI</a>.
2. In the banner, open the _Organizations_ menu and choose **Manage Organizations**.

[![Bluemix UI: Select Manage Organizations from Banner](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/manageOrganizationsBanner_annotated.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/manageOrganizationsBanner_annotated.png)

{:start="3"}
3. In the _Manage Organizations_ pane, make sure your organization is selected in the tree on the left side. Then, click **Domains** to view the custom domains for your organization.

[![Bluemix UI: Manage Organizations Top-Level](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/manageOrganizationsTopLevel_annotated.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/manageOrganizationsTopLevel_annotated.png)

{:start="4"}
4. On the _Domains_ tab, click the **Add Domain** button.

[![Bluemix UI: Manage Domains](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL1_nohead_annotated.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL1_nohead_annotated.png)

{:start="5"}
5. Enter your custom domain in the text box in the newly added row. As mentioned earlier, this should be a domain that you own and that is registered with a DNS hosting service. For my custom domain, I own the `tonyerwin.com` domain, and I want to use the `bluemix.tonyerwin.com` domain for my demo apps that will be deployed to Bluemix.

[![Bluemix UI: Adding Custom Domain](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL2_nohead.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL2_nohead.png)

{:start="6"}
6. Click the **Save** button. After the save operation completes, you should notice a new icon in the _SSL Certificate_ column. We'll come back to it later, but clicking this icon is how you would start the process of uploading a certificate for your domain.

[![Bluemix UI: Custom Domain Added](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL3_nohead_annotated.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL3_nohead_annotated.png)

<h2 id="CreateAppUsingCustomDomain">Using a Custom Domain in an App</h2>

Now, that we have a custom domain, let's setup an app that makes use of it. We can either create a brand new app or edit the routes of an existing app. And, in the rest of this section, I'll walk you through both paths.

### Creating a New App With a Custom Domain

If you want to create a brand new app, do the following:

1. Click on the Catalog in the Bluemix UI banner.
2. In the _Starters_ section, click on one of the runtimes like Liberty for Java™, SDK for Node.js™, Ruby on Rails, or Ruby Sinatra.
3. On the details page for the selected runtime:
    - Enter a `Name` for your application.
    - Optionally change the default `Host`.
    - From the `Domain` pulldown, select your custom domain.

[![Creating Starter App With Custom Domain](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL0_createApp_annotated.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL0_createApp_annotated.png)

{:start="4"}
4. Click the `Create` button to create your app. After creation, you will be taken to the _App Details_ view of your new app.

### Editing Routes of an Existing App to Use a Custom Domain

If you prefer to edit the route of the existing app, follow the steps below:

1. Go to the App Details view for your app. If you created your app in the last section, you're probably already there. Otherwise, find your app in the Dashboard and click on it.

[![Bluemix UI: App Details Showing Same App With Gear Menu](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/sslDemoAppDetailsWithMenu.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/sslDemoAppDetailsWithMenu.png)

{:start="2"}
2. Open the "gear" menu in the upper right hand corner of the App Details view, and choose the `Edit Routes` menu item.
3. In the Edit Routes dialog, you can add and remove routes. In addition, each route offers a pulldown that includes all available domains and allows you to choose any of your custom domains.

[![Edit Route Dialog Before SSL Cert Upload](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL0_editRouteNoSSL_annotated.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL0_editRouteNoSSL_annotated.png)

{:start="4"}
4. Notice in the screen shot above that my app has one route, `ssl-demo.bluemix.tonyerwin.com`. Also, note that the SSL status icon to the right of the route shows an open padlock. This indicates we have not yet uploaded an SSL certificate for the route's domain.

<h2 id="ConfigureDNS">Configuring DNS for Custom Domains</h2>

<div class="tonySidebar">
    <h4>What if I Don't Own a Domain?</h4>
    <div style="margin-bottom: 0px; margin-top: 5px;">You may still wish to experiment with this functionality even if you don't own a domain or have access to your DNS provider. An option for you would be to edit your <a target="_blank" href="http://en.wikipedia.org/wiki/Hosts_(file)">`hosts` file</a>. The mechanism for doing this will depend on your operating system, but in the end you'll want to add an entry like one of the following for your app's route:<br />

<pre>
# For an app running in Dallas 
# (ip from running nslookup on
#  secure.us-south.bluemix.net)
75.126.81.68 www.example.com
</pre>

    OR<br />

<pre># For an app running in London
# (ip from running nslookup on
#  on secure.eu-gb.bluemix.net)
5.10.124.142 www.example.com</pre>

    OR<br />

<pre># For an app running in Sydney
# (ip from running nslookup on
#  secure.au-syd.bluemix.net)
168.1.35.166 www.example.com</pre>
    </div>
</div>

At this point, we have an app using a route making use of our custom domain. However, if you tried to access your app via the route, it would fail. To resolve this, you need to do some DNS configuration. Specifically, you need to add a `CNAME` record that maps your domain to the hostname of the Bluemix router. Since we plan to use our own SSL certificates, the hostname we want to reference is `secure.us-south.bluemix.net`. NOTE: The host to use varies by the region your app is hosted in:

- US South: `secure.us-south.bluemix.net`
- US Easty: `secure.us-east.bluemix.net`
- London: `secure.eu-gb.bluemix.net`
- Frankfurt: `secure.eu-de.bluemix.net`
- Sydney: `secure.au-syd.bluemix.net`

The mechanism for adding a `CNAME` record is going to vary depending on your provider. For GoDaddy, it's rather simple. I go to the `DNS Management` configuration page for my `tonyerwin.com` domain. From there, I click the `Add` button. This brings up a panel like the one in the screenshot below. On it, I've set `Type` to _CNAME_, the `Host` to `*.bluemix` (the `tonyerwin.com` part is assumed), and `Points to` to `secure.us-south.bluemix.net`.

[![GoDaddy Add Record Dialog](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/goDaddyAddRecord.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/goDaddyAddRecord.png)

If you don't use GoDaddy, you should still find a similar mechanism from your provider. Once you commit these kinds of changes, you will have to wait some period of time for the changes to propagate. Once they do, you should be able to access your app via the browser.

If you're still unable to access your app after a reasonable amount of time, you might find it helpful to run `nslookup`. For example, I ran it below for `ssl-demo.bluemix.tonyerwin.com`, and it properly resolved to `secure.us-south.bluemix.net`.

```
$ nslookup ssl-demo.bluemix.tonyerwin.com
Server:  192.168.1.1
Address: 192.168.1.1#53

Non-authoritative answer: ssl-demo.bluemix.tonyerwin.com canonical name = secure.us-south.bluemix.net.
Name: secure.us-south.bluemix.net
Address: 75.126.81.68
```

<h2 id="UploadAnSSLCertificate">Uploading a Certificate for Your Domain</h2>

### Revisiting the Need for Your Own Certificate

We're now at a point where you can access your app in the browser using a route that includes your custom domain. But, if you try to access it using the `https` protocol, you'll get a browser warning. You can try this for yourself using the link to one of my apps below:

- [https://ssl-demo.bluemix2.tonyerwin.com](https://ssl-demo.bluemix2.tonyerwin.com/){:target="_blank"}

If you follow that link, your browser is going to report that you can't trust the identity of the server because it identifies itself as `*.mybluemix.net` rather than the domain in the URL. For example, here's what I see in Chrome:

[![Security Warning in Chrome With Custom Domain](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/chromeWarningForBluemix2.png){: .center-image }{:style="max-height: 400px;"}](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/chromeWarningForBluemix2.png)

So, this finally brings us to the main point of this post &mdash; namely, eliminating that server mismatch by using your own certificate. 

### Time to Upload!

With that, let's walkthrough the steps to upload your files (certificate, private key, and optional intermediate certificate) that you collected as part of the prerequisites:

1. Go back to the _Manage Domains_ tab where you first defined your custom domain.
2. Find your domain in the table and click the `Upload Certificate` icon in the _SSL Certificate_ column. Recall I pointed out this icon when you first created your custom domain.
3. For each field on the Upload Certificate dialog, click the `Choose` button and select the appropriate file.

[![Bluemix UI: Upload Certificate Dialog (Populated)](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL5.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL5.png)

{:start="4"}
4. Click the `Upload` button and the upload process should begin. Once the upload is complete, the dialog will disappear and you will be taken back to the _Manage Domains_ table. And, you should also see the icon for your domain has changed to a green padlock.<br />

[![Bluemix UI: Manage Domains with SSL Uploaded](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL6_nohead_annotated.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL6_nohead_annotated.png)

{:start="5"}
5. If you click on the green padlock (which is the `View Certificate` icon), you will see a dialog much like the one below where you can see all of the important details about the certificate. Note that the dialog also contains buttons that allow you to `Replace` or `Delete` your uploaded files.

[![Bluemix UI: View Certificate](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL7.png){: .center-image }{:style="max-height: 500px;"}](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL7.png)

{:start="6"}
6. If you also uploaded an intermediate certificate, you can click the root node of the certificate tree at the top of the dialog. This will show you all of the important information about the intermediate certificate.

[![Bluemix UI: View Certificate with Intermediate Selected](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL8.png){: .center-image }{:style="max-height: 500px;"}](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL8.png)

{:start="7"}
7. Click the `Close` button on the View Certificate dialog.\
8. Optionally, go back to the App Details view for your app and again bring up the Edit Routes dialog. You should see a green padlock next to your route indicating it's now secured by your uploaded files.

[![Bluemix UI: Edit Routes Dialog with Route Secured](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL9_editRouteWithSSL_annotated.png){: .center-image }](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/custDomainSSL9_editRouteWithSSL_annotated.png)

## Verify the Results

Now, if you try to access your route via the `https` protocol, the browser should declare your site is properly identified and trusted. For example, the screenshot below shows the certificate details for my app from Chrome: 

[![Bluemix UI: Chrome Details Trusted](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/bluemixTonyErwinDetailsInChromeTrusted.png){: .center-image }{:style="max-height: 500px;"}](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/bluemixTonyErwinDetailsInChromeTrusted.png)

But, for full disclosure, if you visit my app (see [https://ssl-demo.bluemix.tonyerwin.com](https://ssl-demo.bluemix.tonyerwin.com/){:target="_blank"}), you'll get a slightly different result because I didn't actually get my certificates from a trusted certificate authority. Instead, I used Keychain Access on my Mac to generate a self-signed intermediate certificate. In addition, I configured the certificate to be trusted on my system. (If you're interested, I described these steps in my other post on [creating self-signed certificates](https://www.tonyerwin.com/2014/09/generating-self-signed-ssl-certificates.html){:target="_blank"}.)   Since my intermediate certificate is obviously not trusted on your system, you'll see a browser warning if you try to access my app. The screen shot below shows the warning I see in Chrome if I try to access my app from another system. While there's still an error, notice that it's no longer a server mismatch error. Instead, Chrome tells me the certificate was issued by an entity not trusted by my computer. 

[![Bluemix UI: Chrome Warning Non-Trusted](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/bluemixTonyErwinDetailsInChromeNonTrusted.png){: .center-image }{:style="max-height: 500px;"}](/images/2014-09-15-bluemix-ui-ssl-certificates-and-custom/bluemixTonyErwinDetailsInChromeNonTrusted.png)

## Redirecting HTTP to HTTPS

So, we're in pretty shape now, but there's one more important item to consider. In my previous post on [redirecting `http` to `https`](https://www.tonyerwin.com/2014/09/redirecting-http-to-https-with-nodejs.html){:target="_blank"}, I explained that unless you take steps (either in your app code or app configuration), unencrypted `http` traffic will still be allowed. You can see an example of that if you visit my live app using the `http` protocol at [http://ssl-demo.bluemix.tonyerwin.com](http://ssl-demo.bluemix.tonyerwin.com/){:target="_blank"}.  In the other post, I go into the problem in much more detail, and I describe a [sample Node.js](https://github.com/aerwin/https-redirect-demo){:target="_blank"} app that demonstrates one approach to solving it. That sample is also running live using my custom domain (and certificates) at [http://redirect-demo.bluemix.tonyerwin.com](http://redirect-demo.bluemix.tonyerwin.com){:target="_blank"}. 

## Conclusion

We covered _a lot_ of ground in this tutorial as you learned all about Bluemix support for associating your certificates with custom domains. Along the way, you saw how to add a custom domain using the Bluemix UI, setup an app to use a custom domain in a route, configure DNS so your custom domain resolves to the IP address of the Bluemix router, and finally upload a certificate for a custom domain. I also briefly touched on some related issues (covered in more detail in other posts) such as generating self-signed certificates and redirecting `http` traffic to `https`. 

_Updated August 10, 2015: Remove mention that a certificate must be a wildcard certificate. That limitation is no longer in place._
