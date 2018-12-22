---
layout: post
title:  "IBM Cloud Platform Unification Project"
date: '2018-12-22T15:15:00.000-06:00'
author: Tony Erwin
description: "Earlier this month, we launched a revamped IBM Cloud Platform Experience at our new cloud.ibm.com location. Our primary goal was to unify our IaaS and PaaS offerings to better meet your needs. This was a massive undertaking with changes up and down the stack. Prior to this unification, there were two distinct UI's at different URLs -- one for IaaS and one for PaaS. This understandably led to a lot of frustration and confusion. We wanted to fix this by creating a seamless experience with one UI at a single URL to manage everything. We're very excited by the outcome, and we think you will be too."
tags:
- ibm 
- cloud
- iaas
- paas
- user experience
- console
modified_time: '2018-12-22T15:15:00.000-06:00'
image:
    feature: "2018-12-22-ibm_cloud_platform_unification_project/ibm_cloud_console_dashboard.png"
---

# Introduction
Earlier this month, we launched a revamped [IBM Cloud Platform Experience](https://www.ibm.com/cloud/platform?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"} at our new [cloud.ibm.com](https://cloud.ibm.com?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"} location. Our primary goal was to unify our [IaaS](https://www.ibm.com/cloud/infrastructure?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"} and [PaaS](https://www.ibm.com/blogs/cloud-computing/2014/02/17/what-is-platform-as-a-service-paas/?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"} offerings to better meet your needs. This was a massive undertaking with changes up and down the stack. We're very excited by the outcome, and we think you will be too.

Prior to this unification, there were two distinct UI's at different URLs -- one for IaaS and one for PaaS. This understandably led to a lot of frustration and confusion. We wanted to fix this by creating a seamless experience with _one_ UI at a single URL to manage everything. With that in mind, the user experience of our console was overhauled to bring new and/or improved capabilities in the following areas:

- dashboard (see screenshot below)
- resource management
- search and tagging
- catalog/purchasing
- account/user management
- billing
- support
- overall performance
- and more! 

&nbsp;
[![IBM Cloud Console Dashboard](/images/2018-12-22-ibm_cloud_platform_unification_project/ibm_cloud_console_dashboard.png){: .center-image }](/images/2018-12-22-ibm_cloud_platform_unification_project/ibm_cloud_console_dashboard.png)

# Rollout of `cloud.ibm.com`
With such massive changes, we faced a number of interesting questions about how to best rollout the new experience. I will summarize our thought process here, but for more details about our strategy, see _[A/B Test Deployment — Rollout of cloud.ibm.com](https://www.ibm.com/blogs/bluemix/2018/11/a-b-test-deployment-rollout-of-cloud-ibm-com/?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"}_ written by myself and colleague [Nic Sauriol](https://www.linkedin.com/in/nsauriol/?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"}.

We were very sensitive to the fact that the holiday season is a key time of year for many of our clients, and we did not want to do anything to disrupt their operations. On the other hand, we believe the new experience offers improvements that our clients could benefit from immediately. Ultimately, we decided to go with an A/B rollout strategy with two consoles running side by side. The diagram below shows a very high-level architecture. Both consoles are deployed separately, but use exactly the same set of [IBM Cloud Platform APIs](https://cloud.ibm.com/apidocs?category=platform_services&cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"} on the backend.

[![Rollout Architecture for cloud.ibm.com](/images/2018-12-22-ibm_cloud_platform_unification_project/cloud_ibm_com_rollout_architecture.png){: .center-image }](/images/2018-12-22-ibm_cloud_platform_unification_project/cloud_ibm_com_rollout_architecture.png){:target="_blank"}

Users in the A group see the existing experience at `console.bluemix.net`, while users in the B group get the enhanced console at [cloud.ibm.com](https://cloud.ibm.com?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"}. However, the choice of console is entirely up to each individual user. At some point in the new year, we will retire the experience at `console.bluemix.net` and force a transition. But, until then, users are free to switch back and forth between both experiences. 

From a technical perspective, we use the [IBM Cloud Kubernetes Service](https://www.ibm.com/cloud/container-service?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"} to host the [microservices that make up the console](https://www.slideshare.net/tonyerwin/migration-of-an-enterprise-ui-microservice-system-from-cloud-foundry-to-kubernetes){:target="_blank"}. By using this service, it’s very simple to spin up  Kubernetes clusters to host both experiences. We can easily make use of the same build pipeline, Helm Charts, and so on, but with different code branches for the new experience.

(NOTE: Something not captured in the high-level architecture is that both consoles are actually made up of many geographically load balanced clusters placed all over the world. This is used to provide for high availability and failover. The concepts behind this are described in my previous blog _[Global IBM Cloud Console Architecture](/2018/02/global-cloud-console-architecture.html?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification)_.)

# Other Related Content
Aside from the A/B rollout blog summarized above, many teammates of mine produced an extensive set of blogs with detailed information about all of the changes found in the unified experience. I highly recommend you check these out!

- _[Introducing the Enhanced IBM Cloud Platform Experience](https://www.ibm.com/blogs/bluemix/2018/11/enhanced-platform-experience/?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"}_ &mdash; [Mark Meredith](https://www.linkedin.com/in/mark-meredith-93684273/){:target="_blank"}
- _[Bringing It All Together: A Single Account and Billing Management Experience](https://www.ibm.com/blogs/bluemix/2018/11/ibm-cloud-account-management/?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"}_ &mdash; [Sydney Riggs](https://www.linkedin.com/in/sydneyriggs/){:target="_blank"} & [Brendan Fitzpatrick](https://www.linkedin.com/in/brendanfitzpatrick/){:target="_blank"}
- _[Outstanding User Access Improvements Help Deliver a Unified IBM Cloud Platform](https://www.ibm.com/blogs/bluemix/2018/11/ibm-cloud-access-management/?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"}_ &mdash; [Tim Brantner](https://www.linkedin.com/in/timbrantner/){:target="_blank"}, [Ben Lopez](https://www.linkedin.com/in/benlopeztx/){:target="_blank"}, & [Michelle Kaufman](https://www.linkedin.com/in/michelle-kaufman-ba4ab552/){:target="_blank"}
- _[Life Just Got Easier with the Enhanced IBM Cloud Support Center](https://www.ibm.com/blogs/bluemix/2018/11/ibm-cloud-support-center/?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"}_ &mdash; [Amit Patel](https://www.linkedin.com/in/amit-patel-902a4b1/){:target="_blank"}
- _[Platform Tagging on the Enhanced IBM Cloud Platform](https://www.ibm.com/blogs/bluemix/2018/11/platform-tagging-on-the-enhanced-ibm-cloud-platform/?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){:target="_blank"}_ &mdash; [Kala Nenkova](https://www.linkedin.com/in/kala-nenkova-526b20103/){:target="_blank"}

# Conclusion
I sincerely hope you enjoy the new experience, and would love to get your feedback (both good and bad) in order to learn and better meet your needs. So, please reach out and let me know how it goes!

{: .button-link-container}
[Try Out the New Experience!](https://cloud.ibm.com?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CloudPlatformUnification){: .btn }{:target="_blank"}{: .center-text }



