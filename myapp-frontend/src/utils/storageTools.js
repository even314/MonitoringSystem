import {ref} from 'vue'

//格式：storage('key')={'time':'inf'}

const key='history'


export const historyList=ref(initHistory())


export const writeHistory=(inf)=>{
    // console.log(historyList)
    var time=currentTime()
    historyList.value[time]=inf
    localStorage.setItem(key,JSON.stringify(historyList.value))
}

//删除
export const delHistory=()=>{
    localStorage.removeItem(key)
    localStorage.setItem(key,JSON.stringify({}))
    historyList.value={}
}

function initHistory(){
    let historyStore=localStorage.getItem(key)
    // console.log(historyStore)
    if(historyStore==null){
       localStorage.setItem(key,JSON.stringify({}))
       return {}
    }
    //出现错误直接清空
    try {
        var data= JSON.parse(historyStore)
    } catch (error) {
        localStorage.removeItem(key)
        localStorage.setItem(key,JSON.stringify({}))
        data={}
    }
    return data
}
/**
* 获取当前时间
*/
function currentTime() {
    var date = new Date();
    var year = date.getFullYear(); //月份从0~11，所以加一
    // let month = date.getMonth();
    // console.log("month",month);
    var dateArr = [
        date.getMonth() + 1,
        date.getDate(),
        // date.getHours(),
        // date.getMinutes(),
        // date.getSeconds(),
    ];
    //如果格式是MM则需要此步骤，如果是M格式则此循环注释掉
    for (var i = 0; i < dateArr.length; i++) {
        if (dateArr[i] >= 1 && dateArr[i] <= 9) {
            dateArr[i] = "0" + dateArr[i];
        }
    }
    return( year +
        "-" +
        dateArr[0] +
        "-" +
        dateArr[1] )
        // " " +
        // dateArr[2] +
        // ":" +
        // dateArr[3] +
        // ":" +
        // dateArr[4])
}
