import { displayResults } from "./displayResults";

export async function searchAddress(query, map, marker) {
    const response = await fetch(
        `https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query)}&limit=5`,
        {
            method: 'GET'
        }
    );
    const data = await response.json();
    
    if (data.features.length != 0) {
        displayResults(map, data.features, marker)
    } else{
        const ul = document.getElementById('proposition-container');
        ul.innerHTML = ""
        const resultsContainer = document.getElementById("results-container");
        resultsContainer.classList.add("d-none")
    }
    
  }