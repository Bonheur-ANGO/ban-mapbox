import mapboxgl from "mapbox-gl";


export function displayResults(map, results, marker) {
    const searchInput = document.getElementById('search-input')
    const ul = document.getElementById('proposition-container');
    const resultsContainer = document.getElementById("results-container");

    resultsContainer.classList.remove("d-none")
    ul.innerHTML = ""
  
    results.forEach((result) => {
        const listItem = document.createElement("li");
        const address = result.properties.label;
        listItem.textContent = address
        ul.appendChild(listItem);
  
        listItem.addEventListener("click", () => {
          //console.log(result);
          searchInput.value= address
          resultsContainer.classList.add("d-none")
            const coordinates = result.geometry.coordinates;
            //removeMarker before adding
            if (map.getSource("geocodage-adresse")) {
              map.removeLayer("geocodage-adresse-point")
              map.removeSource("geocodage-adresse")
            }
            if (marker) {
                marker.remove();
            }
            map.flyTo({ center: coordinates, zoom: 18 });

            //add marker
            marker.setLngLat(coordinates).addTo(map);
            console.log(result);
            map.addSource("geocodage-adresse", {
              type: "geojson",
              data: result
            })

            map.addLayer({
              id: 'geocodage-adresse-point',
              type: 'circle',
              source: 'geocodage-adresse',
              paint: {
                  'circle-radius': 10,
                  'circle-color': '#007cbf'
              }
          });

        });
    });
  
  }
