/**
 * Copyright 2016 Google Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/

// DO NOT EDIT THIS GENERATED OUTPUT DIRECTLY!
// This file should be overwritten as part of your build process.
// If you need to extend the behavior of the generated service worker, the best approach is to write
// additional code and include it using the importScripts option:
//   https://github.com/GoogleChrome/sw-precache#importscripts-arraystring
//
// Alternatively, it's possible to make changes to the underlying template file and then use that as the
// new base for generating output, via the templateFilePath option:
//   https://github.com/GoogleChrome/sw-precache#templatefilepath-string
//
// If you go that route, make sure that whenever you update your sw-precache dependency, you reconcile any
// changes made to this original template file with your modified copy.

// This generated service worker JavaScript will precache your site's resources.
// The code needs to be saved in a .js file at the top-level of your site, and registered
// from your pages in order to be used. See
// https://github.com/googlechrome/sw-precache/blob/master/demo/app/js/service-worker-registration.js
// for an example of how you can register this script and handle various service worker events.

/* eslint-env worker, serviceworker */
/* eslint-disable indent, no-unused-vars, no-multiple-empty-lines, max-nested-callbacks, space-before-function-paren, quotes, comma-spacing */
'use strict';

var precacheConfig = [["/about-us.html","a33705097161fa80eefc2cd6b9c3f9ad"],["/css/libs.min.css","de833be23ea9bf83f1d4b4cda50e6d2f"],["/css/style.min.css","8c59e16530e943970c3b815e59995ab1"],["/fonts/FontAwesome.otf","0d2717cd5d853e5c765ca032dfd41a4d"],["/fonts/Material-Design-Iconic-Font.eot","e833b2e2471274c238c0553f11031e6a"],["/fonts/Material-Design-Iconic-Font.svg","381f7754080ed2299a7c66a2504dff02"],["/fonts/Material-Design-Iconic-Font.ttf","b351bd62abcd96e924d9f44a3da169a7"],["/fonts/Material-Design-Iconic-Font.woff","d2a55d331bdd1a7ea97a8a1fbb3c569c"],["/fonts/Material-Design-Iconic-Font.woff2","a4d31128b633bc0b1cc1f18a34fb3851"],["/fonts/PlayfairDisplay-Bold.eot","89ed4ea5fc9a5c95e756c4ca2fae7859"],["/fonts/PlayfairDisplay-Bold.ttf","8105bcf37f6fa55eaccf960ba1a53def"],["/fonts/PlayfairDisplay-Bold.woff","b65a2e4a34911f8368e87655b0603b4a"],["/fonts/PlayfairDisplay-Regular.eot","a2a3e09dd48238fa6cd7d289a4b0e927"],["/fonts/PlayfairDisplay-Regular.ttf","ddadd153f0b2b6f44e8146ad6bb1d8b1"],["/fonts/PlayfairDisplay-Regular.woff","77df03ee706763d67b3880b743a175e3"],["/fonts/ProximaNova-Black.eot","4325ed848b66ed370420ea7fea09bc80"],["/fonts/ProximaNova-Black.ttf","a0606c5fef28b9e57f501db027063141"],["/fonts/ProximaNova-Black.woff","b978d1b46a86df7a012cf8442936a1cb"],["/fonts/ProximaNova-Bold.eot","10141a9d737da9c84e6e14ec5a562c6c"],["/fonts/ProximaNova-Bold.ttf","926a08fb27e3303c7452b0bdd2d5e5ab"],["/fonts/ProximaNova-Bold.woff","e2cf3dc2f079bf3d5185a02552f153c4"],["/fonts/ProximaNova-Light.eot","d778218590f14376c366c515d384808e"],["/fonts/ProximaNova-Light.ttf","0188899cd3ec92cdcaa4c97ca0c75247"],["/fonts/ProximaNova-Light.woff","eb74a591665045d87eabfb2dc759be0a"],["/fonts/ProximaNova-Regular.eot","b7c512788e3c77b0196f0bace8a88418"],["/fonts/ProximaNova-Regular.ttf","7ce6760d17685c466ba04d1b2c63c38b"],["/fonts/ProximaNova-Regular.woff","2d2ae2556b24a45ff8d5ed86b07b5783"],["/fonts/fontawesome-webfont.eot","674f50d287a8c48dc19ba404d20fe713"],["/fonts/fontawesome-webfont.svg","acf3dcb7ff752b5296ca23ba2c7c2606"],["/fonts/fontawesome-webfont.ttf","b06871f281fee6b241d60582ae9369b9"],["/fonts/fontawesome-webfont.woff","fee66e712a8a08eef5805a46892932ad"],["/fonts/fontawesome-webfont.woff2","af7ae505a9eed503f8b8e6982036873e"],["/fonts/lg.eot","ecff11700aad0000cf3503f537d1df17"],["/fonts/lg.svg","0cb1b8af9950584b5cc8e8250e045508"],["/fonts/lg.ttf","4fe6f9caff8b287170d51d3d71d5e5c6"],["/fonts/lg.woff","5fd4c338c1a1b1eeeb2c7b0a0967773d"],["/img/jpg/about-banner.jpg","dd23a1eb18a34130127508e636b9f5a6"],["/img/jpg/bg-line.jpg","5dad1638faa22fe2addbcd3c96c90bb1"],["/img/jpg/bg-line2.jpg","2e3a5ea8f655b75fbd29de243b123c28"],["/img/jpg/footer.jpg","f068d7b397ce6940ec322d6c47612616"],["/img/jpg/gal1.jpg","99275ca6a4dab36f82e3ad7640e422e5"],["/img/jpg/gal2.jpg","19528e11a7828e8a8e4ed4171e566eaf"],["/img/jpg/gal3.jpg","e2748fc60e02b09773dd4470fab32b6c"],["/img/jpg/gal4.jpg","454ffaf7bb075dde99b9b6fb6fc3df60"],["/img/jpg/human.jpg","1d00d9bbc132d9d261681aab752d0321"],["/img/jpg/slider1.jpg","d24c87da6dc34b4489d7ef67f0189c50"],["/img/jpg/slider2.jpg","ea8bc2a0481725499baf3c4822e8a1bf"],["/img/jpg/slider3.jpg","719032af1cbb3ef79c90c0f3350e5f17"],["/img/jpg/slider4.jpg","f2abb853944df53a4dbe8709007ae948"],["/img/png/Divan.png","61683aa57f1e62bf16ce13b7cd5ad5cf"],["/img/png/ab1.png","1373fdfe5b74868629dfd62a7a0630fe"],["/img/png/ab2.png","2dcd25bbfb684faa544ba46ffba56dea"],["/img/png/ab3.png","b9b4463bc2753ef18863e160a0a8e531"],["/img/png/ab4.png","0803b7ee5811aeb4d548ebc2523ea1de"],["/img/png/arrow-button-right.png","8225ecfaec37f08eefa4b075dcd3b988"],["/img/png/arrow-button-right2.png","bfb667129add490e166b7fdf65fa2f5a"],["/img/png/co.png","fc054ac219a476c5d11a10ea81993387"],["/img/png/f1.png","b2747deeff6a60fdbf63d4cb6bb207c3"],["/img/png/f2.png","82e92056a58300eb2b7a0e5285e39c71"],["/img/png/f3.png","883e85b6989e148d925c2d9975967754"],["/img/png/megacom.png","40fda66e22db039bc88288f89201e975"],["/img/png/menu.png","162acc5e4eef25ca2ed974a2faf07a9a"],["/img/png/sl1.png","fea3f6efff0efc7c600c4e0be0bfde9d"],["/img/png/sl2.png","46724d614cdcb524deb09ec04b9c830b"],["/img/png/sofa-from.png","f826e7f9162f36963b6a2c4c736ddc01"],["/img/png/t1.png","b1aadb37f41f3ac436847443b7f2a032"],["/img/png/t2.png","da4de389206e99d8d3a5b4b68d1e0b8f"],["/img/png/t3.png","60748900071b4aad93cebf6a6fe0859d"],["/img/png/t4.png","e11ad1b30759dd12686f8d902ee3a880"],["/img/png/t5.png","ac982bc9b14622078c3d805b00cca586"],["/img/png/t6.png","9e8d712de942dc71b9900fb8b903f527"],["/img/png/t7.png","a029e4311eb8ea9560c12bbea24f8003"],["/img/png/t8.png","975fd16a00b098a4e2d9cdc98b261d29"],["/img/png/t9.png","a5dc4b0581736a764a7b75de78fa48ed"],["/index.html","4d244bad1fbb1d96a09a31a495892947"],["/js/common.min.js","66388431c5e89440c2aa687a9578d7b0"],["/js/libs.min.js","2a5b7e942f380091e1050b470e95c867"],["/manifest.json","cd97fb57f20e6b285fc5398738a312e3"]];
var cacheName = 'sw-precache-v3--' + (self.registration ? self.registration.scope : '');


