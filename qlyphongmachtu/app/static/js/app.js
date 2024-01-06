function addBook(){
    let desc = document.getElementById('descId');
    let date = document.getElementById('dateId');
    let selectElement = document.getElementById('timeId');
    let timeId = selectElement.value;
    if (desc !== null) {
        fetch('/api/booking-form',{
        method:'post',
        body: JSON.stringify({ // Chuyển từ data sang SJON
               'date' : date.value,
               'desc' : desc.value,
               'time_id' : timeId
        }),
        headers: {
            'Content-Type':"application/json"
        }
        }).then(function(res){
            return res.json();

        }).then(function(data){
            if (data.status == 201){
                alert('Đặt lịch hành công')
            } else if (data.status == 404 ){
                alert('Đặt lịch thất bại')
            }
        })
    }
}