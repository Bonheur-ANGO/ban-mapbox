
export function verifyCodeInsee(map, code_insee, ...callbackFunction) {
    let apiUrl = "http://127.0.0.1:5000/liste_communes"
    fetch(apiUrl)
    .then((response) => {
        if (!response.ok) {
        throw new Error("Erreur lors de la récupération des données de l'API");
        }
        return response.json();
    })
    .then((data) => {
      let codeInseeTab = []
        data.forEach(commune => {
            codeInseeTab.push(commune['code_insee'])
        });
      if (!codeInseeTab.includes(code_insee)) {
        alert("Veuillez entrer un code INSEE valide")
      } else{
        callbackFunction
      }
    })
    .catch((error) => {
        console.error("Erreur lors de la récupération des données de l'API:", error);
    });
  }