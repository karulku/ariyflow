/*
什么是异步编程？
    在js中，代码是按序依次执行的（从上到下）,但是有时我们需要进行耗时操作（比如从服务器获取数据），我们不希望它阻塞整体代码的进行，这时候就需要异步编程。
*/
console.log("准备开始");

setTimeout(function(){
    console.log("2秒后打印")
}, 2000);

console.log("准备结束");
// setTimeout 是异步操作，js不会为了它而停住，而是继续向下运行。

// 异步编写方式：Callback Promise async/await（推荐）

// Promise
function fakeAPI(){
    return new Promise((resolve)=>{
        setTimeout(()=>resolve("数据准备好"),1000);
    });
}
fakeAPI()
    .then(data=>{
        console.log(data);
    })
    .catch(err=>{
        console.error(err);
    });

async function fetchData(){
    const data = await fakeAPI();
    console.log(data);
}
fetchData();