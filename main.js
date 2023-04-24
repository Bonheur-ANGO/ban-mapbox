import mapboxgl  from 'mapbox-gl';
import * as dotenv from 'dotenv';
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';



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
    },
});

map.addLayer({
  id: 'ban-point-label',
  type: 'symbol',
  source: 'ban',
  'source-layer': 'adresses',
  layout: {
      'text-field': '{numero}{suffixe}',
      'text-font': ['Open Sans Regular'],
      'text-size': 12,
      'text-offset': [0, 1.5],
  },
  paint: {
      'text-color': '#000',
  },
});


});

//console.log(map.queryRenderedFeatures());

/*map.on('click', (e) => {
  const features = map.queryRenderedFeatures(e.point);
  
  if (features.length > 0) {
    const feature = features[0];
    
    console.log('Adresse:', feature);
}
});*/

const searchInput = document.getElementById('search-input')
const ul = document.getElementById('proposition-container');
const resultsContainer = document.getElementById("results-container");

async function searchAddress(query) {
  const response = await fetch(
      `https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query)}&limit=5`
  );
  const data = await response.json();
  return data.features;
}


function displayResults(results) {
  resultsContainer.style.display = "block"
  ul.innerHTML = ""

  const list = document.getElementById("proposition-container");
  results.forEach((result) => {
      const listItem = document.createElement("li");
      let address = document.createElement('span');
      let infosAdresse = document.createTextNode(result.properties.postcode + ' ' + result.properties.city);
      listItem.textContent = result.properties.name;
      listItem.appendChild(address);
      listItem.appendChild(infosAdresse);
      ul.appendChild(listItem);

      listItem.addEventListener("click", () => {
          const coordinates = result.geometry.coordinates;
          map.flyTo({ center: coordinates, zoom: 20 });
          resultsContainer.innerHTML = "";
      });
  });

  resultsContainer.appendChild(list);
}


searchInput.addEventListener("input", async (event) => {
  const query = event.target.value;
  if (query.length > 2) {
      const results = await searchAddress(query);
      console.log(results);
      displayResults(results);
  } else {
      document.getElementById("results-container").innerHTML = "";
  }
});