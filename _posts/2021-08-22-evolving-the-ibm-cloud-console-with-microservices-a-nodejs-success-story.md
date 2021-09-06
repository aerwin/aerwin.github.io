---
layout: post
title:  "Evolving the IBM Cloud Console with Microservices: A Node.js Success Story"
date: '2021-08-22T11:20:00.000-06:00'
author: Tony Erwin
description: "The role Node.js played in evolving the IBM Cloud console architecture into a highly scalable, modern microservice-based system."
tags:
- ibm 
- cloud
- kubernetes
- microservices
- nodejs
- micro-frontends
modified_time: '2021-08-22T11:20:00.000-06:00'
image:
    feature: "2021-08-22-evolving-the-ibm-cloud-console-with-microservices-a-nodejs-success-story/console-current-architecture.png"
---

# Introduction
The <a href="https://cloud.ibm.com?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-About" target="_blank">IBM Cloud console</a> provides the web front end for <a href="https://www.ibm.com/cloud" target="_blank">IBM Cloud</a>, an open and secure public cloud providing enterprise-class IaaS and PaaS capabilities with over 170 managed services covering data, AI, IoT, security, blockchain, and more. I’ve had the pleasure of working on the console for most of the last decade. As a more junior developer, I wrote the first lines of proof-of-concept front-end code before IBM Cloud even had a name. This cloud was made <a href="https://www.ibm.com/blogs/cloud-archive/2014/06/general-availability/" target="_blank">generally available as IBM Bluemix in 2014</a>, <a href="https://www.ibm.com/cloud/blog/announcements/bluemix-is-now-ibm-cloud" target="_blank">rebranded as IBM Cloud in 2017</a>, and <a href="https://www.ibm.com/blogs/cloud-archive/2018/11/enhanced-platform-experience/" target="_blank">incorporated the fully integrated SoftLayer experience in 2018</a>.

I became the lead full-stack architect in 2014, and had the opportunity to work with a countless number of talented developers, UI designers, and offering managers as the console’s architecture and user experience (UX) were regularly updated and improved to keep pace with the maturing IBM Cloud. Last year, I left this amazing team for another role as an architect on the <a href="https://www.ibm.com/cloud/financial-services" target="_blank">IBM Cloud for Financial Services</a>. As I reflect on the experience, I’ll share with you how the console architecture has evolved from its monolithic origins into a highly scalable, modern <a href="https://martinfowler.com/articles/microservices.html" target="_blank">microservice-based</a> system composed of dozens of <a href="https://martinfowler.com/articles/micro-frontends.html" target="_blank">micro front ends</a>. In particular, I’ll highlight the critical role that <a href="https://nodejs.org/" target="_blank">Node.js</a> played in this evolution.

&nbsp;
[![IBM Cloud Console Architecture Diagram](/images/2021-08-22-evolving-the-ibm-cloud-console-with-microservices-a-nodejs-success-story/console-current-architecture.png){: .center-image }](/images/2021-08-22-evolving-the-ibm-cloud-console-with-microservices-a-nodejs-success-story/console-current-architecture.png)

{: .button-link-container}
[Read the Full Article on IBM Developer](https://developer.ibm.com/articles/evolving-the-ibm-cloud-console-with-microservices-a-nodejs-success-story/){: .btn }{:target="_blank"}{: .center-text }
