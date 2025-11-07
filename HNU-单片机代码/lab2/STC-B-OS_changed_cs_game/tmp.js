const data = {
    key1: 'value1',
    key2: 'value2'
};

// 发送 POST 请求
resp = fetch('http://ariyflow.asia:5000/test', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(function(response){
    return response.json()
})
.then(function(data){
    console.log(data);
});