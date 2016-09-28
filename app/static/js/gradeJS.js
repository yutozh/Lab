// save password and username
// var defer = $.Deferred();

$(document).ready(function () {
    if ($.cookie("rmbUser") == "true") {
        $("#savepass").prop("checked", true);
        $("#inputStuNum").val($.cookie("username"));
        $("#inputPassword").val($.cookie("password"));
    }
    $('#copySignature').on('click', function (e) {
        e.preventDefault();
    }).zclip({
    path: 'https://cdn.bootcss.com/zclip/1.1.2/ZeroClipboard.swf',
    copy: function () {//复制内容
        return $("#privateInfo").text();
    },
    afterCopy: function () {//复制成功
        alertShow("复制成功,直接去粘贴吧~", "success");
    }
});

    $(window).bind("scroll", function(){
        var top = $(this).scrollTop(); // 当前窗口的滚动距离
        var alert_box = $("#div_alert");
        var m_t = alert_box.css("margin-top");
        alert_box.css({"margin-top":(-25 + parseInt(top)).toString()+"px"});
  });
});



function savePwd() {
    var username = $("#inputStuNum").val();
    $.cookie("username", username, {expires: 7});
    if ($("#savepass").prop("checked")) {
        var password = $("#inputPassword").val();
        $.cookie("rmbUser", "true", {expires: 7});
        $.cookie("password", password, {expires: 7});
    } else {
        $.cookie("rmbUser", "false", {expire: -1});
        $.cookie("password", "", {expires: -1});
    }
}

function checkInput() {
    var username = $("#inputStuNum").val();
    var password = $("#inputPassword").val();
    var captcha = $("#input_captcha").val();
    var alert = $("#alert_text");
    var wrapper = $('#wholewrapper');
    if (username == '') {

        alertShow("请输入学号!", "danger");
        return false;
    }
    if (password == '') {

        alertShow("请输入密码!", "danger");
        return false;
    }
    if (($("#not_auto").attr('class')).toString().indexOf("active") > -1 && captcha == '') {

        alertShow("请输入验证码!", "danger");
        return false;
    }
    wrapper.fadeOut();
    alert.text("");
    return true;
}

function onSubmit() {
    // alert($.cookie("username"));
    $('#wholewrapper').hide();
    if (checkInput()) {
        savePwd();
        var username = $("#inputStuNum").val();
        var password = $("#inputPassword").val();
        var captcha = '';
        var data = {};
        var captchaResult = '';
        changeBtn('disabled');
        if (($("#not_auto").attr('class')).toString().indexOf("active") > -1) {
            // 手动输入验证码
            captcha = $("#input_captcha");
            data = {"username": username, "password": password, "captcha": captcha.val()};
            // captchaResult = ajaxLogin(data);
            $.when(ajaxLogin(data, 0)).done(function (captchaResult) {
                if (captchaResult[0] == false) {

                    if (captchaResult[1] == "-1") {
                        alertShow("验证码错误", "danger");
                        captcha.val("");

                    } else if (captchaResult[1] == "-2") {
                        alertShow("学号或密码错误", "danger");
                    } else if (captchaResult[1] == "-3") {
                        alertShow("登陆超时", "danger");
                    } else {
                        alertShow("未知错误,错误代码:" + captchaResult[1], "danger");
                    }
                    changeCaptcha();
                    changeBtn("active");
                    return false;
                }
            });
        }
    else {
            // var socket = io.connect("http://" + document.domain + ":" + location.port);
            // socket.on("response",function (msg) {
            //     console.log(msg);
            //     var status = msg.status;
            //     var values = msg.values + '%';
            //     var bar = $("#progress_bar");
            //     bar.css({"width": values});
            //     bar.text(values)
            // });
            //
            // socket.emit('autoCaptcha', {data: "start"});

            // 自动识别验证码
            initBar();
            var bar = $("#progress_bar");
            var values = '0%';
            data = {"username": username, "password": password, "captcha": captcha};

            $.when(ajaxLogin(data, 0)).done(function (res) {

                $.when(ajaxLogin(data, 1)).done(function (res) {

                    $.when(ajaxLogin(data, 2)).done(function (res) {

                        $.when(ajaxLogin(data, 3)).done(function (res) {

                            $.when(ajaxLogin(data, 4)).done(function (res) {

                                $.when(ajaxLogin(data, 5)).done(function (res) {

                                });
                            });
                        });
                    });
                });
            });

            // captchaResult =;
            // if (captchaResult[0] == false) {
            //     if (captchaResult[1] == "-2") {
            //         alertShow("学号或密码错误", "danger");
            //         changeBtn("active");
            //         initBar();
            //         return false;
            //     }
            // }
            // else {
            //     finishBar('success');
            //     break;
            // }
            // if (i == 4) {
            //     finishBar('danger');
            //     alertShow("自动识别失败,请重试或手动输入", "danger");
            //     changeBtn("active");
            //     return false;
            // }
            // }
        }

        // postForGrade(captchaResult[1]);
        changeBtn("active");

    } else {
        return false;
    }
}


function alertShow(info, type) {
    var alert = $("#alert_text");
    var wrapper = $('#wholewrapper');
    var div = $("#div_alert");

    div.addClass("alert-" + type);
    alert.html(info);
    wrapper.fadeIn(100);
    setTimeout(function () {
        wrapper.fadeOut(200);
    }, 3000);
    setTimeout(function () {
        div.removeClass("alert-" + type);
    }, 3200);

}

