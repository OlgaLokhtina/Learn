//document.getElementById('main-change').addEventListener("submit", checkForm);


function checkForm(el) {
    //event.preventDefault();
    var text1 = document.getElementById('pass_1');
    var text2 = document.getElementById('pass_2');
    var text3 = document.getElementById('pass_3');
    if (text1.value == "" || text2.value == "" || text3.value == "") {
        alert('Заполните все поля!');
        return false;
    }
    else if (text2.value != text3.value) {
        alert('Введенные пароли не совпадают!');
        return false;
    }
    else {
        return true;
    }
}

//document.getElementById('ch').addEventListener("click", onClickButton);

function onClickButton(el) {
    //event.preventDefault();
    var text1 = document.getElementById('pass_1');
    var text2 = document.getElementById('pass_2');
    var text3 = document.getElementById('pass_3');
    var but = document.getElementById('ch');
    if (text1.type == "password") {
        text1.type = "text";
        text2.type = "text";
        text3.type = "text";
        but.innerHTML = 'Скрыть пароли';
    }
    else {
        text1.type = "password";
        text2.type = "password";
        text3.type = "password";
        but.innerHTML = 'Показать пароли';
    }

}