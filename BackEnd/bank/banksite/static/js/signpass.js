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
$(function () {
    $(document.body).append('<div id="dialog" style="display: none;">' +
        'First time login with SignPass?<br>' +
        'If yes, please login to your bank account!' +
        '</div>');
    $("#SignPass").click(function () {
        if ($.cookie("uid")) {
            openSignPassWindow();
            return;
        }
        $("#dialog").dialog({
            buttons:[
                {
                    text:"No",
                    click:function () {
                        openSignPassWindow();
                        $(this).dialog("close");
                    }
                },
                {
                    text:"Yes",
                    click:function () {
                        $(this).dialog("close");
                        $("#uid").focus();
                    }
                }
            ],
            modal:true,
            title:"Login with SignPass"
        });
    });
});
function openSignPassWindow() {
    window.open("http://192.168.0.1:8000/signpass/service", "SignPass");
}