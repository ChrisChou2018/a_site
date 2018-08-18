var scrollnews = document.getElementById('wenchuan');
var lis = scrollnews.getElementsByTagName('p');
var ml = 0;
var timer1 = setInterval(function(){
		var liHeight = lis[0].offsetHeight;
		var timer2 = setInterval(function(){
		 scrollnews.scrollTop = (++ml);
		 if(ml == liHeight){
				clearInterval(timer2);
				scrollnews.scrollTop = 0;
				ml = 0;
				lis[0].parentNode.appendChild(lis[0]);
		 }
	},10);
},3000);