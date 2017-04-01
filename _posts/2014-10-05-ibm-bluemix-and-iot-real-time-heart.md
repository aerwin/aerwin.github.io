---
layout: post
title: 'IBM Bluemix and IoT: Real-Time Heart Rate and Geolocation'
date: '2014-10-05T15:19:00.001-05:00'
author: Tony Erwin
description: "Some of my peers in IBM's Emerging Technology group have been creating some really cool Internet of Things (IoT) demos using IBM Bluemix. Two of them, HR Tracker and Race Tracker, are geared toward fitness and activity tracking. They are both capable of displaying the heart rate and geolocation of exercisers as the values change in real-time. In this post, I'll describe both sample apps and give an overview of the technology used to build them."
tags:
- bluemix
- geolocation
- ibm emerging tech
- mio alpha
- iphone
- m2m
- that conference
- iot
- mqtt
- ibm
- cloudant
- internet of things
- node-red
- node.js
modified_time: '2014-10-05T20:46:26.336-05:00'
blogger_id: tag:blogger.com,1999:blog-5914472037415701789.post-3069709968825056377
blogger_orig_url: http://www.tonyerwin.com/2014/10/ibm-bluemix-and-iot-real-time-heart.html
image:
    feature: "2014-10-05-ibm-bluemix-and-iot-real-time-heart/raceTracker3_2to1Ratio.gif"
    thumb: "2014-10-05-ibm-bluemix-and-iot-real-time-heart/hrOnWristThumb.png"
---

[![MIO Alpha I Strapless Continuous Heart Rate Monitor](/images/2014-10-05-ibm-bluemix-and-iot-real-time-heart/hrOnWrist.JPG){: .paragraph-thumbnail }](/images/2014-10-05-ibm-bluemix-and-iot-real-time-heart/hrOnWrist.JPG)

Some of my peers in IBM's Emerging Technology group have been creating some really cool Internet of Things (IoT) demos using [IBM Bluemix](https://www.bluemix.net){:target="_blank"}. Two of them, HR Tracker and [Race Tracker](http://m2m.demos.ibm.com/sports.html){:target="_blank"}, are geared toward fitness and activity tracking. They are both capable of displaying the heart rate and geolocation of exercisers as the values change in real-time. In this post, I'll describe both sample apps and give an overview of the technology used to build them.

#### HR Tracker

