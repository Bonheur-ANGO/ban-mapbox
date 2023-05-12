import mapboxgl  from 'mapbox-gl';

export function zoomOnCommune(map, code_insee) {
    if (map.getSource("commune")) {
        map.removeLayer("commune-layer")
        map.removeSource("commune")
    }
    
    let apiUrl = "http://127.0.0.1:5000/commune/" + code_insee
    fetch(apiUrl)
        .then((response) => {
            if (!response.ok) {
            throw new Error("Erreur lors de la récupération des données de l'API");
            }
            return response.json();
        })
        .then((feature) => {
          map.addSource('commune', {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': [feature]
            }
          });
        
            map.addLayer({
              'id': 'commune-layer',
              'type': 'fill',
              'source': 'commune',
              'paint': {
                'fill-color': '#088',
                'fill-opacity': 0.3
              }
          });
          const coordinates = feature.geometry.coordinates
        
          let bounds = new mapboxgl.LngLatBounds();
          coordinates[0].forEach(coord =>{
            let lng = coord[0];
            let lat = coord[1];
        
            // Check if coordinates are valid
            if (lng < -180 || lng > 180 || lat < -90 || lat > 90) {
                console.error('Invalid coordinates: ', coord);
            } else {
                bounds.extend(coord);
            }
          })
        
          map.fitBounds(bounds, {
            zoom: 13
          })
  
        })
        .catch((error) => {
            console.error("Erreur lors de la récupération des données de l'API:", error);
        });
  
  
  }