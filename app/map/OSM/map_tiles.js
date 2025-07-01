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

function createFloorPlanOverlay() {
  var imageBounds = [
    [59.94797825300306, 30.30886979410739],
    [59.952138591203415, 30.32291672325872]
  ];
  return L.imageOverlay('historical_plans/02_floor_ppk.png', imageBounds, {
    opacity: 0.5
  });
}

function createMinihPlanOverlay() {
  var imageBounds = [
    [59.94738371665793, 30.305109247591687], // юго-запад (левый нижний)
    [59.953554417377035, 30.32594182602913] // северо-восток (правый верхний)
  ];
  return L.imageOverlay('historical_plans/minih_plan_1730.png', imageBounds, {
    opacity: 1
  });
}

var historicalPlan = createHistoricalPlanOverlay();