Last month, I got to be part of an HR Tracker demo at [That Conference 2014](https://www.tonyerwin.com/2014/08/ibm-bluemix-and-that-conference-2014.html){:target="_blank"}. For my part, it was a pretty simple process. First, I installed the demo app on my iPhone. Then, I strapped on a brand new, wrist-worn [MIO Alpha I Strapless Continuous Heart Rate Monitor](http://smile.amazon.com/gp/product/B00BJ6HLDI/ref=smi_www_rcolv2_go_smi?ie=UTF8&amp;redirect=true){:target="_blank"}, turned it on, and paired it with the phone via Bluetooth. Finally, I hit the **Start** button in the app. And, before I knew it, a new icon popped up in colleague [Mark VanderWiele's](https://twitter.com/MarkVanderwiele){:target="_blank"} browser showing my heart rate and position. Pretty cool!

[![HR Tracker Screenshot](/images/2014-10-05-ibm-bluemix-and-iot-real-time-heart/hrScreenshot.png){: .center-image }](/images/2014-10-05-ibm-bluemix-and-iot-real-time-heart/hrScreenshot.png)

And, even cooler, as my heart rate changed on the MIO Alpha, I could see it update almost immediately in the web app. 

[![HR Tracker Screenshot](/images/2014-10-05-ibm-bluemix-and-iot-real-time-heart/hrMonitorAndScreen.JPG){: .center-image }{:style="max-width: 400px;"}](/images/2014-10-05-ibm-bluemix-and-iot-real-time-heart/hrMonitorAndScreen.JPG)

At this point, I went out for a short walk. While I was gone, Mark could see exactly where I was and how "hard" I was working (via heart rate) in the parking lot and side streets around the [Kalahari Resort](http://www.kalahariresorts.com/wisconsin){:target="_blank"}.

#### Race Tracker

Race Tracker is similar to HR Tracker, but is geared more toward monitoring data for lots of participants in an event. This morning [Bryan Boyd](https://twitter.com/bryanboyd){:target="_blank"} took part in the [Medtronic Twin Cities Marathon](https://www.tcmevents.org/events/medtronic_twin_cities_marathon_weekend_-_october_3-5_2014/marathon/){:target="_blank"} up here in Minnesota. Of course, running a marathon is way on the other side of the intensity spectrum from my little walk. :)

Via the Race Tracker app (written mostly by Bryan), I was able to "watch" his progress during the race. The animated GIF below (sped up to reduce size) shows Bryan's data updating at he crossed the 20-mile point (on the St. Paul side of the Mississippi River):

[![Race Tracker w/ Bryan Boyd in Marathon](/images/2014-10-05-ibm-bluemix-and-iot-real-time-heart/raceTracker2_800.gif){: .center-image }](/images/2014-10-05-ibm-bluemix-and-iot-real-time-heart/raceTracker2_800.gif)

I then switched to the satellite view and caught him still going strong at Mile 21:

[![Race Tracker w/ Bryan Boyd in Marathon (Satellite)](/images/2014-10-05-ibm-bluemix-and-iot-real-time-heart/raceTracker3_800.gif){: .center-image }](/images/2014-10-05-ibm-bluemix-and-iot-real-time-heart/raceTracker3_800.gif)

Race Tracker can also send notifications at pre-determined intervals. For example, the tweet below came through the feed as Bryan reached 24 miles:

<div style="margin-top:20px;margin-bottom:20px;width:100%;"><blockquote class="twitter-tweet tw-align-center" lang="en"><p>Finished mile 24 at 16:37:36 with a split of 9:04! <a href="https://twitter.com/bryanboyd">@bryanboyd</a> <a href="https://twitter.com/tggiles">@tggiles</a> <a href="https://twitter.com/Lani_Giles">@lani_giles</a></p>&mdash; Bryan Boyd (@bryanboydruns) <a href="https://twitter.com/bryanboydruns/status/518802193399291906">October 5, 2014</a></blockquote><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script></div>

So, did Bryan finish? I wish I knew! Around Mile 25, data updates stopped being shown in the web UI. I'm assuming his heart kept beating. So, did the battery on his phone or heart rate monitor run out? Once I find out, I'll try to post an update. :)

_Update: I heard from Bryan, and his heart is indeed still beating. He blamed the glitch on "developer error." But, as a fellow developer, I know those things happen with prototypes. :) Oh, and by the way, Bryan also [finished the race](http://www.strava.com/activities/203750901/overview){:target="_blank"} in a very respectable 3:57._

#### Technology

On the day I tried HR Tracker, Mark conducted a session called [_From Concept to Operation in 30 minutes Using Services and a PaaS_](https://www.thatconference.com/sessions/session/5473){:target="_blank"}. During his talk, he went through the steps needed to build a Bluemix-based backend for these apps. It was a great demonstration of how quickly the "next big idea" can be prototyped and delivered to run on Bluemix.

Architecturally, [MQTT](http://mqtt.org/){:target="_blank"} ties all of the components together. Every piece either publishes or subscribes to an MQTT Broker (in this case powered by [IBM MessageSight](http://www-03.ibm.com/software/products/en/messagesight){:target="_blank"}). So, for example, when the iPhone app detects a change in heart rate or GPS position, it publishes a message with that information to the MQTT Broker. The MQTT Broker in turn sends the messages to all subscribers.

As you might have guessed, the Bluemix-based backend is a subscriber. Mark started by creating a new app in the Bluemix UI from the [Internet of Things Starter](https://console.ng.bluemix.net/catalog/starters/internet-of-things-platform-starter){:target="_blank"} boilerplate. The resulting app runs a [Node-RED](http://nodered.org/){:target="_blank"} server and is automatically bound to a new instance of the [Cloudant NoSQL DB](https://console.ng.bluemix.net/catalog/services/cloudant-nosql-db){:target="_blank"} service. With NODE-Red, you can graphically create a flow that subscribes to an MQTT Broker and takes appropriate action. In this case, it acts by writing the information to the Cloudant DB and by sending a tweet if the runner has crossed a mile marker. So, in just a few minutes you can have a Bluemix app processing IoT data from a large number of devices and putting that data right into a database for later retrieval and analysis.

And, in case you're wondering, the map UI also subscribes to the messages and updates the display as new information arrives.

##### What's Next?

Since data is stored as it comes in, all sorts of additional features are possible. The Emerging Tech team already has code in HR Tracker to allow people to "replay" past activities or to compete against themselves (or others) on previous routes.

They've also begun exploring interesting things that could be done by applying analytics to all of this data. For example, did someone cheat? Does data indicate someone was grabbing the side of a car for half of their so-called bike ride?

With that, I'll close with a question to anyone who has made it this far in the post. And, I'd love to see some responses in the comments section. :)

_Question: If you had access to all of the data generated by this IoT scenario, what would you be interested to find out?_

#### Related Resources

- [m2m demos @ IBM](http://m2m.demos.ibm.com/index.html){:target="_blank"}
- [Race Tracker Overview](http://m2m.demos.ibm.com/sports.html){:target="_blank"}{:target="_blank"} & [Race Tracker Web App](http://racetracker.mybluemix.net/){:target="_blank"}
- [_MQTT: A Practical Protocol for the Internet of Things_](http://www.slideshare.net/BryanBoyd/mqtt-austin-api){:target="_blank"} by [Bryan Boyd](https://twitter.com/bryanboyd){:target="_blank"}
- [IBM Mobile and M2M Community](https://www.ibm.com/developerworks/community/blogs/c565c720-fe84-4f63-873f-607d87787327/tags/blog?lang=en){:target="_blank"}