var ignoreUrlParametersMatching = [/^utm_/];



var addDirectoryIndex = function (originalUrl, index) {
    var url = new URL(originalUrl);
    if (url.pathname.slice(-1) === '/') {
      url.pathname += index;
    }
    return url.toString();
  };

var cleanResponse = function (originalResponse) {
    // If this is not a redirected response, then we don't have to do anything.
    if (!originalResponse.redirected) {
      return Promise.resolve(originalResponse);
    }

    // Firefox 50 and below doesn't support the Response.body stream, so we may
    // need to read the entire body to memory as a Blob.
    var bodyPromise = 'body' in originalResponse ?
      Promise.resolve(originalResponse.body) :
      originalResponse.blob();

    return bodyPromise.then(function(body) {
      // new Response() is happy when passed either a stream or a Blob.
      return new Response(body, {
        headers: originalResponse.headers,
        status: originalResponse.status,
        statusText: originalResponse.statusText
      });
    });
  };

var createCacheKey = function (originalUrl, paramName, paramValue,
                           dontCacheBustUrlsMatching) {
    // Create a new URL object to avoid modifying originalUrl.
    var url = new URL(originalUrl);

    // If dontCacheBustUrlsMatching is not set, or if we don't have a match,
    // then add in the extra cache-busting URL parameter.
    if (!dontCacheBustUrlsMatching ||
        !(url.pathname.match(dontCacheBustUrlsMatching))) {
      url.search += (url.search ? '&' : '') +
        encodeURIComponent(paramName) + '=' + encodeURIComponent(paramValue);
    }

    return url.toString();
  };

