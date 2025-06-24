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

function createHistoricalPlanOverlay() {

  var imageBounds = [
    [59.9414442615, 30.2918196905],   // юго-запад (левый нижний)
    [59.9572002615, 30.3365046905]    // северо-восток (правый верхний)
  ];
  
  return L.imageOverlay('historical_plans/1828_shubert.png', imageBounds, {
    opacity: 1
  });
}

var historicalPlan = createHistoricalPlanOverlay();