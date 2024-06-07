let menu_list = null
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
            menu_list = result["data"]
            let lc_du = $("#lc_du")
            lc_du.empty()
            menu_list.forEach(function (tr) {
                if (tr["page_level"] === 0) {
                    const new_span = $('<span>').text(tr["page_name"]).attr("s_id", tr["ID"]);
                    const new_li = $('<li class="lc_du_l" >').append(new_span);
                    lc_du.append(new_li);
                }
            })
            lc_du.on("click", "span", show_menu)
            lc_du.find("span").first().trigger("click")
        },
        error: function () {//ajax请求失败后触发的方法
            console.log('Send Request Fail..');
        }
    });
};


function show_menu() {
    let s_id = $(this).attr("s_id")
    let ld_u = $("#rh_ld_u")
    ld_u.empty()
    $("#rb_dls").text($(this).text())
    menu_list.forEach(function (tr) {
        if (s_id === String(tr["parent_id"]) && tr["page_level"] === 1) {
            const new_span = $('<span>').text(tr["page_name"]).attr("s_id", tr["ID"]);
            const new_li = $('<li class="rh_ld_ul" >').append(new_span);
            ld_u.append(new_li);
        }
    });
    ld_u.on("click", "li", show_page)
    let li_first = ld_u.find("li").first()
    if (li_first.text() !== '') {
        li_first.trigger("click")
    } else {
        $("#rb_drs").text(null)
    }
    return true
}

function show_page() {
    $("#rb_drs").text($(this).text())
}