---
layout: post
title:  "Bluemix UI Architecture Presented at Cloud Foundry Summit 2017"
date: '2017-08-06T21:11:00.000-05:00'
author: Tony Erwin
description: "In June, I had the honor of attending the Cloud Foundry Summit Silicon Valley 2017 conference. My two submissions related to Bluemix UI architecture were selected, and I got the chance to present them. One talk centered around migration of the Bluemix UI from a monolith to a microservices architecture, and the other talk focused on best practices around monitoring microservice systems. In this post, I'll briefly describe my talks as well as share some general takeaways from the conference."
tags:
- bluemix
- bluemix ui
- architecture
- microservices
- node.js
- cloud foundry
- cf summit
modified_time: '2017-08-06T21:11:00.000-05:00'
image:
    feature: "2017-08-06-bluemix-ui-at-cf-summit/cloud_foundry_summit_badge.jpg"
---

# Introduction
In June, I had the honor of attending the [Cloud Foundry Summit Silicon Valley 2017](https://www.cloudfoundry.org/event/summit-silicon-valley-2017/){:target="_blank"} conference in Santa Clara, CA. My two submissions related to [Bluemix UI](https://console.bluemix.net/?cm_mmc=TonyErwin-_-Data-_-WW_WW-_-CFSummit2017){:target="_blank"} architecture were selected, and I got the chance to present them as part of the conference's Cloud Native Node.js track. In this post, I'll briefly describe my talks as well as share some general takeaways from the conference.

# Topic 1: Microservices Architecture of the Bluemix UI
The full title of my first topic was [_To Kill a Monolith: Slaying the Demons of a Monolith with Node.js Microservices on Cloud Foundry_](http://sched.co/AJmh){:target="_blank"}. The intent of the talk to was to trace my team's journey migrating the Bluemix UI from a monolithic app to a microservices architecture. 

The Bluemix UI (which runs on Cloud Foundry) is the front-end to Bluemix, IBM's open cloud hosting platform. The original implementation as a single-page, monolithic Java web app brought with it many demons, such as poor performance, lack of scalability, inability to push small updates, and difficulty for other teams to contribute code. Over the last 2 years, the team has been on a mission to slay these demons by embracing cloud native principles and splitting the monolith into smaller Node.js microservices. The effort to migrate to a more modern and scalable architecture has paid large dividends, but has also left behind a few battle scars from wrestling with the added complexity cloud native can bring. The team had to tackle problems in a wide variety of areas, including: large-scale deployments, continuous integration, monitoring, problem determination, high availability, and security. 

In the talk, I went on to discuss the advantages of microservice architectures, ways that Node.js has increased developer productivity, approaches to phasing microservices into a live product, and real-life lessons learned in the deployment and management of Node.js microservices across multiple Cloud Foundry environments.

If you'd like to see the full presentation, check out the slide deck below:

<div class="center-image">
    <iframe src="//www.slideshare.net/slideshow/embed_code/key/J2Dmo3J4Nnl8hV" width="756" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe>
</div>

Or, if you prefer video, you can watch the talk on YouTube:

<div class="center-image">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/psvBZkrkiRM" frameborder="0" allowfullscreen></iframe>
</div>

# Topic 2: Monitoring Node.js Microservices
My second topic was called [_Monitoring Node.js Microservices on Cloud Foundry with Open Source Tools and a Shoestring Budget_](http://sched.co/AJmn){:target="_blank"}. During the migration described in my first talk, we learned that while microservice architectures offer lots of great benefits, there’s also a downside. Perhaps most notably, there is an increased complexity in monitoring the overall reliability and performance of the system. In addition, when problems are identified, finding a root cause can be a challenge. To ease these pains in managing the Bluemix UI, we’ve built a lightweight system using Node.js and other opensource tools to capture key metrics for all microservices (such as memory usage, CPU usage, speed and response codes for all inbound/outbound requests, etc.). 

In this approach, each microservice publishes lightweight messages (using MQTT) for all measurable events while a separate monitoring microservice subscribes to these messages. When the monitoring microservice receives a message, it stores the data in a time series DB (InfluxDB) and sends notifications if thresholds are violated. Once the data is stored, it can be visualized in Grafana to identify trends and bottlenecks. 

In the presentation, I described the details of the Node.js implementation, real-world examples of how this system has been used to keep the Bluemix UI running smoothly without spending a lot of money, and how the system has acted as a “canary in the mine shaft" to find problems in non-UI subsystems before the relevant teams even knew there was an issue!

The slide deck for the presentation is available below:

<div class="center-image">
    <iframe src="//www.slideshare.net/slideshow/embed_code/key/pKFMdi6Z9LMNgq" width="756" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe>
</div>

And, you can also watch it on YouTube:

<div class="center-image">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/kpC4h7pSpiI" frameborder="0" allowfullscreen></iframe>
</div>

# Takeaways from the Conference
This was my second trip to CF Summit, and in both cases it was a great experience. In my first trip in 2015, I gave a [talk with Brian Martin](http://santaclara2015.cfsummit.com/program/schedule){:target="_blank"} when my team was basically just getting started on our journey to microservices. Then, I was a little naive about what we were getting into, but this time around I was far more battle-hardended and had more in-depth knowledge and experiences to share.

One thing I noticed in the questions afterward this time is that there were more people who came up to me and asked questions specific to their own journeys re-architecting monoliths. This tells me there are a lot of organizations struggling with what to do with their legacy code bases and that they are hungry for guidance. Of course, post talk questions are far from scientific. But, I found it interesting nonetheless.

One thing I emphasized to these folks was to not underestimate the need for robust monitoring as they build out their own microservices. As I went into far more detail in my second talk, I think this was the biggest mistake we made when we started the Bluemix UI migration.

# Oh, yeah... Wally World
I stayed at the [Hilton](http://www3.hilton.com/en/hotels/california/hilton-santa-clara-SJCSCHF/index.html){:target="_blank"} across the street from the [Santa Clara Convention Center](http://santaclaraconventioncenter.org/){:target="_blank"} where the conference was held. From my room, I had a great view of [Levi's Stadium](http://www.levisstadium.com/){:target="_blank"} and [California's Great America](https://www.cagreatamerica.com/){:target="_blank"}. 

Every morning I'd look out from my window and see the vast parking lots for both facilities sitting empty:

![Empty Parking at Great America](/images/2017-08-06-bluemix-ui-at-cf-summit/empty-parking-lot-at-great-america.jpg){: .center-image }

And, each day I kept hoping the [Griswold's](http://www.imdb.com/title/tt0085995/){:target="_blank"} would come driving up in their family truckster and see the park was closed, just like Wally World was in 1983. ![Smiley Face](https://pic.sopili.net/pub/emoji/twitter/2/72x72/1f600.png){: .emoticon-image }

<iframe width="560" height="315" src="https://www.youtube.com/embed/HU-bvDvCMlU?t=8s" frameborder="0" allowfullscreen></iframe>
