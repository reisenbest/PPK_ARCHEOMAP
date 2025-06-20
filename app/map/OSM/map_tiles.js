// map_tiles.js

function addLocalTileLayer(map, mapBounds) {
  L.tileLayer("tiles2/{z}/{x}/{y}.png", {
    bounds: mapBounds,
    minZoom: 15,
    maxZoom: 20,
    tileSize: 256,
    noWrap: true,
    errorTileUrl: "blank.png"
  }).addTo(map);
}