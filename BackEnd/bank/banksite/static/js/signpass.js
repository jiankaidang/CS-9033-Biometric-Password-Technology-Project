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
        '<p>First time login with SignPass?</p>' +
        '<p style="font-size:0.8em">If yes, please login to your bank account first, and then connect with SignPass!</p>' +
        '</div>');
    $("#SignPass").click(function () {
        if ($.cookie("uid")) {
            openSignPassWindow();
            return;
        }
        $.post("/signpass_login", {
            service_uid:$("#uid").val()
        }, function (data) {
            if (!data.success) {
                login_form.data(LOGIN_CHECK_SUCCEEDED, false);
                $("#dialog").dialog({
                    buttons:[
                        {
                            text:"OK",
                            click:function () {
                                $(this).dialog("close");
                                $("#uid").focus();
                            }
                        }
                    ],
                    modal:true,
                    title:"Login with SignPass"
                });
                return;
            }
            login_form.data(LOGIN_CHECK_SUCCEEDED, true).submit();
        });
    });
});
function openSignPassWindow() {
    window.open("http://192.168.0.15:8000/signpass/chase/" + $("#service_uid").val() + "/bindRequestFromService", "SignPass");
}