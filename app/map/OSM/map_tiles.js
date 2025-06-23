// map_tiles.js

function createLocalTileLayer(mapBounds) {
  return L.tileLayer("tiles2/{z}/{x}/{y}.png", {
    bounds: mapBounds,
    minZoom: 15,
    maxZoom: 20,
    tileSize: 256,
    noWrap: true,
    errorTileUrl: "blank.png"
  });
}