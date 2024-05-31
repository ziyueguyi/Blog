const main = document.querySelector('.main');
const btn = document.querySelector('.btn');
const signInBox = document.querySelector('.signInBox');
btn.onclick = () => {
    if (main.className.indexOf('active') !== -1) {
        main.className = 'main';
        setTimeout(() => {
            signInBox.innerText = '注册内容区';
        }, 500);
    } else {
        main.className = 'main active';
        setTimeout(() => {
            signInBox.innerText = '登录内容区';
        }, 500);
    }
};
