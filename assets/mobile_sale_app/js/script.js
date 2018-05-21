sorting_product();
validate_user_info();
change_delivery_charge();
update_status();
render_rating();




function addToCart() {
    $.ajax({
        url: "add_to_cart/",
        type: "POST",
        data: {product_id: $()}
    })
}

function change_delivery_charge() {
    $('#id_kind_delivery').on('change', function (e) {
        var valueSelected = this.value;
        if (valueSelected == 'F') {
            console.log('OK');
            $('#id_delivery_charge').html('20,000 đ');
        }
        else {
            console.log('Not OK');
            $('#id_delivery_charge').html("0 đ");
        }
    });
}

function update_status() {
    $('#id_status').on('change', function (e) {
        var valueSelected = this.value;
        console.log(valueSelected);
        if (valueSelected == 1) {
            console.log('key 1');
            $('#id_status_selected').val('1');
        }
        else if (valueSelected == 2) {
            console.log('key 2');
            $('#id_status_selected').val('2');
        }
        else {
            console.log('key 0');
            $('#id_status_selected').val('0');
        }
    });
}

function sorting_product() {
    $('#lbsort').on('change', function (e) {
        window.location = this.options[this.selectedIndex].value;
    })
}

// $(function () {
//     console.log('CC');
//     $('#id_form_user_info').validate({
//         rules: {
//             id_name: 'require',
//             id_phone_no: {
//                 require: true,
//                 phone: true
//             },
//             id_birth_day: {
//                 require: true,
//                 date: true
//             },
//             id_address: "require",
//             id_email: {
//                 email: true
//             },
//
//         },
//         messages: {
//             id_name: 'Vui lòng điền họ và tên',
//             id_phone_no: 'Vui lòng điền SĐT nhận hàng',
//             id_birth_day: 'Vui lòng nhập đúng định dạng ngày',
//             id_address: "Vui lòng điền địa chỉ nhận hàng"
//         },
//         submitHandler: function (form) {
//             form.submit();
//
//         }
//     });
// });

function isValidDate(str) {
  var d = moment(str,'D/M/YYYY');
  if(d == null || !d.isValid()) return false;

  return str.indexOf(d.format('D/M/YYYY')) >= 0
      || str.indexOf(d.format('DD/MM/YYYY')) >= 0
      || str.indexOf(d.format('D/M/YY')) >= 0
      || str.indexOf(d.format('DD/MM/YY')) >= 0;
}

function validate_user_info() {
    $('#id_form_user_info').on('submit', function (e) {
        var phone = document.getElementById("id_phone_no").value;
        var phone_pattern = /^[0-9]{10,11}$/;
        if (!phone.match(phone_pattern)) {
            $('#phone').addClass('has-error');
            $('#phone_err').removeClass('hidden');
            return false;
        }
        var social_id = document.getElementById('id_social_id').value;
        var social_id_pattern = /^\d{9,11}$/;
        if (!social_id.match(social_id_pattern)) {
            console.log('False');
            $('#social_id').addClass('has-error');
            $('#social_err').removeClass('hidden');
            return false;
        }
        return true;
    });
    return;
}

function validate_payment_form() {
    $('#payment-form').on('submit', function (e) {
        var phone = document.getElementById("id_phone_no").value;
        var phone_pattern = /^[0-9]{10,11}$/;
        if (!phone.match(phone_pattern)) {
            $('#phone').addClass('has-error');
            $('#phone_err').removeClass('hidden');
            return false;
        }
        var social_id = document.getElementById('id_social_id').value;
        var social_id_pattern = /^\d{9,11}$/;
        if (!social_id.match(social_id_pattern)) {
            console.log('False');
            $('#social_id').addClass('has-error');
            $('#social_err').removeClass('hidden');
            return false;
        }
        return true;
    });
    return;
}

function render_rating() {
    var stars = document.getElementsByClassName('ls');
    $('#s1').click(function () {
        change_color(stars, 0);
        $('#id_rating').val(1);
    });
    $('#s2').click(function () {
        change_color(stars, 1);
        $('#id_rating').val(2);

    });
    $('#s3').click(function () {
        change_color(stars, 2);
        $('#id_rating').val(3);
    });
    $('#s4').click(function () {
        change_color(stars, 3);
        $('#id_rating').val(4);
    });
    $('#s5').click(function () {
        change_color(stars, 4);
        $('#id_rating').val(5);
    });
}

function change_color(stars, i) {
    console.log("i="+i);
    console.log('click');
    var j;
    for (j = 0; j <= i; j++) {
        stars[j].classList.remove('unrate');
        stars[j].classList.add('rate');
    }
    console.log("j="+j);
    for (j; j < stars.length; j++) {
        stars[j].classList.remove('rate');
        stars[j].classList.add('unrate');
    }
}








