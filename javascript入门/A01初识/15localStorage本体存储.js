/*
localStorage属于浏览器提供的一种轻量级数据存储方式，可以让我们在页面刷新后仍然保存数据（最多5MB，按域进行保存，数据是纯文本）
主要API:
localStorage.setItem(key, value) 设置数据
localStorage.getItem(key) 获取数据
localStorage.removeItem(key) 移除数据
localStorage.clear() 清空数据
*/
// 这个代码跑不了，这个功能只在web里面有，node.js没有
localStorage.setItem("username","Alice");

const myname = localStorage.getItem("username");
console.log("username from localStorage: ",myname);

localStorage.removeItem("username");
localStorage.clear();