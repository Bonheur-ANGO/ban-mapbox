export async function searchAddress(query) {
    const response = await fetch(
        `https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query)}&limit=5`
    );
    const data = await response.json();
    return data.features;
  }