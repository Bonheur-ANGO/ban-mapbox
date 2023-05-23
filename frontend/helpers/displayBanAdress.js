export function displayBanAdress(map, code_insee) {
    let apiUrl = "http://127.0.0.1:5000/commune/ban/" + code_insee
    fetch(apiUrl)
        .then((response) => {
            if (!response.ok) {
            throw new Error("Erreur lors de la récupération des données de l'API");
            }
            return response.json();
        })
        .then((features) => {
          map.addSource('ban', {
            'type': 'geojson',
            'data': features
          });
        
            map.addLayer({
              'id': 'ban-adresses',
              'type': 'circle',
              'source': 'ban',
              paint: {
                'circle-radius': 8,
                'circle-color': '#c0392b',
                'circle-opacity': 0.8,
            },
            'minzoom': 12
          });
  
        })
        .catch((error) => {
            console.error("Erreur lors de la récupération des données de l'API:", error);
        });
}