var isPathWhitelisted = function (whitelist, absoluteUrlString) {
    // If the whitelist is empty, then consider all URLs to be whitelisted.
    if (whitelist.length === 0) {
      return true;
    }

    // Otherwise compare each path regex to the path of the URL passed in.
    var path = (new URL(absoluteUrlString)).pathname;
    return whitelist.some(function(whitelistedPathRegex) {
      return path.match(whitelistedPathRegex);
    });
  };

var stripIgnoredUrlParameters = function (originalUrl,
    ignoreUrlParametersMatching) {
    var url = new URL(originalUrl);
    // Remove the hash; see https://github.com/GoogleChrome/sw-precache/issues/290
    url.hash = '';

    url.search = url.search.slice(1) // Exclude initial '?'
      .split('&') // Split into an array of 'key=value' strings
      .map(function(kv) {
        return kv.split('='); // Split each 'key=value' string into a [key, value] array
      })
      .filter(function(kv) {
        return ignoreUrlParametersMatching.every(function(ignoredRegex) {
          return !ignoredRegex.test(kv[0]); // Return true iff the key doesn't match any of the regexes.
        });
      })
      .map(function(kv) {
        return kv.join('='); // Join each [key, value] array into a 'key=value' string
      })
      .join('&'); // Join the array of 'key=value' strings into a string with '&' in between each

    return url.toString();
  };


