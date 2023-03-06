;
var food_cat_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".wrap_cat_set .save").click(function () {
            var button_target = $(this);
            if (button_target.hasClass("disabled")) {
                common_ops.alert("正在处理，请不要重复提交");
                return;
            }

            var name_target = $(".wrap_cat_set input[name=name]");
            var name = name_target.val();

            if (name.length < 1) {
                common_ops.tip("请输入符合规范的姓名", name_target);
                return;
            }

            var weight_target = $(".wrap_cat_set input[name=weight]");
            var weight = weight_target.val();

            if (parseInt(weight) < 1) {
                common_ops.tip("请输入符合规范的权重", weight_target);
                return;
            }

            button_target.addClass("disabled");
            var data = {
                name: name,
                weight: weight,
                id: $(".wrap_cat_set input[name=id]").val()
            }

            $.ajax({
                url: common_ops.buildUrl("/food/cat-set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/food/cat");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                },
                error: function (error) {
                    var callback = null;
                    if (res.code == -1) {
                        callback = function () {
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert(error.msg, callback);
                }
            })
        })
    }
};
$(document).ready(function () {
    food_cat_set_ops.init();
})