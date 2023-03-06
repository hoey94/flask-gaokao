;
var user_reset_pwd_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $("#save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var old_password_target = $("#old_password");
            var old_password = old_password_target.val();

            var new_password_target = $("#new_password");
            var new_password = new_password_target.val();

            if (!old_password || old_password.length < 2) {
                common_ops.tip("请输入原密码", old_password_target);
            }

            if (!new_password || new_password.length < 2) {
                common_ops.tip("请输入新密码", new_password_target);
            }

            btn_target.addClass('disabled');

            var data = {
                old_password: old_password,
                new_password: new_password
            }

            $.ajax({
                url: common_ops.buildUrl("/user/reset-pwd"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert(res.msg, callback);
                },
                error: function (error) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == -1) {
                        callback = function () {
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert(error.msg, callback);
                }
            })

        });
    }
};

$(document).ready(function () {
    user_reset_pwd_ops.init();
})