function initBar() {
    var bar = $("#progress_bar");
    bar.prop("class", "progress-bar progress-bar-info");
    bar.css({"width": "0%"});
    bar.text("0%");
}

function finishBar(status) {
    var bar = $("#progress_bar");
    bar.prop("class", "progress-bar progress-bar-" + status);
    bar.css({"width": "100%"});
    bar.text("100%");
}

function changeBtn(status) {
    var submit_btn = $("#btn_submit");
    if (status == 'disabled') {
        submit_btn.text('查询中,请耐心等待哦~');
        submit_btn.attr('disabled', 'disabled');
    }
    else if (status == 'active') {
        submit_btn.text('查询');
        submit_btn.removeAttr('disabled');
    }
}

function changeCaptcha() {
    $("#img_captcha").attr("src", "/image?a=" + Math.random().toString());
}
function ajaxLogin(data, i) {
    var res = [];
    var defer = $.Deferred();
    if (i == 5) {
        res = [false, "-5"];
        finishBar('danger');
        alertShow("自动识别失败,请重试或手动输入", "danger");
        changeBtn("active");
        defer.reject(res);
    }

    else {
        $.ajax({
            url: '/gradeSubmit',
            data: data,
            dataType: 'json',
            type: 'post',
            // async: false,
            beforeSend: function () {
                values = ((i + 1) * 20).toString() + '%';
                var bar = $("#progress_bar");
                bar.css({"width": values});
                bar.text(values);
            },
            success: function (result) {
                if (result.res == "false") {
                    res = [false, result.session];
                    if (i != '-1' && res[1] == "-2") {
                        alertShow("学号或密码错误", "danger");
                        changeBtn("active");
                        initBar();
                        defer.reject(res);
                    }
                } else {
                    res = [true, result.session];
                    alertShow("<span class='glyphicon glyphicon-ok-circle'> 验证成功,正在跳转中...", "success");
                    $.cookie("JID", result.JID);
                    $.cookie("name", result.nameLable);
                    finishBar('success');
                    changeBtn("active");
                    postForGrade(res[1]);
                    defer.reject(res);
                }
                defer.resolve(res);  // 只在验证码识别错误时,执行该语句,继续下一次尝试
            }
        });
    }
    return defer.promise();
}

function onCheckSignature() {
    var signature = $("#checkSignature").val();
    var crypt = new JSEncrypt();
    var pri_key = "-----BEGIN RSA PRIVATE KEY-----\
MIICYAIBAAKBgQCXkoECMg49nYWVzs+GzADxeMAr2ZPoXw1fbwZWbjknphT9EkaS\
68Oih4A6mOloqyQtmI2W+5cbDGs9Jm13MtHgh9008V+XWujxCgJwfCrE90DhN7iG\
CmNdhmwR9Fj0xXJ1vetvJqyJHISNenuy6Y61LbrTqdqldZZjRtpfrTtH3wIDAQAB\
AoGAUSaPC63hEfwUWXCwi2sN1jrgKJoFJpQ9hKrcqcm5sBCrjBMM1fyEcbA6ZyUX\
UoLOi9rxc7Sf4ktz3vmDjo2iwuj1YwJtaEzVwUo/GEBBNZlB/6FOcJWVxPSyaNk6\
vihuM9BgE/+4MEAAbhaf4Ajinjo1n1tkSzpoEY8P8HnJh4ECRQDX2LDWSgz7GWif\
DGmaZw011zo9l0L+6jLEGJ0SdsnrUQm2TNWMeHifQnDpxWAB2w7h5h0M7kPCDy0k\
H7MsSWvtP7ZBOwI9ALPE3lRG4JdbGfSwRcmjeamU2vcC9Yw4/0VEhKnHi5Pu0+r1\
bl45+TWNXCStSmj9opbPcNRNWd/qtfBprQJFANGPJEEoq+muBZFFb9Hkc0LurzDV\
BsqPfrI8Y2NlySyaBR/lAP/cht+4lf+hDVE/6PcRfurq+QYTzfPggwhgUFSLItu5\
AjxQSFdSI+UhMxpAYIiKKGupBEVVkwi9+qZl9NeaSvdWtY4GnF0Rz6ov9FV2O73D\
baIy36lv5quAiH2ARHECRFoSqDp3QAUMTUHmmHeLMMfcUfmqhUccqHl7uuZKNsho\
0B3G5AU7B7q7PqFcSZYq+dzW1zrkxoFuT9H4x66inFZGL7cK\
-----END RSA PRIVATE KEY-----";
    crypt.setPrivateKey(pri_key);
    var res = crypt.decrypt(signature);
    if (res != null) {
        var list = res.split('|');
        var info = "姓名:" + list[3] + "\n" +
            "学号:" + list[4] + "\n" +
            "必修:" + list[0] + "\n" +
            "选修:" + list[1] + "\n" +
            "总分:" + list[2];
        alert("验证成功,详细信息如下:\n" + info);
    } else {
        alertShow("验证失败,请检查校验码是否完整", "warning");
    }
}

function onGetSignature() {
    $("#signaturePanel").fadeIn(500);
    $("#getSignature").hide();
    $("#copySignature").show();
}



function postForGrade(data) {
    // data 为CSRF
    setTimeout(function () {
        window.location.href = "/gradeDetail?csrf=" + data;
    }, 2000);
}


