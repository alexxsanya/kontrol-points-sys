function statusHandler(){
    if($('.flash-status').css("display") != "none"){
        setTimeout(function() {  
            $('.flash-status').css("display",'none')
        }, 10000);
    }
}

function searchPoint(){

    var k_name = $('#s-k-name').val()

    if(k_name.length < 8){
        alert("Invalid Control Point Name");
    }else{

        $.getJSON('point/'+k_name, function(data) {     
            
            if(!$.isEmptyObject(data)) {
                        
                var k_geocord = data.k_geocord.split(',') 

                var latLng = new google.maps.LatLng(k_geocord[0], k_geocord[1]); 
                
                map = new google.maps.Map(document.getElementById('mapCanvas'), {
                    center: latLng,
                    zoom: 18,
                    mapTypeId:'roadmap',
                });  
                
                // Creating a marker and putting it on the map
                var marker = new google.maps.Marker({
                    position: latLng,
                    map: map,
                    title: data.k_name,	
                    icon:`/static/assets/${data.k_status}.png`
                });
                var clicker = addClicker(marker, data);
            }else{
                alert("No Control Point in the system with provided Name")
            }
        });
        $('#searchModal').modal('hide');
    }

    function addClicker(marker, content) {
        var infowindow = new google.maps.InfoWindow();
        google.maps.event.addListener(marker, 'click', function() {
        if (infowindow) {infowindow.close();}
        k_geocord = content.k_geocord.split(',') 
        var latLng = new google.maps.LatLng(parseFloat(k_geocord[0]),parseFloat(k_geocord[1]));
        destination = new google.maps.LatLng(latLng); 
        var info = "<div style = 'width:250px;min-height:40px'>"+
                      "<p> <b>Point Name</b>  : "+content.k_name+"</p>"+ 
                      "<p> <b>Description</b> : <br>"+content.k_description+"</p>"+
                      "<p> <b>Address  </b>   : "+content.k_addr_subcounty+", "+
                        content.k_addr_county+", "+content.k_addr_district+
                      "</p>"+
                      "<hr />"+
                      "<div style='margin:5px 5px'>"+
                        "<button onclick='get_direction()' data='"+
                            content.k_geocord+"'>Get Direction</button>"+
                      "</div>"+
                   "</div>"; 
        infowindow.setContent(info); 
  
        infowindow.open(map, marker);

      });
    }
}

radiusToZoom = function (radius){
    return Math.round(14-Math.log(radius)/Math.LN2);
}

function App() {
    statusHandler()
}