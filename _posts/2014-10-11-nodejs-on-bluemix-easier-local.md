---
layout: post
title: 'Node.js on Bluemix: Easier Local Development with cfenv'
date: '2014-10-11T15:01:00.001-05:00'
author: Tony Erwin
description: "I'm a fan of the cfenv package for Node.js written by Patrick Mueller. It parses environment info in a Bluemix (or Cloud Foundry) application and provides functions to make it convenient to retrieve all of the service attributes you need from VCAP_SERVICES. I've written a simple wrapper to make local development of apps a little easier by parsing a local copy of your app's env.log file and initializing cfenv with that info. After this initialization, you can use the same cfenv interface just as if you were running in the cloud."
tags:
- bluemix
- code samples
- bluemix ui
- cfenv
- ibm
- paas
- cloud
- node.js
- vcap_services
- cloud foundry
modified_time: '2015-01-13T15:08:25.367-06:00'
blogger_id: tag:blogger.com,1999:blog-5914472037415701789.post-7414599619318526008
blogger_orig_url: http://www.tonyerwin.com/2014/10/nodejs-on-bluemix-easier-local.html
image:
    feature: "2014-10-11-nodejs-on-bluemix-easier-local/bluemixUI_EnvVars.png"
    thumb: "2014-10-11-nodejs-on-bluemix-easier-local/googleThumb72.png"
---

_Updated: Nov. 22, 2014 to reflect deprecation of `env.log`._

I'm a fan of the [`cfenv`](https://github.com/cloudfoundry-community/node-cfenv){:target="_blank"} package for [Node.js](http://nodejs.org/){:target="_blank"} written by [Patrick Mueller](https://twitter.com/pmuellr){:target="_blank"}. It parses environment info in a [Bluemix](https://console.bluemix.net){:target="_blank"} (or [Cloud Foundry](http://cloudfoundry.org/){:target="_blank"}) application, and provides functions to make it easy to retrieve all of the service data you need from [`VCAP_SERVICES`](https://console.bluemix.net/docs/services/rules/index-gentopic4.html#programming){:target="_blank"}. It also gives access to other important attributes for port, host name/ip address, URL of the application, etc. On top of that, it detects whether your app is running locally or in the cloud. And, when running locally, it provides handy defaults.

I've written a simple wrapper (a local module called `cfenv-wrapper`) to make local development of Bluemix/Cloud Foundry apps a little easier. My code parses a local copy of your app's environment data, and extracts the data for `VCAP_SERVICES` and `VCAP_APPLICATION`. Then, it passes that information to `cfenv`'s initialization function, `getAppEnv`. After this initialization, you can use the same `cfenv` interface just as if you were running in the cloud.

The local environment data can be in JSON or properties files meeting the following requirements:

- `env.json` -- JSON file with `VCAP_SERVICES` info as retrieved by `cf env`. If `env.json` is present, the code will also load `env_custom.json`,  which should hold JSON representing your app's user-defined environment variables.
- `env.log` file (deprecated) -- If there's no `env.json` file, the wrapper will load a local copy of your app's `env.log` file. This is provided for backwards compatibility with earlier versions of `cfenv-wrapper`. After CF 182, CF stopped providing an `env.log` file for <a href="https://github.com/cloudfoundry/dea_ng/pull/147">security reasons</a>.

