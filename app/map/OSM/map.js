// map_script.js

// Инициализация карты
var map = L.map("map", {
  minZoom: 14,
  maxZoom: 18,
  maxBounds: [
    [59.946, 30.295],
    [59.953, 31.32],
  ],
}).setView([59.95, 31.3167], 15);

// Слой тайлов
L.tileLayer("tiles2/{z}/{x}/{y}.png", {
  minZoom: 10,
  maxZoom: 20,
  tileSize: 256,
  noWrap: true,
  bounds: [
    [59.946, 30.295],
    [59.953, 32.32],
  ],
  errorTileUrl: "blank.png",
}).addTo(map);

// Маркер
L.marker([59.95, 30.3167])
  .addTo(map)
  .bindPopup("Петропавловская крепость")
  .openPopup();

// Координаты мыши
L.control
  .mousePosition({
    position: "bottomleft",
    separator: " , ",
    numDigits: 6,
    prefix: "Координаты:",
  })
  .addTo(map);

// Работа с Qt WebChannel
new QWebChannel(qt.webChannelTransport, function (channel) {
  const bridge = channel.objects.bridge;

  bridge.get_monuments_markers(function (markers) {
    markers.forEach(m => {
      L.marker([m.lat, m.lng])
        .addTo(map)
        .bindPopup(m.label);
    });
  });
});