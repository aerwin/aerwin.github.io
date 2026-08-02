---
layout: post
title: Build a Where? app for web and Pebble users
date: '2014-12-05T00:35:00.000-06:00'

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
categories: [Cloud]
modified_time: '2015-01-11T18:23:29.570-06:00'
blogger_id: tag:blogger.com,1999:blog-5914472037415701789.post-4238120236195489858
blogger_orig_url: http://www.tonyerwin.com/2014/12/build-where-app-for-web-and-pebble-users.html

image:
  path: "/images/2014-12-05-build-where-app-for-web-and-pebble-users/blogger_featured880x440.png"
  show: false
---

![Where? App Logo](/images/2014-12-05-build-where-app-for-web-and-pebble-users/blogger_bluemixGlobeCream300.png)

Where am I? Where can I go? Where have I been? In this tutorial, you'll build a client/server app that answers these and other "where" questions for web users and for wearers of the Pebble smartwatch _(Note: Pebble was acquired by Fitbit/Google and is no longer available)_.

First, you'll build the back end: a [Node.js](https://nodejs.org/) app that you'll deploy to IBM® Bluemix. The back end provides a REST API that enables clients to:

- Register a user's geolocation with the server, to be stored in a Cloudant NoSQL database.
- Get the nearest postal address associated with the location by using the Pitney Bowes Reverse Geocoding service (UPDATE: now part of the APIs from Pitney Bowes service). This service provides a powerful API for looking up postal addresses based on GPS location.
- Retrieve information about where someone could travel from a location, by using the Pitney Bowes Travel Boundary service. This service provides GPS coordinates for a "boundary" around a specified location that can be reached based on driving time or distance.
- Provide worldwide statistics for recent and popular "check-in" locations (using the MapReduce capabilities in Cloudant).

Then, you'll use this REST API as the basis for building two very different client apps:

- A responsive, single-page web app that is implemented by using [AngularJS](https://angularjs.org/), [Bootstrap](https://getbootstrap.com/), and [Leaflet.js](https://leafletjs.com/) and provides extensive, rich content.

![Where? App: Pebble Main Screen](/images/2014-12-05-build-where-app-for-web-and-pebble-users/webApp2_withBoundary.png)

- An app written for Pebble that's designed to provide useful but more-focused info in the smaller screen of this cool wearable device. You'll write this client app in JavaScript by using the Pebble.js library and the CloudPebble online IDE _(Note: both CloudPebble and getpebble.com are no longer available)_.

![Where? App: Web with Travel Boundary](/images/2014-12-05-build-where-app-for-web-and-pebble-users/whereApp_pebble1.png)

_The original IBM developerWorks article and the live demo app are no longer available._