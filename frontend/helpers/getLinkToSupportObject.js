export function getLinkToSupportObject(map, code_insee){
    fetch('http://127.0.0.1:5000/commune/objets_supports/'+ code_insee)
  .then(response => response.json())
  .then(data => {
    console.log(data);
    map.addSource("objets-support", {
      type: "geojson",
      data: data,
    });

    map.addLayer({
      id: 'objets-support-line-layer',
      type: "line",
      source: 'objets-support',
      'paint': {
        'line-width': 5,
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