function addBook(){
    let desc = document.getElementById('descId');
    let date = document.getElementById('dateId');
    timeId = document.getElementById('timeId');
    let selectedTime = timeId.options[timeSelect.selectedIndex];
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
                alert('Thành công')
            } else if (data.status == 404 ){
                alert('Không thành  công')
            }
        })
    }
}