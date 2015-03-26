var CDNCache = {

    domains: [
        'cdnjs.cloudflare.com',
        'cdn.jsdelivr.net',
        'maxcdn.bootstrapcdn.com',
        'cdn.datatables.net'
    ],

    inDomain: function(path) {
        var a = document.createElement('a');
        a.href = path;
        return CDNCache.domains.indexOf(a.hostname) !== -1;
    },

    getFromCache: function(path) {
        return localStorage.getItem(path);
    },

    store: function(path) {
        // Too bad, we are doing another request! =(
        var xhr = new XMLHttpRequest();
        xhr.open("GET", path + "?ignorecdncache", true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                // Only cache if successful
                if ( xhr.status >= 200 && xhr.status < 300 ) {
                    var contentType = xhr.getResponseHeader('content-type');
                    //// If a CSS file contains an URL, we can't cache
                    //// As any redirect will change the reference
                    //if ( xhr.responseText.indexOf('url(') !== -1 )
                    //    return;
                    //
                    var base64Body = '';
                    try {
                        // try doing a simple base64 conversion
                        base64Body = btoa(xhr.responseText);
                    } catch (e) {
                        // try doing a utf8-escaped base64 conversion
                        base64Body = btoa(unescape(encodeURIComponent(xhr.responseText)));
                    }
                    var base64Response = "data:" + contentType + ";base64," + base64Body;
                    localStorage.setItem(path, base64Response);
                    delete base64Body;
                    delete base64Response;  // this one can be quite big
                }
            }
        }
        xhr.send();
    },

    get: function(request) {
        if (!CDNCache.inDomain(request.url)) {
            return {
                cancel: false
            };
        }

        var cachedElement = CDNCache.getFromCache(request.url);
        if (cachedElement) {
            return {
                redirectUrl: cachedElement
            };
        }

        CDNCache.store(request.url);

        return {
            cancel: false
        };
    }

};

chrome.webRequest.onBeforeRequest.addListener(
    CDNCache.get,
    { urls: ["*://*/*", "*://*/*"] },
    ["blocking"]
);