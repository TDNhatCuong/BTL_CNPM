function addBook() {
    let desc = document.getElementById('descId');
    let date = document.getElementById('dateId');
    let selectElement = document.getElementById('timeId');
    let timeId = selectElement.value;
    if (desc !== null) {
        fetch('/api/booking-form', {
            method: 'post',
            body: JSON.stringify({
                'date': date.value,
                'desc': desc.value,
                'time_id': timeId
            }),
            headers: {
                'Content-Type': "application/json"
            }
        }).then(function (res) {
            return res.json();

        }).then(function (data) {
            if (data.status == 201) {
                alert('Đặt lịch hành công')
            } else if (data.status == 404) {
                alert('Đặt lịch thất bại')
            }
        })
    }
}


function lenlich(id) {
    checkPatientCount();
    fetch('/len-ds', {
        method: "post",
        body: JSON.stringify({
            "id": id,
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function (res) {
        return res.json();

    }).then(function (data) {
        window.location.reload();
        alert('Đã thêm thành công bệnh nhân!');
    })
}


function lenphieukham(id) {
    fetch('/len-pk', {
        method: "post",
        body: JSON.stringify({
            "id": id,
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function (res) {
        return res.json();

    }).then(function (data){
        window.location.href = "/phieukham" ;
    });
//    .then(function (data) {
//        window.location.reload();
//        alert('Đã lập phiếu khám thành công!');
//    })
}




function addPK() {
    let desc = document.getElementById('description').value;
    let dise = document.getElementById('disease').value;
    let medicineTables = document.querySelectorAll("#medicine-table");

    medicineTables.forEach(function(table) {
        let medcineName = table.querySelector(".medcine-name select").value;
        let medcineQuantity = table.querySelector(".medcine-quantity input").value;
        let medcineUsage = table.querySelector(".medcine-usage textarea").value;
    });

    fetch('api/phieukham', {
        method: 'post',
        body: JSON.stringify({
            'desc': desc.value,
            'dise': dise.value,
            'mediName': medcineName.value[0]
            'mediQuantity': medcineQuantity.value[0]
            'mediUsage': medcineUsage.value[0]
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function (res) {
            return res.json();

    }).then(function (data) {
            if (data.status == 201) {
                alert('Đặt lịch hành công')
            } else if (data.status == 404) {
                alert('Đặt lịch thất bại')
            }
        })
    }
}




function checkPatientCount() {
    fetch('/api/check-patient-count')
        .then(response => response.json())
        .then(data => {
            if (data.patients_today >= 40) {
                // alert('Đã đủ 40 bệnh nhân, không thể đăng ký thêm!');
                document.getElementById('message-container').innerText = 'Đã đủ 40 bệnh nhân, không thể đăng ký thêm!';
                var buttons = document.querySelectorAll('button.book-btn');
                buttons.forEach(button => {
                    button.disabled = true;
                });
                var messageContainer = document.getElementById('message-container');
                messageContainer.innerText = message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

window.onload = function () {
    checkPatientCount();
};



