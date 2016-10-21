"use strict";
var page = require('webpage').create(),
    system = require('system');

function onFirstPageReady() {
    // no 'playurl' found by far, proceed to the next stage.
    var cid = page.evaluate(function() {
        return window.cid;
    })
    if (undefined === typeof cid) {
        console.log("Error: invalid url");
    }
    // console.log("CID found: " + cid);
    page.open("http://www.bilibili.com/html/html5player.html?cid="+cid, function() {
        var checkCount = 0;
        function crs() {
            setTimeout(function() {
                if (page.found) {
                    phantom.exit();
                }
                var readyState = page.evaluate(function() {
                    return document.readyState;
                });
                // console.log("Second ready state"+readyState);
                if("complete" === readyState || checkCount > 10) {
                    console.log("Error: timeout.");
                    phantom.exit();
                }
                else {
                    checkCount = checkCount + 1;
                    crs();
                }
            }, page.timeouttime);
        }
        crs();
    });
}

if (system.args.length === 1) {
    console.log('Usage: papapabili.js <URL> [timeout]');
    phantom.exit(1);
} else {
    page.settings = {
        javascriptEnabled: true,
        loadImages: false,
        userAgent: "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"// "Mozilla/5.0 (Linux; Android 6.0.1; SHV36 Build/S7150; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/50.0.2661.86 Mobile Safari/537.36"
    };
    page.timeouttime = system.args[2]?(Number(system.args[2])/10):200;
    console.log(page.timeouttime);
    page.address = system.args[1];
    page.found = false;
    page.onResourceRequested = function (req) {
        var rurl = req.url;
        if(rurl.indexOf("playurl") !== -1) {
            console.log("Target found: " + rurl);
            // page.render("./temp/beforeexit.png");
            page.found = true;
            // phantom.exit();
        }
    };

    page.open(page.address, function (status) {
        var title = page.evaluate(function() {
            return document.title;
        });
        console.log("Title: "+title);
        var checkCount = 0;
        function checkReadyState() {
            setTimeout(function() {
                if (page.found) {
                    phantom.exit();
                }
                var readyState = page.evaluate(function() {
                    return document.readyState;
                });
                // console.log("first ready state: "+readyState);
                if("complete" === readyState || checkCount > 10) {
                    onFirstPageReady();
                }
                else {
                    checkCount = checkCount + 1;
                    checkReadyState();
                }
            }, page.timeouttime);
        }
        checkReadyState();
    });
}