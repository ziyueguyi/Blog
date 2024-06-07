// 页面加载时自动加载菜单
window.onload = function () {
    let url = ""
    let method = "OPTIONS"
    Alert("1234")
    $.ajax({
        url: url, //要请求的后端地址
        type: method, //数据发送的方式(POST或者GET)
        // data: user_info, //需要传递的参数
        dataType: "json", //后端返回的数据格式
        success: function (result) {//ajax请求成功后触发的方法
            if (result["code"] === 200) {
                Alert(result["msg"] + "1")
            } else {
                Alert(result["msg"] + "2"); //result为响应内容
            }
        },
        error: function () {//ajax请求失败后触发的方法
            console.log('Send Request Fail..');
        }
    });
};