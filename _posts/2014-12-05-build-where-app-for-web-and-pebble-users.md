---
layout: post
title: Build a Where? app for web and Pebble users
date: '2014-12-05T00:35:00.000-06:00'
author: Tony Erwin
description: "Create an app that answers 'where' questions. You'll build and deploy a back-end Node.js application on Bluemix that provides a REST API to support client apps. Then you'll build two client apps: one for the web and one for the Pebble smartwatch.
"
tags:
- pebble
- bluemix
- bluemix ui
- cloud pebble
- paas
- geocoding
- javascript
- angular
- express
- pitney bowes
- leaflet.js
- wearables
- iot
- bootstrap
- rest
- cloudant
- node.js
modified_time: '2015-01-11T18:23:29.570-06:00'
blogger_id: tag:blogger.com,1999:blog-5914472037415701789.post-4238120236195489858
blogger_orig_url: http://www.tonyerwin.com/2014/12/build-where-app-for-web-and-pebble-users.html
image:
    feature: "2014-12-05-build-where-app-for-web-and-pebble-users/blogger_thumb72.pn"
    thumb: "2014-12-05-build-where-app-for-web-and-pebble-users/bluemix_logo_multi_181_Thumb.png"
---

![Where? App Logo](/images/2014-12-05-build-where-app-for-web-and-pebble-users/blogger_bluemixGlobeCream300.png){: .paragraph-thumbnail }

Where am I? Where can I go? Where have I been? In this tutorial, you'll build a client/server app that answers these and other "where" questions for web users and for wearers of the [Pebble](https://getpebble.com/){:target="_blank"} smartwatch.

First, you'll build the back end: a [Node.js](http://nodejs.org/){:target="_blank"} app that you'll deploy to [IBM® Bluemix](https://www.bluemix.net/){:target="_blank"}. The back end provides a REST API that enables clients to:

- Register a user's geolocation with the server, to be stored in a [Cloudant NoSQL database](https://console.ng.bluemix.net/catalog/services/cloudant-nosql-db?env_id=ibm:yp:us-south){:target="_blank"}.
- Get the nearest postal address associated with the location by using the Pitney Bowes Reverse Geocoding service (UPDATE: now part of the [APIs from Pitney Bowes](https://console.ng.bluemix.net/catalog/services/apis-from-pitney-bowes?env_id=ibm:yp:us-south){:target="_blank"} service). This service provides a powerful API for looking up postal addresses based on GPS location.
- Retrieve information about where someone could travel from a location,  by using the Pitney Bowes Travel Boundary service. This service provides GPS coordinates for a "boundary" around a specified location that can be reached based on driving time or distance.
- Provide worldwide statistics for recent and popular "check-in" locations (using the [MapReduce](https://cloudant.com/product/cloudant-features/mapreduce/){:target="_blank"} capabilities in Cloudant).

Then, you'll use this REST API as the basis for building two very different client apps:

- A responsive, single-page web app that is implemented by using [AngularJS](https://angularjs.org/){:target="_blank"}, [Bootstrap](http://getbootstrap.com/){:target="_blank"}, and [Leaflet.js](http://leafletjs.com/){:target="_blank"} and provides extensive, rich content.

![Where? App: Pebble Main Screen](/images/2014-12-05-build-where-app-for-web-and-pebble-users/webApp2_withBoundary.png){: .center-image }

- An app written for Pebble that's designed to provide useful but more-focused info in the smaller screen of this cool wearable device. You'll write this client app in JavaScript by using the [Pebble.js](http://pebble.github.io/pebblejs/){:target="_blank"} library and the [CloudPebble](https://cloudpebble.net/){:target="_blank"} online IDE.

![Where? App: Web with Travel Boundary](/images/2014-12-05-build-where-app-for-web-and-pebble-users/whereApp_pebble1.png){: .center-image }

{: .button-link-container}
[Read Article on IBM developerWorks](http://www.ibm.com/developerworks/library/mo-pebble-where-app/index.html){: .btn }{:target="_blank"}{: .center-text }[Run Web App](https://where.mybluemix.net/){: .btn }{:target="_blank"}