function main() {
    
    var MAXLOGLINES = 15;
    
    var logElem = document.querySelector('.logcntnr .log')
        , readlineElem = document.querySelector('.logcntnr input')
        , aws
        , ttsws
        ;
    
    function log(msg) {
        var lines = logElem.textContent.split('\n');
        if (lines.length > MAXLOGLINES) {
            lines.shift();
        }
        lines.push(msg.trim());
        logElem.textContent = lines.join('\n')
    }
    
    for (var i=0; i<MAXLOGLINES; i++) {
      log('');
    }

    //Globalize these
    window.globals = { sendData: function(output) {
                            log(output);
                            aws.send(output + '\n');
                       },
                       connectData: function(addr) {
                            dataConnect(addr);
                       },
                       disconnectData: function() {
                            aws.close();
                       }
    }
    
    readlineElem.addEventListener('keypress', function (e) {
        var key = e.which || e.keyCode;
        if (key == 13) {
            var d = readlineElem.value;
            log(d);
            aws.send(d + '\n');
        }
    });

    function dataConnect(addr) {
        log('DATA CONNECT: '+ addr);
      
        var dataIn = "";
        
        aws = new WebSocket(addr + "/data");

        aws.onopen = function() {
            $('.connect-data_websocket').hide();
            $('.disconnect-data_websocket').show();
        };
      
        aws.onclose = function(ev) {
            log('DATA DISCONNECTED: ' + ev.reason);
            $('.connect-data_websocket').show();
            $('.disconnect-data_websocket').hide();
        };
        
        aws.onmessage = function(ev) {
            for (var i = 0, len = ev.data.length; i < len; i++) {
                if(ev.data[i] == '\n'){
                    processData(dataIn);
                    dataIn = "";
                } else {
                    if(ev.data[i] == '\0'){
                        dataIn += " ";
                    } else {
                        dataIn += ev.data[i];
                    }
                }
            }
        };
        
        aws.onerror = function(ev) {
            log('DATA ERROR: '+ JSON.stringify(ev));
        };
        
    }
    
    function processData(data){
	log('>: ' + data);
        try {
            var json = JSON.parse(data);
        } catch (e) {
            return;
        }
   
        if(json.source == "arduino"){
            log('RAW: ' + data);
        } else if(json.source == "response") log('RESPONSE: ' + json.response); else log('RAW: ' + data);
    }
    
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
         //Tab toggle
    });

    $('.reset-iframe').click(function() {
        var thisIframe = $(this).attr('rel');
	var currentState = 	(thisIframe).attr('src');
	function removeSrc() {
            $(thisIframe).attr('src', '');
        }
	setTimeout (removeSrc, 50);
	function replaceSrc() {
            $(thisIframe).attr('src', currentState);
        }
	setTimeout (replaceSrc, 50);
    });

    $('.connect-data_websocket').click(function() {
        $('.connect-websocket').hide();
        window.globals.connectData(ENDPOINT);
        console.log("DATA CONNECT");
    });
	
    $('.disconnect-data_websocket').click(function() {
        $('.disconnect-websocket').hide();
        window.globals.disconnectData();
        console.log("DATA DISCONNECT");
    });
    
    $('.show-controls').click(function() {
        $('.show-controls').hide();
        $('.hide-controls').show();
        $('#controlCanvas').show();
    });
    $('.hide-controls').click(function() {
        $('.show-controls').show();
        $('.hide-controls').hide();
        $('#controlCanvas').hide();
    });    
    $('.show-controls').hide();
    
    setTimeout (dataConnect(ENDPOINT), 500);
    
};
