 // récupère toutes les communes
 export function getCommunes() {
    let apiUrl = "http://127.0.0.1:5000/liste_communes"
    const select = document.querySelector("#communes")
    fetch(apiUrl)
    .then((response) => {
        if (!response.ok) {
        throw new Error("Erreur lors de la récupération des données de l'API");
        }
        return response.json();
    })
    .then((data) => {
        data.forEach(commune => {
            let option = document.createElement("option")
            option.setAttribute("value", commune["code_insee"])
            option.textContent = commune["nom_commune"]
            select.append(option)

        });
    })
    .catch((error) => {
        console.error("Erreur lors de la récupération des données de l'API:", error);
    });
}

//récupère la liste des communes
/*getCommunes("liste_communes")


const code_insee = () =>{
    geomatchingBtn.addEventListener('click', () =>{
        return select.value
    })
}

 // Fonction pour envoyer un message à map.html
 function sendMessageToMap(message) {
    mapIframe.contentWindow.postMessage(message, "*");
}

sendMessageToMap({type: "action", data: "your-data"})*/