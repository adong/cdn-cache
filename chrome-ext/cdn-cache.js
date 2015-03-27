var CDNCache = {

    localCDNPath: 'http://localhost:8890/',

    domains: [
        'cdnjs.cloudflare.com',
        'cdn.jsdelivr.net',
        'maxcdn.bootstrapcdn.com',
        'cdn.datatables.net',
        'cdns.gigya.com'
    ],

    inDomain: function(path) {
        var a = document.createElement('a');
        a.href = path;
        return CDNCache.domains.indexOf(a.hostname) !== -1;
    },

    get: function(request) {
        if (!CDNCache.inDomain(request.url)) {
            return {
                cancel: false
            };
        }

        var a = document.createElement('a');
        a.href = request.url;

        var newUrl = CDNCache.localCDNPath;//+ '?_ir=cdn-cache&_u=' + encodeURIComponent(request.url  )
        newUrl += encodeURIComponent(a.protocol + "//" + a.host);
        newUrl += a.pathname + a.search + a.hash;

        return {
            redirectUrl: newUrl
        };
    }

};

chrome.webRequest.onBeforeRequest.addListener(
    CDNCache.get,
    { urls: ["*://*/*", "*://*/*"] },
    ["blocking"]
);