function initMap() {
  var uluru = {lat: -25.363, lng: 131.044};
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: {lat: 42, lng: -71}
  });
  var marker = new google.maps.Marker({
    position: uluru,
    map: map
  });
  var marker2 = new google.maps.Marker({
    position: {lat: 42, lng: -71},
    map: map
  });
}

function addMarker(lat,lng) {
  
}
