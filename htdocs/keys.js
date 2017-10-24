var _qrstr = {
    "keyonly"    : function(ssid,key,auth) { return key; },
    "zxing"      : function(ssid,key,auth) { return "WIFI:S:" + ssid + ";T:" + auth.substring(0,3) + ";P:" + key + ";;"; },
    "qrsetup"    : function(ssid,key,auth) { return "S=" + ssid + "\r\n" + "KA=" + key + "\r\n" + "E=Mixed\r\n" + "M=000000000000\r\n"; },
    "qrconnect"  : function(ssid,key,auth) { return "WI:\r\n" + "SS:" + ssid + "\r\n" + "EN:" + auth.substring(0,3) + "\r\n" + "PA:" + key + "\r\n"; }
};
var _qrapp = {
    "zxing"      : { "Android" : "https://play.google.com/store/apps/details?id=com.google.zxing.client.android" },
    "qrsetup"    : { "iOS" : "http://itunes.apple.com/jp/app/id533032026", "Android" : "https://play.google.com/store/apps/details?id=jp.buffalo.aoss.qrsetup" },
    "qrconnect"  : { "iOS" : "http://itunes.apple.com/jp/app/id482536782", "Android" : "https://play.google.com/store/apps/details?id=jp.iodata.android.wificonnect" }
};

function generate_qrcode(data) {
    $.each(_qrstr, function(mode, qrfunc) {
        var modediv = $('<div id="' + mode + '"></div>');
        modediv.append('<h2><a name="' + mode + '">' + mode + '</a></h2>');

        var qrappdiv = $('<div id="' + mode + '_url"></div>');
        if(mode in _qrapp) {
            $.each(_qrapp[mode], function(appname, appurl) {
                qrappdiv.append('<a href="' + appurl + '" target="_blank">' + appname + '</a>');
                qrappdiv.append('&nbsp;');
            });
        }
        modediv.append(qrappdiv);

        var qrtable = $('<table id="qrtable_' + mode + '"></table>');
        var isEven = function(num) { return (num % 2 == 0) ? true : false; };
        var i = 0;

        $.each(data, function(label, id2key) {
            var ssid   = id2key[0];
            var keys   = id2key[1];
            var auth   = id2key[2];
            var qrid   = ["qrcode", label, mode].join('_');
            var qrdiv = $('<div id="' + qrid + '">');
            var qrcol = $('<tr></tr>');
            var qrstr  = qrfunc(ssid,keys,auth);

            if(isEven(i)) {
                qrcol.append('<td class="label_even">' + label + '</td>');
                qrcol.append('<td>-&gt;</td>');
                qrcol.append(qrdiv);
            }
            else {
                qrcol.append(qrdiv);
                qrcol.append('<td>&lt;-</td>');
                qrcol.append('<td class="label_odd">' + label + '</td>');
            }

            qrdiv.qrcode(qrstr);
            qrtable.append(qrcol);
            i++;
        });

        modediv.append(qrtable);
        modediv.append('<hr />');
        $('#Wi-Fi_Keys').append(modediv);
    });
}

function generate_raw (data) {
    var header = '#LABEL\tAUTH    \tSSID                           \tKEY\n';
    $("#Wi-Fi_Raws").prepend(header);
    $.each(data, function(label, id2key) {
        var ssid   = id2key[0];
        var keys   = id2key[1];
        var auth   = id2key[2];
        var raw = [label, auth, ssid, keys].join('\t');
        $("#Wi-Fi_Raws").append(raw + "\n");
    });
}

function generate_content_link() {
    for(var mode in _qrstr) {
        $("#Wi-Fi_Content").append('<li><a href="#' + mode + '">' + mode + '</a><br />');
    }
    $("#Wi-Fi_Content").after('<hr />');
}

$(function() {
    generate_content_link()
    $.getJSON("keys.json", function(json) {
        generate_qrcode(json);
        generate_raw(json);
    });
});
