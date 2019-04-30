var lng = 0;
var lat = 0;
var K_Points = []
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
        console.log(lat)
        navigator.geolocation.watchPosition(getPosition);
        console.log(lat)
    } 
    
    navigator.geolocation.watchPosition(getPosition);
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

    var card = document.getElementById('pac-card');
    var input = document.getElementById('pac-input');

    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(card);

    var autocomplete = new google.maps.places.Autocomplete(input);

    autocomplete.bindTo('bounds', map);

    autocomplete.setFields(
        ['address_components', 'geometry', 'icon', 'name']);

    var infowindow = new google.maps.InfoWindow();
    var infowindowContent = document.getElementById('infowindow-content');
    infowindow.setContent(infowindowContent);
    var marker = new google.maps.Marker({
      map: map,
      anchorPoint: new google.maps.Point(0, -29)
    });

    autocomplete.addListener('place_changed', function() {
      infowindow.close();
      marker.setVisible(false);
      var place = autocomplete.getPlace();
      if (!place.geometry) {
        window.alert("No details available for input: '" + place.name + "'");
        return;
      }
      if (place.geometry.viewport) {
        map.fitBounds(place.geometry.viewport);
      } else {
        map.setCenter(place.geometry.location);
        map.setZoom(16);  // Why 17? Because it looks good.
      }
      marker.setPosition(place.geometry.location);
      marker.setVisible(true);
      /*
      var address = '';
      if (place.address_components) {
        address = [
          (place.address_components[0] && place.address_components[0].short_name || ''),
          (place.address_components[1] && place.address_components[1].short_name || ''),
          (place.address_components[2] && place.address_components[2].short_name || '')
        ].join(' ');
      }

      infowindowContent.children['place-icon'].src = place.icon;
      infowindowContent.children['place-name'].textContent = place.name;
      infowindowContent.children['place-address'].textContent = address;
      infowindow.open(map, marker);*/
    });

    var marker = new google.maps.Marker({
      position: myCurrentPosition, 
      map: map,
      icon:'/static/assets/user.png'
    });
 
      // Add circle overlay and bind to marker
    var circle = new google.maps.Circle({
        map: map,
        radius: 2*1609.34,    // 2 miles in metres
        strokeColor: '#FF0000',
        strokeOpacity: 0.4,
        strokeWeight: 2,
        fillColor: '#AA0000',
        fillOpacity: 0.15,
    });
    circle.bindTo('center', marker, 'position');  
    

     $.getJSON('/all-points', function(json1) {
        $.each(json1, function(key, data) {
            K_Points = json1
            console.log(K_Points)
            k_geocord = data.k_geocord.split(',')
            console.log(k_geocord)
            var latLng = new google.maps.LatLng(parseFloat(k_geocord[0]), parseFloat(k_geocord[1])); 
            // Creating a marker and putting it on the map
            var marker = new google.maps.Marker({
                position: latLng,
                map: map,
                title: data.k_name,	
                icon:`/static/assets/${data.k_status}.png`
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
                      "<p><a href='/points/"+content.k_name+"' <b>Point Name</b>  : "+content.k_name+"</a></p>"+ 
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
        console.log(lat)
        navigator.geolocation.watchPosition(getPosition);
        console.log(lat)
    }  
    
    navigator.geolocation.watchPosition(getPosition);
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
    var latLng = new google.maps.LatLng(parseFloat(geocord[0]),parseFloat(geocord[1]));   
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