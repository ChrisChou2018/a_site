//nav �����˵� ��ʼ-----------------------------------------------------------------
$(document).ready(function(e) {
	
  $('.nav_list li').mouseenter(function(){
		$(this).find('.nav_tt').slideDown(300);
		});
		
	$('.nav_list li').mouseleave(function(){
		$(this).find('.nav_tt').slideUp(300);
		});
	
	$(".cont1_tit").click(function(){
			$(this).next(".cont1_ul").slideToggle(500).siblings(".cont1_ul").slideUp(500);
	})
	
	$('.ewm_weixin').mouseenter(function(){
	  $('.top_weixin').show(300);
	  });
	$('.ewm_weixin').mouseleave(function(){
		$('.top_weixin').hide(300);
		});
	//$('.ewm_qq').mouseenter(function(){
//	  $('.top_qq').show(300);
//	  });
//	$('.ewm_qq').mouseleave(function(){
//		$('.top_qq').hide(300);
//		});
//	$('.ewm_weibo').mouseenter(function(){
//	  $('.top_weibo').show(300);
//	  });
//	$('.ewm_weibo').mouseleave(function(){
//		$('.top_weibo').hide(300);
//		});
		
	$('.close').click(function(){
		$('.b_cpf').hide(300);
		$('.b_zz').hide(300);
		});
	$('.close1').click(function(){
		$('.b_cpf').hide(300);
		$('.b_zz').hide(300);
		});
		
	$('.lpf_close').click(function(){
		$('.b_lpf').hide(300);
		$('.b_pp').show(300);
		});
	$('.b_pp').mouseenter(function(){
		$('.b_lpf').show(300);
		$('.b_pp').hide(300);
		});
		
	//$(window).scroll(function(){
    //if($(window).scrollTop()>500){
       // $(".y_left").css({
					 // "position":"fixed",
					//	"width":"260px",
					//	"top":"0px"
     //  });
  //  }else{
//			$(".y_left").css({
	//				  "position":"static",
	//					"width":"21.7%",
     //  });
	//		}
	//	});
		
	$(".subNav").click(function(){
			$(this).toggleClass("currentDd").siblings(".subNav").removeClass("currentDd")
			$(this).toggleClass("currentDt").siblings(".subNav").removeClass("currentDt")
			
			// 修改数字控制速度， slideUp(500)控制卷起速度
			$(this).next(".left_ul1").slideToggle(500).siblings(".left_ul1").slideUp(500);
	})	

});

	
//������ ��ʼ-----------------------------------------------------------------
function tabChange(obj,id,p_tab,p_style)
{
 var arrayli = obj.parentNode.getElementsByTagName("li"); //��ȡli����
 var arrayul = document.getElementById(id).getElementsByTagName(p_tab); //��ȡul����
 for(i=0;i<arrayul.length;i++)
 {
  if(obj==arrayli[i])
  {
   arrayli[i].className = p_style;
   arrayul[i].style.display = "";
  }
  else
  {
   arrayli[i].className = "";
   arrayul[i].style.display = "none";
  }
 }
}



//������ ��ʼ-----------------------------------------------------------------
var rDrag = {
 o:null,
//欢迎来到站长特效网，我们的网址是www.zzjs.net，很好记，zz站长，js就是js特效，本站收集大量高质量js代码，还有许多广告代码下载。
 init:function(o){
  o.onmousedown = this.start;
 },
 start:function(e){
  var o;
  e = rDrag.fixEvent(e);
               e.preventDefault && e.preventDefault();
               rDrag.o = o = this;
  o.x = e.clientX - rDrag.o.offsetLeft;
                o.y = e.clientY - rDrag.o.offsetTop;
  document.onmousemove = rDrag.move;
  document.onmouseup = rDrag.end;
 },
 move:function(e){
  e = rDrag.fixEvent(e);
  var oLeft,oTop;
  oLeft = e.clientX - rDrag.o.x;
  oTop = e.clientY - rDrag.o.y;
  rDrag.o.style.left = oLeft + 'px';
  rDrag.o.style.top = oTop + 'px';
 },
 end:function(e){
  e = rDrag.fixEvent(e);
  rDrag.o = document.onmousemove = document.onmouseup = null;
 },
    fixEvent: function(e){
        if (!e) {
            e = window.event;
            e.target = e.srcElement;
            e.layerX = e.offsetX;
            e.layerY = e.offsetY;
        }
        return e;
    }
}
window.onload = function(){
        var obj = document.getElementById('b_lpf');
 rDrag.init(obj);
}