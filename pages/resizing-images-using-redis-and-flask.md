title: Resizing images using Flask and Redis.
date: 2013-06-15
published: true
topic: WEB APPS
intro: Recently I put together a mini-project that resizes images conventially through Flask and caches the thumbnal images in Redis.

The code is all on [github](https://github.com/cameronmaske/puppy-eyes) and there is a [demo](http://puppy-eyes.herokuapp.com/) here to try it out! To resize an image, you pass the image's url as the url parameter "link" like so...

[http://puppy-eyes.herokuapp.com/?link=http://i.imgur.com/75Jr3.jpg](http://puppy-eyes.herokuapp.com/?link=http://i.imgur.com/75Jr3.jpg)

And the server will return the resized *thumbnail* image!

##So how does it work?

On the backend, the server looks into the Redis server (a very fast key-store) to see if the resized image already exists (based on the link passed in and sizing options). If it does, great! It get's turned back into an image file from the stored string and servered back.
If it does not exist, the image is downloaded, resized (by PIL), stored in Redis as a string (essentially caching it if a repeat call it made) and then servered back.

If for some reason you linked to something that isn't an image, it should just redirect through.

This mini-project came out of the frustration of images in emails. Getting images with varying heights and widths to appear the same size across popular image clients is a nightmare. Some support max-width, some support only width, some don't even support height (I'm looking at you [Outlook](http://www.campaignmonitor.com/css/)).
While this wasn't the choosen solution in the end, I thinks it's a neat use case of how both the simplicity (and power) of Redis and Flask play nicely together!

Let me know if you have any questions in the comments!
