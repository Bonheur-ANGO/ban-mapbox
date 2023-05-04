export async function getAllLayers(){
    let layers = [];
    let url = await fetch('https://wxs.ign.fr/static/vectorTiles/styles/BDTOPO/routier.json')
    let data = await url.json()
    data.layers.map(layer => layers.push(layer.id))
    return layers
}