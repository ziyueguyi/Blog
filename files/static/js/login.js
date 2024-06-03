const main = document.querySelector('.main');
const btn = document.querySelector('.btn');
const reg = document.querySelector('.signInBox').querySelectorAll(".reg");
const but_or_reg = document.querySelector('.but_or_reg');
// 登录和注册切换功能
btn.onclick = () => {
    if (main.className.indexOf('active') !== -1) {
        main.className = 'main';
        setTimeout(() => {
            reg.forEach(function (tr) {
                tr.style.display = "none";
            });
            but_or_reg.value = "登录";
        }, 500);
    } else {
        main.className = 'main active';
        setTimeout(() => {
            reg.forEach(function (tr) {
                tr.style.display = "inline";
            });
            but_or_reg.value = "注册";
        }, 500);
    }
};
// 点击登录和注册按钮
but_or_reg.onclick = () => {
    let url = ""
    let user_info = {
        "account": document.querySelector('#account').value,
        "password": document.querySelector('#password').value
    }
    let method;
    if (but_or_reg.value === "登录") {
        method = "OPTIONS"
    } else {
        user_info["nick_name"] = document.querySelector('#nick_name').value;
        user_info["email"] = document.querySelector('#email').value;
        user_info["birthday"] = document.querySelector('#birthday').value;
        user_info["password"] = document.querySelector('#password').value;
        let sex = "0"
        document.getElementsByName("sex").forEach(function (tr) {
            if (tr.checked) {
                sex = tr.value
            }
        });
        user_info["sex"] = sex
        method = "POST"
    }

    $.ajax({
        url: url, //要请求的后端地址
        type: method, //数据发送的方式(POST或者GET)
        data: user_info, //需要传递的参数
        dataType: "json", //后端返回的数据格式
        success: function (result) {//ajax请求成功后触发的方法
            if (result["code"] === 200) {
                window.location.href = result["msg"]
            } else {
                Alert(result["msg"]); //result为响应内容
            }
        },
        error: function () {//ajax请求失败后触发的方法
            console.log('Send Request Fail..');
        }
    });
};
