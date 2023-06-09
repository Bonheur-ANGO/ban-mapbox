import mapboxgl  from 'mapbox-gl';
import { searchAddress } from './helpers/searchAdress';
import { displayResults } from './helpers/displayResults';
import { VectorTile } from '@mapbox/vector-tile';
import { getCommunes } from './helpers/getCommunes';
import { zoomOnCommune } from './helpers/zoomOnCommune';
import { verifyCodeInsee } from './helpers/verifyCodeInsee';
import { displayTronconsFusionned } from './helpers/displayTronconsFusionned';
import { mergedAdress } from './helpers/mergedAddress';
import { getLinkToSupportObject } from './helpers/getLinkToSupportObject';
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
let marker = new mapboxgl.Marker()


const searchInput = document.getElementById("search-input")
map.on('load', () => {
  searchInput.addEventListener('input', ()=>{
    searchAddress(searchInput.value, map, marker)
  })
  // Ajouter la source de tuiles vectorielles BAN après le chargement de la carte
  /*map.addSource('ban', {
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
  });*/

  



  //bdtopo
  fetch('https://wxs.ign.fr/static/vectorTiles/styles/BDTOPO/routier.json')
    .then(response => response.json())
    .then(styleData => {
      //console.log(styleData);
      map.addSource("bdtopo", {
        type: "vector",
        tiles: styleData.sources.bdtopo.tiles,
      });

      styleData.layers.forEach(layer => {
        const newLayer = {...layer}
        map.addLayer(newLayer)
      });



    });



});


map.on('click', (e) => {
  const allLayers = map.getStyle().layers;
  const bdTopoLayers = allLayers
    .filter((layer) => layer.source === 'bdtopo')
    .map((layer) => layer.id);

    const tronconsLayers = allLayers
    .filter((layer) => layer.source === 'troncons')
    .map((layer) => layer.id);

  const banLayers = allLayers
    .filter((layer) => layer.source === 'ban')
    .map((layer) => layer.id);

    const ft = allLayers
    .filter((layer) => layer.source === 'fusion-troncon')
    .map((layer) => layer.id);

    const jta = allLayers
    .filter((layer) => layer.source === 'jointure-adresse')
    .map((layer) => layer.id);



  const allFeatures = map.queryRenderedFeatures(e.point, {
    layers: [...banLayers, ...bdTopoLayers, ...tronconsLayers, ...ft, ...jta], 
  });

  //display metadata
  if (allFeatures.length > 0) {
    // get the first feature
    const addressFeature = allFeatures[0];

    const addressInfo = Object.entries(addressFeature.properties)
      .map(([key, value]) => `<strong style="color: purple">${key}:</strong> ${value}`)
      .join("<br>");

    //display popup
    const popup = new mapboxgl.Popup()
      .setLngLat(e.lngLat)
      .setHTML(`<div style="font-size: 16px;">${addressInfo}</div>`)
      .setMaxWidth('800')
      .addTo(map);

    ;
  } else {
    console.log("Aucun objet trouvée");
  }




});


//Récupère toutes les communes
getCommunes()


//zoom et applique un style sur la commune
const zoomBtn = document.getElementById("zoomBtn")
const communeInput = document.getElementById("inputForCommune")

zoomBtn.addEventListener("click", ()=>{
  const code_insee = communeInput.value
  verifyCodeInsee(map, communeInput.value, zoomOnCommune(map, code_insee))
})

//appariement géométrique
const geometricMatchingBtn = document.getElementById('geomatching')
geometricMatchingBtn.addEventListener('click', ()=>{
  const code_insee = communeInput.value
  verifyCodeInsee(map, code_insee, getLinkToSupportObject(map, code_insee) ,displayTronconsFusionned(map, code_insee), /*mergedAdress(map, code_insee)*/)
  /*let apiUrl = "http://127.0.0.1:5000/commune/appariement_geometrique/" + code_insee
    fetch(apiUrl)
        .then((response) => {
            if (!response.ok) {
            throw new Error("Erreur lors de la récupération des données de l'API");
            }
            return response.json();
        })
        .then((features) => {
          console.log(features);
          map.addSource('alert', {
            'type': 'geojson',
            'data': features
          });
        
            map.addLayer({
              'id': 'alert-line',
              'type': 'line',
              'source': 'alert',
              'paint': {
                'line-width': 5,
                'line-color': '#f1c40f'
            }
          });
  
        })
        .catch((error) => {
            console.error("Erreur lors de la récupération des données de l'API:", error);
        });*/
  
})



map.on('click', 'fusion-line', function (e) {
  if (e.features.length > 0) {
      var clickedId = e.features[0].properties['identifiant_voie'];

      // Met à jour le filtre pour inclure l'identifiant de la ligne sur laquelle vous avez cliqué
      map.setFilter('fusion-line-highlight', ['==', 'identifiant_voie', clickedId]);
  }
});

