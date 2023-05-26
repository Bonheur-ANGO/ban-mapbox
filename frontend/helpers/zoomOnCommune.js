import mapboxgl  from 'mapbox-gl';
import { getTronconsByCommune } from './getTronconsByCommune';
import { displayBanAdress } from './displayBanAdress';

export function zoomOnCommune(map, code_insee) {
    if (map.getSource("commune")) {
        map.removeLayer("commune-layer")
        map.removeSource("commune")
        map.removeLayer("ban-adresses")
        map.removeSource("ban")

        if(map.getSource("fusion-troncon")){
          map.removeLayer("fusion-line")
          map.removeLayer("fusion-line-highlight")
          map.removeSource("fusion-troncon")
      }
    } 
    
    


    
    let apiUrl = `https://geo.api.gouv.fr/communes?code=${code_insee}&format=geojson&geometry=contour`
    fetch(apiUrl)
        .then((response) => {
            if (!response.ok) {
            throw new Error("Erreur lors de la récupération des données de l'API");
            }
            return response.json();
        })
        .then((feature) => {
          //getTronconsByCommune(map, code_insee)
          displayBanAdress(map, code_insee)
          map.addSource('commune', {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': [feature.features[0]]
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
          const coordinates = feature.features[0].geometry.coordinates
        
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
            zoom: 14
          })
  
        })
        .catch((error) => {
            console.error("Erreur lors de la récupération des données de l'API:", error);
        });
  
  
  }