**NOTE:** Many cloud services can be accessed with no changes when running locally. In Bluemix, a partial list of these includes [Cloudant](https://console.ng.bluemix.net/catalog/services/cloudant-nosql-db){:target="_blank"}, [Pitney Bowes](https://console.ng.bluemix.net/catalog/services/apis-from-pitney-bowes){:target="_blank"}, and [Twilio](https://console.ng.bluemix.net/catalog/services/twilio){:target="_blank"}. In those cases, you can use `env.json` and `env.log` with the exact data provided by CF. However, there are services that don't yet allow connections from outside of Bluemix. For those services, you would need to modify your local file so that it uses info specific to installations of those services in your local environment.

#### New Functions
My wrapper also adds two new functions, not in the original `cfenv` interface:

- `getEnvVars` -- returns JSON data structure containing all environment variables. When running locally, it returns the data from the `env_custom.json` or `env.log` files. When running in the cloud, it will return the standard `process.env` runtime variable.
- `getEnvVar(name)` -- returns value of the environment variable with the given name. When running locally, it will try to pull the value from the `env_custom.json` or `env.log` files. If it can't find it, it falls back to the standard `process.env` runtime variable.

These serve to give you a consistent interface for environment variable resolution in both environments.

#### Code on Github
The code for `cfenv-wrapper` (and a working sample) is available on GitHub:

- <a target="_blank" href="https://github.com/aerwin/node-cfenv-wrapper" title="GitHub Repository for node-cfenv-wrapper">https://github.com/aerwin/node-cfenv-wrapper/</a>

The repository's README file contains full details on how to get the code and run either locally or in Bluemix.

#### Run Live Code

You can run a working version of the code deployed to Bluemix by using the link below:

- <a target="_blank" href="http://cfenv-wrapper.mybluemix.net/">http://cfenv-wrapper.mybluemix.net/</a>

When you run it, you should see something like the following screenshot split into three sections for Base Info, Services, and Environment Variables. The Services section shows the names of any services the app is bound to. The Environment Variables section shows the standard environment variables common to Cloud Foundry apps plus any custom environment variables. NOTE: The code intentionally prunes `VCAP_SERVICES` from the Environment Variable output because it typically contains sensitive service credentials.

![Screenshot of Running cfenv-wrapper](/images/2014-10-11-nodejs-on-bluemix-easier-local/cfenvWrapperLive.png){: .center-image }

Below, you can see the details for my app in the Bluemix UI. Notice the list of services matches the `cfenv-wrapper` output:<br />

![Bluemix UI: App Details for cfenv-wrapper](/images/2014-10-11-nodejs-on-bluemix-easier-local/bluemixUI_AppDetails.png){: .center-image }

Also, for this deployment of the app, I've set three custom environment variables (e.g., `CUSTOM_ENV_VAR1`, `CUSTOM_ENV_VAR2`, and `CUSTOM_ENV_VAR3`). 

![Bluemix UI: Environment Variables for cfenv-wrappe](/images/2014-10-11-nodejs-on-bluemix-easier-local/bluemixUI_EnvVars.png){: .center-image }

You can set custom environment variables either in the UI (above) or via the command line: `cf set-env cfenv-wrapper CUSTOM_ENV_VAR1 "Value 1"`

#### Getting Environment Info For Local System

##### JSON Format

To see a JSON representation of your app's environment data, you can run the following `cf` command: `cf env APP_NAME`

Then, copy the JSON (which starts right after the **System-Provided** header and ends just before the **User-Provided** header) into a file named `env.json`. This file should be in the same place on your local file system that you put the code. That is, as a peer to the `server.js` file.

If you have user-defined environment variables, put them into a file name `env_custom.json`. For example, if `cf env` shows the following user-provided environment variables:

```
User-Provided:
CUSTOM_ENV_VAR1: Value 1
CUSTOM_ENV_VAR2: Value 2
CUSTOM_ENV_VAR3: Value 3
```

Then, you would want your `env_custom.json` file to look like this:

```
{
    "CUSTOM_ENV_VAR1": "Value 1",
    "CUSTOM_ENV_VAR2": "Value 2",
    "CUSTOM_ENV_VAR3": "Value 3"
}
```

##### `env.log` Format

_NOTE: This section is only applicable if running a version of CF earlier than 182._

To see the contents of `env.log`, you can run the following `cf` command: `cf files APP_NAME logs/env.log`

Then, copy the output into a file named `env.log` to the same place on your local file system that you put the code. That is, as a peer to the `server.js` file.

#### The Code

##### `server.js`

The `server.js` file is shown below. It initializes the `cfenv-wrapper` and then uses it to retrieve and display base info, names of services bound to the app, and environment variables.

<script src="http://gist-it.appspot.com/github.com/aerwin/node-cfenv-wrapper/blob/master/server.js"></script>

##### `cfenv-wrapper.js`

The `cfenv-wrapper.js` file is shown below. If running locally, it will try to parse `env.json` in the working directory. If found and successfully parsed, it will then initialize `cfenv`. If, not it will try to load and parse `env.log`. If there's no success using `env.json` nor `env.log`, then the wrapper  will just use `cfenv` with no special initialization. In addition to this initialization, the code provides functions that "wrap" the functions of `cfenv`.

<script src="http://gist-it.appspot.com/github.com/aerwin/node-cfenv-wrapper/blob/master/cfenv-wrapper.js"></script>