var gototop = document.getElementById("Gototop");

 window.onscroll= function(){
    console.info(document.documentElement.scrollTop);
     if(document.documentElement.scrollTop > 100){
         gototop.style.display = "block";
     }
     else{
        gototop.style.display = "none";
     }
 }
 function goToTop(){
    var x= setInterval(function(){
        document.documentElement.scrollTop-=20;
        if(document.documentElement.scrollTop<=0)
        clearInterval(x);
    },1)
 }