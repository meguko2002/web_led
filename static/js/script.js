// ページ読込完了後にボタンにclickイベントを登録する
window.addEventListener("load", function(){
	document.getElementById("send_on").addEventListener("click", {state:"on", handleEvent:light_ctr},false);
	document.getElementById("send_off").addEventListener("click", {state:"off", handleEvent:light_ctr},false);
}, false);

function light_ctr(e){
    console.log(this.state)
    var XHR = new XMLHttpRequest();
    // openメソッドにPOSTを指定して送信先のURLを指定します
    XHR.open("POST", "/", true);
    // sendメソッドにデータを渡して送信を実行する
    XHR.send(this.state);
    // サーバの応答をonreadystatechangeイベントで検出して正常終了したらデータを取得する
    XHR.onreadystatechange = function(){
        if(XHR.readyState == 4 && XHR.status == 200){
            // POST送信した結果を表示する
            jsonObj = JSON.parse(XHR.responseText);
            document.getElementById("userinfo_response").innerHTML = jsonObj.led;
        }
    };
}




