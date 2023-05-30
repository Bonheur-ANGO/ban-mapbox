export function displayTronconsFusionned(map, code_insee) {
    let apiUrl = "http://127.0.0.1:5000/commune/voie/" + code_insee
    fetch(apiUrl)
        .then((response) => {
            if (!response.ok) {
            throw new Error("Erreur lors de la récupération des données de l'API");
            }
            return response.json();
        })
        .then((features) => {
          console.log(features);
          map.addSource('fusion-troncon', {
            'type': 'geojson',
            'data': features
          });
        
            map.addLayer({
              'id': 'fusion-line',
              'type': 'line',
              'source': 'fusion-troncon',
              'paint': {
                'line-width': 5,
                'line-color': '#2ecc71'
            }
          });

          map.addLayer({
            'id': 'fusion-line-highlight',
            'type': 'line',
            'source': 'fusion-troncon',
            'paint': {
                'line-color': '#f00',
                'line-width': 5
            },
            'filter': ['==', 'identifiant_voie', '']
        });
  
        })
        .catch((error) => {
            console.error("Erreur lors de la récupération des données de l'API:", error);
        });
}