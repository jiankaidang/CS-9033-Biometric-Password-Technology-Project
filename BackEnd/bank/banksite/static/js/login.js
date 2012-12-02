/**
 * User: Jiankai Dang
 * Date: 11/18/12
 * Time: 5:20 PM
 */
$(function () {
    var LOGIN_CHECK_SUCCEEDED = 'login_check_succeeded', login_form = $("#login_form");
    login_form.on("submit", function () {
        if (login_form.data(LOGIN_CHECK_SUCCEEDED)) {
            return true;
        }
        $.post("/login_check", {
            uid:$("#uid").val(),
            password:$("#password").val()
        }, function (data) {
            if (!data.success) {
                login_form.data(LOGIN_CHECK_SUCCEEDED, false);
                alert(data.msg);
                return;
            }
            login_form.data(LOGIN_CHECK_SUCCEEDED, true).submit();
        });
        return false;
    });
});