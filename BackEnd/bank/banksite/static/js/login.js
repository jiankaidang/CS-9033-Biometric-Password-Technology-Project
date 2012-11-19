/**
 * User: Jiankai Dang
 * Date: 11/18/12
 * Time: 5:20 PM
 */
$(function () {
    $("#login_form").submit(function () {
        $.post($("#login_form").attr("action"), {
            uid:$("#uid").val(),
            password:$("#password").val()
        }, function (data) {
            if (!data.success) {
                alert(data.msg);
                return;
            }
            alert(1);
        });
        return false;
    });
});