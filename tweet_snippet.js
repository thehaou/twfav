// 0. setup
var tweetTotalList = [];
var tweetCurrentList = [];

var testStop = 2; // this is for testing purposes (stops execution early)
var sh = 0;

var requestLimit = 170; // technically 180, but we'll do 175 to account for initial loading of the page
var requestCounter = 0;
var delay = 3000; // in milliseconds. adjust if your browser takes longer than 3s to load a new batch of images
var timeoutDelay = 60 * 15 * 1000; // 15 min
var waiting = false;

var previousStatusCheckpoint = ''; // if we've already collected up to a certain point, stop once we run out of new stuff // TODO this needs testing; 1307348783517237248

// 0.5 helper function from http://bgrins.github.io/devtools-snippets/#console-save
console.log('beginning; will translate tweets every ' + delay/1000 + ' seconds');
(function(console) {

    console.save = function(data, filename) {

        if (!data) {
            console.error('Console.save: No data')
            return;
        }

        if (!filename) filename = 'console.json'

        if (typeof data === "object") {
            data = JSON.stringify(data, undefined, 4)
        }

        var blob = new Blob([data], {
                type: 'text/json'
            }),
            e = document.createEvent('MouseEvents'),
            a = document.createElement('a')

        a.download = filename
        a.href = window.URL.createObjectURL(blob)
        a.dataset.downloadurl = ['text/json', a.download, a.href].join(':')
        e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
        a.dispatchEvent(e)
    }
})(console)

var iID = setInterval(function scrape() {
        // 7. stop processing (and save) if the height hasn't changed
        if (sh == document.documentElement.scrollHeight && !waiting) {
            console.log('reached the bottom, saving JSON and stopping');
            console.save(tweetTotalList, 'tweets.json');
            console.log('transformed a total of ' + tweetTotalList.length + ' pictures into JSON');
            clearInterval(iID);
            return;
        }

        // 6. if request limit reached, pause ingestion for 15 min
        if (requestCounter == requestLimit) {
            clearInterval(iID);
            requestCounter = 0;
            iID = setInterval(scrape, timeoutDelay);
            waiting = true;
            console.log('request limit probably reached, waiting 15 minutes - please do not close this tab or switch away')
            return;
        }

        if (waiting) {
            clearInterval(iID);
            iID = setInterval(scrape, delay);
            waiting = false;
            console.log('starting ingest again')
            return;
        }


        // 1. turn image tweets into JSON (the image downloading happens separately in main.py)
        var dateTime = '';
        var batchNum = 0;
        var linkEls = document.querySelectorAll('[role="link"]')

        for (var i = 0; i < linkEls.length; i++) {
            let linkEl = linkEls[i];

            // 2. extract the name and date and jazz for each
            let child = linkEl.getElementsByTagName('time')[0];
            if (child !== undefined) {
                dateTime = child.dateTime;
                batchNum = 0; // for tweets with more than one image attached - this will uniquely identify the children

                // 4. add to the total list if previous elements exist
                if (tweetCurrentList.length !== 0) {
                    tweetTotalList = tweetTotalList.concat(tweetCurrentList);
                    tweetCurrentList = [];
                }

                continue;
            }

            var imageEl = linkEl.querySelector('[alt="Image"]');

            // 3. from within the node, get the media link; if there is no media link, skip because it's not an image.
            // Note this currently skips gifs and other animated media as well.
            if (imageEl !== null) {
                let httpsSplit = linkEl.href.split('/', 6)
                let username = httpsSplit[3];
                let status = httpsSplit[5];
                // Twitter default compression is ugly - we'll try and fetch the "large" version of the image
                let imageURL = imageEl.src.replace(/name=.*/gi, 'name=large');

                // 3.5 check for early execution end (we've reached stuff already parsed)
                if (status == previousStatusCheckpoint) {
                    console.log('reached tweet that has already been parsed, halting');
                    console.save(tweetTotalList, 'tweets.json');
                    console.log('transformed a total of ' + tweetTotalList.length + ' pictures into JSON');
                    clearInterval(iID);
                    return;
                }

                tweetCurrentList.push({
                    dateTime: dateTime,
                    imageURL: imageURL,
                    fileName: username + "_" + status + "_" + batchNum
                });

                batchNum += 1;
            }
        }

        // 5. scroll down the page if the batch is complete
        console.log('will start a new batch');
        console.log(tweetTotalList);

        sh = (document.documentElement.scrollHeight);
        document.documentElement.scrollTop = sh;

        requestCounter += 1;

        // following is for testing purposes (stops execution early)
//         testStop -= 1;
//         if (testStop == 0) {
//             console.log('stopping for testing purposes');
//             console.save(tweetTotalList, 'tweets.json');
//             clearInterval(iID);
//         }
    },
    delay);

