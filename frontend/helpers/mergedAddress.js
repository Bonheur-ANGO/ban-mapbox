export function mergedAdress(map, code_insee) {
    let apiUrl = "http://127.0.0.1:5000/commune/ban/jointure/" + code_insee
  fetch(apiUrl)
      .then((response) => {
          if (!response.ok) {
          throw new Error("Erreur lors de la récupération des données de l'API");
          }
          return response.json();
      })
      .then((features) => {
        console.log(features);
        map.addSource('jointure-adresse', {
          'type': 'geojson',
          'data': features
        });
      
          map.addLayer({
            'id': 'jointure-adresse-line',
            'type': 'line',
            'source': 'jointure-adresse',
            'paint': {
              'line-width': 5,
              'line-color': '#8e44ad'
          }
        });

      })
      .catch((error) => {
          console.error("Erreur lors de la récupération des données de l'API:", error);
      });
}