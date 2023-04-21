import mapboxgl  from 'mapbox-gl';
import * as dotenv from 'dotenv';



// Accès à l'API de tuiles vectorielles de Plan IGN
const accessToken = "pk.eyJ1IjoiYm9uaGV1ciIsImEiOiJjbGdxZmJnZTAwb3kxM2ZtbWFsOGV4NWpuIn0.iFcYtIyt8g-7QBQwd3AYYw";
const style = 'https://wxs.ign.fr/static/vectorTiles/styles/PLAN.IGN/essentiels/standard.json';


// Initialisation de la carte
mapboxgl.accessToken = accessToken;
const map = new mapboxgl.Map({
  container: 'map',
  center: [2.349014, 48.864716],
  zoom: 9
});

map.addSource('Plan ign', {
  type: 'vector',
  url: "https://wxs.ign.fr/essentiels/geoportail/tms/1.0.0/PLAN.IGN/{z}/{x}/{y}.pbf",
})

map.setStyle(style)