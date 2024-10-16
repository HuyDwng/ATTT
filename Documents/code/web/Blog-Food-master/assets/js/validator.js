//Đối tượng
function Validator(options) {

    var selectorRules = {};

    //Hàm validate
    function validate(inputElement, rule) {
        var errorElement = inputElement.parentElement.querySelector(options.errorSelector);
        var errorMessage;
        //lấy ra các rules của selector
        var rules = selectorRules[rule.selector];
        //Lặp qua từng rule và kiểm tra
        //Có lỗi thì dừng kiểm
        for (var i = 0; i < rules.length; ++i) {
            errorMessage = rules[i](inputElement.value);
            if (errorMessage) break;
        }

        if(errorMessage) {
            errorElement.innerText = errorMessage;
            inputElement.parentElement.querySelector('.form-mess').classList.add('invalid');
            inputElement.parentElement.querySelector('input').classList.add('invalidinput');
        } else {
            errorElement.innerText = '';
            inputElement.parentElement.querySelector('.form-mess').classList.remove('invalid');
            inputElement.parentElement.querySelector('input').classList.remove('invalidinput');
        }
    }
    // Lấy element của form cần validate
    var formElement = document.querySelector(options.form);

    if(formElement) {
        //Khi submit form
        formElement.onsubmit = function (e) {
            e.preventDefault();

            //Lặp từng rule và validate
            options.rules.forEach(function (rule) {
                var inputElement = formElement.querySelector(rule.selector);
                validate(inputElement, rule);
            });
        }
        //Lặp rule và xử lý
        options.rules.forEach(function (rule) {
            //Lưu lại các rules cho mỗi input

            if(Array.isArray(selectorRules[rule.selector])) {
                selectorRules[rule.selector].push(rule.test);
            }   else {
                selectorRules[rule.selector] = [rule.test];
            }
            var inputElement = formElement.querySelector(rule.selector);

            if(inputElement) {
                //Trường hợp blur khỏi input
                inputElement.onblur = function () {
                    validate(inputElement, rule);
                }
                //Trường hợp khi đang nhập
                inputElement.oninput = function () {
                    var errorElement = inputElement.parentElement.querySelector(options.errorSelector);
                    errorElement.innerText = '';
                    inputElement.parentElement.querySelector('.form-mess').classList.remove('invalid');
                    inputElement.parentElement.querySelector('input').classList.remove('invalidinput');
                }
            }
        });
    }

}


//Định nghĩa rules
Validator.isRequired = function(selector) {
    return {
        selector: selector,
        test: function(value) {
            return value.trim() ? undefined : 'Vui lòng nhập thông tin' 
        }
    };
}

Validator.isEmail = function(selector) {
    return {
        selector: selector,
        test: function(value) {
            var regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
            return regex.test(value) ? undefined : 'Đây không phải là email';
        }
    };
}

Validator.minLength = function(selector, min) {
    return {
        selector: selector,
        test: function(value) {
            return value.length >= min ? undefined : 'Vui lòng nhập tối thiểu ' + min + ' ký tự';
        }
    };
}

Validator.isConfirmed = function (selector, getConfirmValue) {
    return {
        selector: selector,
        test: function(value) {
            return value === getConfirmValue() ? undefined : 'Mật khẩu không trùng khớp';
        }
    };
}