function statusHandler(){
    if($('.flash-status').css("display") != "none"){
        setTimeout(function() {  
            $('.flash-status').css("display",'none')
        }, 10000);
    }
}

function App() {
    statusHandler()
}