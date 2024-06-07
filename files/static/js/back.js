// 页面加载时自动加载菜单
window.onload = function () {
    let url = ""
    let method = "OPTIONS"
    $.ajax({
        url: url, //要请求的后端地址
        type: method, //数据发送的方式(POST或者GET)
        // data: user_info, //需要传递的参数
        dataType: "json", //后端返回的数据格式
        success: function (result) {//ajax请求成功后触发的方法
            result["data"].forEach(function (tr) {
                if (tr["page_level"] === 0) {
                    const new_span = $('<span>').text(tr["page_name"]);
                    const new_li = $('<li class="lc_du_l">').append(new_span);
                    $("#lc_du").append(new_li);
                }
            })
        },
        error: function () {//ajax请求失败后触发的方法
            console.log('Send Request Fail..');
        }
    });
};