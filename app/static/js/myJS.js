/**
 * Created by zyt on 16-8-28.
 */

$(window).ready(
    resize()
);

// window.addEventListener("resize", resize, false);

function resize() {

    // var containerH=$(window).height();
    // var containerW=$(window).width();
    // var $backimg = $("#backImg");
    // imgWid = parseInt($backimg.css("width"));
    // imgHei = parseInt($backimg.css("height"));
    // $backimg.css({"height":containerH});
    // var scale = parseInt(containerH) / imgHei;
    // $("#background").css({"width":containerW,"height":containerH});
    // $("#input").css({"width":imgWid*0.8*scale,"height":parseInt(containerH)*0.8});
    var containerH = $(window).height();
    var containerW = $(window).width();
    var $backimg = $("#backImg");
    $backimg.css({"height": containerH});
    imgWid = $backimg.css("width");
    imgHei = $backimg.css("height");

    var scale = parseInt(containerH) / imgHei;
    $("#background").css({"width": containerW, "height": containerH});
    $("#input").css({"width": parseInt(imgWid) * 0.8, "height": parseInt(containerH) * 0.8});
}

$("#input_btn").click(function () {
    var username = $("#input_name").val();
    if (username == ''){
        $("#prompt").html('你还什么都没输入呢╭(╯^╰)╮？');
        return;
    }
    var data = {"name": username};

    $.ajax({
        url: '/bookSearch',
        context: $("#input"),
        data: data,
        dataType: "json",
        type: "post",
        beforeSend: function () {
            $("#wholewrapper").fadeIn();
        },
        success: function (data) {
            if (data['result'] == 'False') {
                $("#prompt").html('没有查到喔T﹏T');
                $("#wholewrapper").fadeOut();
                return false;
            }
            else {
                var htmlContent = '';
                var price = 0.0;
                for (var p in data) {
             item='<tr style="position: relative">\
                <td>'+ data[p][0] +'</td>\
                <td>'+ data[p][1][0]+'</td>\
                <td style="position: absolute;right: 1px">'+ data[p][1][3]+'</td>\
            </tr>';
                    htmlContent += item;
                    price += parseFloat(data[p][1][3])
                }
                htmlRes = '<p style="margin-bottom: 1rem">\
        亲爱的<span id="username">' + username +'</span>同学,以下是你的教材预定情况:\
    </p>\
                <table class="zebra">\
        <thead>\
            <tr>\
                <th>编号</th>\
                <th>书名</th>\
                <th>折后价</th>\
            </tr>\
        </thead>\
        <tfoot>\
        </tfoot>\
        <tbody>'+
        htmlContent
                    +'</tbody>\
    </table>\
<p>\
        总计<span id="booknum">' + data.length +'</span>本教材, 总价格\
        <span id="bookprice">'+ price.toFixed(2) +'</span>元.\
    </p>\
                    <p style="margin-top: 1.5rem;">\
        如有任何问题请及时联系你们的学委哦~\
    </p>';
                $(this).html(htmlRes);
                $("#wholewrapper").fadeOut();
            }
        }
    })
});