var hashParamName = '_sw-precache';
var urlsToCacheKeys = new Map(
  precacheConfig.map(function(item) {
    var relativeUrl = item[0];
    var hash = item[1];
    var absoluteUrl = new URL(relativeUrl, self.location);
    var cacheKey = createCacheKey(absoluteUrl, hashParamName, hash, false);
    return [absoluteUrl.toString(), cacheKey];
  })
);

function setOfCachedUrls(cache) {
  return cache.keys().then(function(requests) {
    return requests.map(function(request) {
      return request.url;
    });
  }).then(function(urls) {
    return new Set(urls);
  });
}

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(cacheName).then(function(cache) {
      return setOfCachedUrls(cache).then(function(cachedUrls) {
        return Promise.all(
          Array.from(urlsToCacheKeys.values()).map(function(cacheKey) {
            // If we don't have a key matching url in the cache already, add it.
            if (!cachedUrls.has(cacheKey)) {
              var request = new Request(cacheKey, {credentials: 'same-origin'});
              return fetch(request).then(function(response) {
                // Bail out of installation unless we get back a 200 OK for
                // every request.
                if (!response.ok) {
                  throw new Error('Request for ' + cacheKey + ' returned a ' +
                    'response with status ' + response.status);
                }

                return cleanResponse(response).then(function(responseToCache) {
                  return cache.put(cacheKey, responseToCache);
                });
              });
            }
          })
        );
      });
    }).then(function() {
      
      // Force the SW to transition from installing -> active state
      return self.skipWaiting();
      
    })
  );
});

self.addEventListener('activate', function(event) {
  var setOfExpectedUrls = new Set(urlsToCacheKeys.values());

  event.waitUntil(
    caches.open(cacheName).then(function(cache) {
      return cache.keys().then(function(existingRequests) {
        return Promise.all(
          existingRequests.map(function(existingRequest) {
            if (!setOfExpectedUrls.has(existingRequest.url)) {
              return cache.delete(existingRequest);
            }
          })
        );
      });
    }).then(function() {
      
      return self.clients.claim();
      
    })
  );
});


self.addEventListener('fetch', function(event) {
  if (event.request.method === 'GET') {
    // Should we call event.respondWith() inside this fetch event handler?
    // This needs to be determined synchronously, which will give other fetch
    // handlers a chance to handle the request if need be.
    var shouldRespond;

    // First, remove all the ignored parameters and hash fragment, and see if we
    // have that URL in our cache. If so, great! shouldRespond will be true.
    var url = stripIgnoredUrlParameters(event.request.url, ignoreUrlParametersMatching);
    shouldRespond = urlsToCacheKeys.has(url);

    // If shouldRespond is false, check again, this time with 'index.html'
    // (or whatever the directoryIndex option is set to) at the end.
    var directoryIndex = 'index.html';
    if (!shouldRespond && directoryIndex) {
      url = addDirectoryIndex(url, directoryIndex);
      shouldRespond = urlsToCacheKeys.has(url);
    }

    // If shouldRespond is still false, check to see if this is a navigation
    // request, and if so, whether the URL matches navigateFallbackWhitelist.
    var navigateFallback = '';
    if (!shouldRespond &&
        navigateFallback &&
        (event.request.mode === 'navigate') &&
        isPathWhitelisted([], event.request.url)) {
      url = new URL(navigateFallback, self.location).toString();
      shouldRespond = urlsToCacheKeys.has(url);
    }

    // If shouldRespond was set to true at any point, then call
    // event.respondWith(), using the appropriate cache key.
    if (shouldRespond) {
      event.respondWith(
        caches.open(cacheName).then(function(cache) {
          return cache.match(urlsToCacheKeys.get(url)).then(function(response) {
            if (response) {
              return response;
            }
            throw Error('The cached response that was expected is missing.');
          });
        }).catch(function(e) {
          // Fall back to just fetch()ing the request if some unexpected error
          // prevented the cached response from being valid.
          console.warn('Couldn\'t serve response for "%s" from cache: %O', event.request.url, e);
          return fetch(event.request);
        })
      );
    }
  }
});







