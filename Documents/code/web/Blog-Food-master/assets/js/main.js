let timer=null;
var counter=1;
function startInterval(){
  timer=setInterval(function(){
      document.getElementById('radio' + counter).checked=true;
      counter++;
      if(counter > 4)
      {
          counter=1;
      }
  },3000);
}
startInterval(timer);
function onClick(radio){
    var id=radio.id;
    var number= parseInt(id.replace("radio",""));
    clearInterval(timer);
    counter=number;
    startInterval(timer);
}
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
  //Tìm kiếm
 function search(){
    var k= document.getElementById("searchinput");
    var output1 = document.getElementById("output-history1");
    var output2 = document.getElementById("output-history2");
    var tmp;
    var History = document.getElementsByClassName("historyitem");
    for(var i=0; i<History.length;i++) //hide history
    {
        History[i].style.height = "0";
        History[i].style.padding = "0 0";
    }
    if(k.value !== "")
    {
        k = k.value;
        //lịch sử tìm kiếm
        History[0].style.height = "38px";       //open history 1
        History[0].style.padding = "10px 12px"; //open history 1
        tmp=output1.innerText;
        output1.innerText=k;
        if(tmp!==output1.innerText)
        {
            output2.innerText=tmp;
            if(output2.innerText!=="") //open history 2
            {
                History[1].style.height = "38px";
                History[1].style.padding = "10px 12px";
            }
        }
        //end lịch sử tìm kiếm
        var items = document.querySelectorAll("#item-search")
        for(var i=0;i<items.length;i++)
        {
            var item=items[i].innerText;

            if(item.toLowerCase().indexOf(k.toLowerCase())>=0)
            {
                items[i].style.borderBottom = "3px solid red";
            }
        }
         setTimeout(function(){
            for(var i=0;i<items.length;i++)
            {
             items[i].style.borderBottom = "none";
            }
         },4000)
    }
 }
//dark mode 
var toggle = document.getElementById("toggle");

toggle.onclick = function() {
    document.body.classList.toggle("dark-theme");
}
