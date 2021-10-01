// ページ読込完了後にボタンにclickイベントを登録する
window.addEventListener("load", function(){
	document.getElementById("send_on").addEventListener("click", function(){
		var postDatas = 'on'
		var XHR = new XMLHttpRequest();
		// openメソッドにPOSTを指定して送信先のURLを指定します
		XHR.open("POST", "/", true);
		// sendメソッドにデータを渡して送信を実行する
		XHR.send(postDatas);
		// サーバの応答をonreadystatechangeイベントで検出して正常終了したらデータを取得する
		XHR.onreadystatechange = function(){
			if(XHR.readyState == 4 && XHR.status == 200){
				// POST送信した結果を表示する
				document.getElementById("userinfo_response").innerHTML = XHR.responseText;
			}
		};
	} ,false);
	document.getElementById("send_off").addEventListener("click", function(){
		var XHR = new XMLHttpRequest();
		XHR.open("POST", "/", true);
		XHR.send('off');
		XHR.onreadystatechange = function(){
			if(XHR.readyState == 4 && XHR.status == 200){
				// POST送信した結果を表示する
				document.getElementById("userinfo_response").innerHTML = XHR.responseText;
			}
		};
	} ,false);

}, false);




