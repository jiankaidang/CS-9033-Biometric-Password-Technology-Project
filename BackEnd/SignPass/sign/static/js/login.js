/**
 * User: Jiankai Dang
 * Date: 11/18/12
 * Time: 5:20 PM
 */
$(function () {
    $("#login_form").submit(function () {
        var login_form = $(this);
        $.post("/signpass/service/checkBinding", {
            username:$("#username").val(),
            service_name:$("#service_name").val(),
            service_uid:$("#service_uid").val()
        }, function (data) {
            data = JSON.parse(data);
            if (!data.success) {
                alert(data.msg);
                return;
            }
            var intervalID = window.setInterval(function () {
                $.post("/signpass/service/bindRequestPoll", {
                    username:$("#username").val(),
                    service_name:$("#service_name").val(),
                    service_uid:$("#service_uid").val()
                }, function (data) {
                    if (JSON.parse(data).success) {
                        window.clearInterval(intervalID);
                        alert("Successfully connected with SignPass!");
                    }
                });
            }, 3000);
            setTimeout(function () {
                window.clearInterval(intervalID);
                alert("Sorry! Connection with SignPass failed!");
            }, 180000);


            /*         websocket = new WebSocket("ws://192.168.0.15:8000/signpass/service/bind");
             websocket.onmessage = function(evt) {
             onMessage(evt)
             };
             websocket.onerror = function(evt) {
             onError(evt)
             };

             websocket.send("websocket sending");

             //JSON.stringify({username:$("#username").val(), service_name:$("#service_name").val(),service_uid:$("#service_uid").val() })
             function onMessage(evt) {
             alert("get message");
             websocket.close();
             }
             function onError(evt) {
             alert(evt.data);
             }
             */

        });
        return false;
    });
});