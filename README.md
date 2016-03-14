# cdn-cache

Get CDN files locally, for development or browsing improvement.

## Why?

While developing, refreshing the page can be a pain if you have a bad connection and your project loads lots of external assets, like css, js, fonts, etc.

And lets say it's not *that* easy to change paths to load them locally, or you simplly can't.

So I said, why not having my all those files cached in my computer?

## Get it

- Install the Chrome Extension https://chrome.google.com/webstore/detail/cdncache/cjjmbggfmolglgbakinoejofkgflbibc
- Clone/download the project
- Then run:

```
$ cd server
$ python run.py
```

### Which URLs are actually trapped by cdn-cache?

The domains you specify in the extension config:

![Screen1](https://raw.githubusercontent.com/gbrunacci/gbrunacci.github.io/master/assets/cdncache.png)

## How it works?

1. You install the Chrome extension and run the Server
2. A chrome extension catches all requests, and redirect them to the internal server
3. If it's the first time, it does the real request.
4. Get the response, return it to the browser, and store it locally so next time #3 is skipped.

## To Do

* Firefox Extension
* Support other cache methods
* More config options
