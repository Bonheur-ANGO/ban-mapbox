import mapboxgl  from 'mapbox-gl';
import * as dotenv from 'dotenv';
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';
import { searchAddress } from './helpers/searchAdress';
import { displayResults } from './helpers/displayResults';
import { VectorTile } from '@mapbox/vector-tile';
import Pbf from 'pbf';



// Accès à l'API de tuiles vectorielles de Plan IGN
const accessToken = "pk.eyJ1IjoiYm9uaGV1ciIsImEiOiJjbGdxZmJnZTAwb3kxM2ZtbWFsOGV4NWpuIn0.iFcYtIyt8g-7QBQwd3AYYw";
//const style = 'https://maputnik.github.io/osm-liberty/style.json';


// Initialisation de la carte
mapboxgl.accessToken = accessToken;
const map = new mapboxgl.Map({
  container: 'map',
  style: "https://api.maptiler.com/maps/bright-v2/style.json?key=gJkxOc4aneJKVFzYyxzk",
  center: [2.349014, 48.864716],
  zoom: 9
});


map.on('load', () => {
  // Ajouter la source de tuiles vectorielles BAN après le chargement de la carte
  map.addSource('ban', {
      type: 'vector',
      tiles: ['https://plateforme.adresse.data.gouv.fr/tiles/ban/{z}/{x}/{y}.pbf'],
      minzoom: 0,
      maxzoom: 14,
  });

  map.addLayer({
    id: 'ban-adresses',
    type: 'circle',
    source: 'ban',
    'source-layer': 'adresses',
    paint: {
        'circle-radius': 8,
        'circle-color': '#FF0000',
        'circle-opacity': 0.8,
    }
});

map.addLayer({
  id: 'ban-point-label',
  type: 'symbol',
  source: 'ban',
  'source-layer': 'adresses',
  layout: {
      'text-field': '{numero}{suffixe}',
      'text-font': ['Open Sans Regular'],
      'text-size': 16,
      'text-offset': [0, 1.5],
  },
  paint: {
      'text-color': '#000',
  },
});


//bdtopo
map.addSource("bd-topo-routes", {
  type: "vector",
  url: "https://wxs.ign.fr/static/vectorTiles/styles/BDTOPO/routier.json"
});



});

//console.log(map.queryRenderedFeatures());

map.on('click', (e) => {
  const features = map.queryRenderedFeatures(e.point, {
    layers: ["ban-adresses"], // Remplacez ceci par le nom de la couche d'adresses de la BAN que vous avez ajoutée
  });

  // Vérifiez si une entité d'adresse a été trouvée
  if (features.length > 0) {
    // Prenez la première entité trouvée
    const addressFeature = features[0];
    console.log(addressFeature);

    // Créez une chaîne contenant les propriétés de l'adresse sous forme de texte HTML
    const addressInfo = Object.entries(addressFeature.properties)
      .map(([key, value]) => `<strong style="color: purple">${key}:</strong> ${value}`)
      .join("<br>");

    // Créez une nouvelle popup et définissez son contenu et sa position
    const popup = new mapboxgl.Popup()
      .setLngLat(e.lngLat)
      .setHTML(`<div style="font-size: 16px;">${addressInfo}</div>`)
      .addTo(map);
  } else {
    console.log("Aucune adresse trouvée");
  }

});

const searchInput = document.getElementById('search-input')
let marker = new mapboxgl.Marker()

searchInput.addEventListener("input", async (event) => {
  const query = event.target.value;
  if (query.length > 2) {
      const results = await searchAddress(query);
      displayResults(map, results, marker);
  }
});




/**/