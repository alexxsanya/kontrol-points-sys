var lng = 0;
var lat = 0;
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(getPosition);

} else {
  alert("Geolocation is not supported by this browser.");
}

function getPosition(position) {
  lat = position.coords.latitude;
  lng = position.coords.longitude; 
}

function loadControlMap(){ 
    if(lat==0 & lng==0){
        lat= 0.3499986
        lng = 32.56716
    } 
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(getPosition);
      
      } else {
        alert("Geolocation is not supported by this browser.");
      }
      
      function getPosition(position) {
        lat = position.coords.latitude;
        lng = position.coords.longitude; 
    }
    var style = [
        {
          "featureType": "administrative",
          "elementType": "geometry",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "administrative.land_parcel",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "administrative.neighborhood",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "poi",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "poi",
          "elementType": "labels.text",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "road",
          "elementType": "labels",
          "stylers": [
            {
              "visibility": "on"
            }
          ]
        },
        {
          "featureType": "road",
          "elementType": "labels.icon",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "transit",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "water",
          "elementType": "labels.text",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        }
      ]
     
    var myCurrentPosition = new google.maps.LatLng(lat, lng);
    map = new google.maps.Map(document.getElementById('mapCanvas'), {
      center: myCurrentPosition,
      zoom: 14,
      mapTypeId:'roadmap',
      styles:style,
    });
  
    var marker = new google.maps.Marker({
      position: myCurrentPosition, 
      map: map,
      icon:'/static/assets/user.png'
    });
  
     $.getJSON('/all-points', function(json1) {
        $.each(json1, function(key, data) {
            
            k_geocord = data.k_geocord.split(',')
            console.log(k_geocord)
            var latLng = new google.maps.LatLng(parseFloat(k_geocord[0]), parseFloat(k_geocord[1])); 
            // Creating a marker and putting it on the map
            var marker = new google.maps.Marker({
                position: latLng,
                map: map,
                title: data.k_name,	
                icon:'/static/assets/pin.png'
            });
  
          var clicker = addClicker(marker, data);
        });
    });
  
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
                        "&nbsp<button onclick='add_review()' data='"+
                            content.id+"' user_id='"+
                            content.user_id+"'>Add a Review</button>"+
                      "</div>"+
                   "</div>"; 
        infowindow.setContent(info); 
  
        infowindow.open(map, marker);

      });
    }

}

function calculateRoute(to) {
    if(lat==0 & lng==0){
        lat= 0.3499986
        lng = 32.56716
    } 
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(getPosition);
      
    } else {
        alert("Geolocation is not supported by this browser.");
      }
      
    function getPosition(position) {
        lat = position.coords.latitude;
        lng = position.coords.longitude; 
    }
    var myCurrentPosition = new google.maps.LatLng(lat, lng);    
    var myOptions = {
      zoom: 13,
      center: myCurrentPosition,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }; 
    var mapObject = new google.maps.Map(document.getElementById("mapCanvas"), myOptions);

    var directionsService = new google.maps.DirectionsService();
    var directionsRequest = {
      origin: myCurrentPosition,
      destination: to,
      travelMode: google.maps.DirectionsTravelMode.DRIVING,
      unitSystem: google.maps.UnitSystem.METRIC
    };
    directionsService.route(
      directionsRequest,
      function(response, status)
      {
        if (status == google.maps.DirectionsStatus.OK)
        {
          new google.maps.DirectionsRenderer({
            map: mapObject,
            directions: response
          });
        }
        else
          $("#error").append("Unable to retrieve your route<br />");
      }
    );
}

function get_direction(e){
    e = e || window.event;
    var target = e.target || e.srcElement;
    var geocord =  target.getAttribute('data')
    geocord = geocord.split(',') 
    var latLng = new google.maps.LatLng(parseFloat(k_geocord[0]),parseFloat(k_geocord[1]));   
    calculateRoute(latLng)

}

function add_review(e){
  e = e || window.event;
  var target = e.target || e.srcElement;
  var kontrol_id =  target.getAttribute('data')  
  var user_id = target.getAttribute('user_id') 

  localStorage.setItem('kontrol_id',kontrol_id);
  localStorage.setItem('user_id',user_id);

  $('#reviewModal').modal('show')
}