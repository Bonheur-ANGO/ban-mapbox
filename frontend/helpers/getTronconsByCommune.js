export function getTronconsByCommune(map, code_insee){
    fetch('http://127.0.0.1:5000/commune/troncons/'+ code_insee)
  .then(response => response.json())
  .then(data => {
    //console.log(data['features']);
    map.addSource("troncons", {
      type: "geojson",
      data: data,
    });

    map.addLayer({
      id: 'troncons-line-layer',
      type: "line",
      source: 'troncons',
      'paint': {
        'line-width': 2,
        'line-color': [
            'match',
            ['get', 'nature'],
            'Sentier', '#69ff69', // rouge pour les sentiers
            'Piste cyclable', '#00ff00', // bleu pour les pistes cyclables
            'Type autoroutier', '#5068d2',
            'Route à 2 chaussées', '#ea2543',
            'Route à 1 chaussée', '#646464',
            'Chemin', '#c76227',
            'Bretelle', '#16dbc1',
            'Rond-point', '#a0a0a0',
            'Route empierrée', '#646464',
            'Escalier', 'rgba(255, 255, 255, 1)',
            '#000000' // noir par défaut pour tout autre type
        ]
    }
    })
    



  });
}