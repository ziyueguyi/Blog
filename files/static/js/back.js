var del = document.getElementsByClassName('a_del')
for (let i = 0; i < del.length; i++) {
    del[i].onclick = function () {
        del[i].parentNode.parentNode.parentNode.remove()
    }
}
// document.querySelector('.h_icon2').onclick = get_head_dir
function get_head_dir() {
    let url = ""
    $.ajax({
        url: url, //要请求的后端地址
        type: "OPTIONS", //数据发送的方式(POST或者GET)
        dataType: "json", //后端返回的数据格式
        success: function (result) {//ajax请求成功后触发的方法
            if (result["code"] === 200) {
                Alert(result["msg"] + "3")
            } else {
                Alert(result["msg"]+"2"); //result为响应内容
            }
        },
        error: function () {//ajax请求失败后触发的方法
            Alert("msg","1"); //result为响应内容
        }
    });
}
