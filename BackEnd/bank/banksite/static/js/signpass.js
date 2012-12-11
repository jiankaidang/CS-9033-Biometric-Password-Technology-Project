/**
 * User: Jiankai Dang
 * Date: 11/19/12
 * Time: 12:21 AM
 */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain:false, // obviates need for sameOrigin test
    beforeSend:function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});
var backEndIP = "http://128.238.243.63:8000";
var service_uid, type = "bind";
$(function () {
    $(document.body).append('<div id="dialog" style="display: none;">' +
        '<p>First time login with SignPass?</p>' +
        '<p style="font-size:0.8em">If yes, please login to your bank account first, and then connect with SignPass!</p>' +
        '</div>');
    $("#SignPass").click(function () {
        if ($.cookie("uid")) {
            openSignPassWindow();
            return;
        }
        $.post("/login_check", {
            uid:$("#uid").val(),
            password:""
        }, function (data) {
            if (!data.success && data.code) {
                alert(data.msg);
                return;
            }
            service_uid = data.uid;
            type = "verify";
            openSignPassWindow();
            /*$.ajax(backEndIP + "/signpass/service/serviceLoginRequest", {
             data:{
             service_uid:data.uid,
             service_name:"chase"
             },
             dataType:"jsonp",
             success:function (data) {
             if (!JSON.parse(data).success) {
             alert(data.msg);
             return;
             }
             var intervalID = window.setInterval(function () {
             $.post(backEndIP + "/signpass/service/loginRequestPoll", {
             service_name:$("#service_name").val(),
             service_uid:$("#service_uid").val()
             }, function (data) {
             if (JSON.parse(data).success) {
             window.clearInterval(intervalID);
             location.href = "/signpass_login?uid=" + $("#uid").val();
             }
             });
             }, 3000);
             setTimeout(function () {
             window.clearInterval(intervalID);
             alert("Sorry! Connection with SignPass failed!");
             }, 180000);
             }
             });*/
        });
    });
});
function openSignPassWindow() {
    window.open(backEndIP + "/signpass/chase/" + (service_uid || $("#service_uid").val()) + "/bindRequestFromService?type=" + type, "SignPass");
}