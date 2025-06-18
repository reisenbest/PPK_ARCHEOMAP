// === Инициализация карты ===
// Инициализация карты с правильными границами
     var mapBounds = [
  [59.944, 30.300078], // юго-запад
  [59.955, 30.333123]  // северо-восток
];

var map = L.map('map', {
  minZoom: 15,
  maxZoom: 20,
  maxBounds: mapBounds,
  maxBoundsViscosity: 1.0
}).setView([59.970, 30.356], 15); // Центр ближе к Петропавловке

L.tileLayer("tiles2/{z}/{x}/{y}.png", {
  bounds: mapBounds, // Используем те же границы
  minZoom: 15,
  maxZoom: 20,
  tileSize: 256,
  noWrap: true,
  errorTileUrl: "blank.png"
}).addTo(map);
// === Статичный маркер Петропавловской крепости ===
L.marker([59.95, 30.3167])
  .addTo(map)
  .bindPopup("Петропавловская крепость")
  .openPopup();

// === Координаты мыши ===
L.control
  .mousePosition({
    position: "bottomleft",
    separator: " , ",
    numDigits: 6,
    prefix: "Координаты:",
  })
  .addTo(map);

// === Работа с Qt WebChannel и маркерами ===
let monumentMarkers = [];  // массив для хранения маркеров

function updateMarkers() {
  // Удаляем старые маркеры
  monumentMarkers.forEach(marker => map.removeLayer(marker));
  monumentMarkers = [];

  bridge.get_monuments_markers(function (markers) {
    markers.forEach(m => {
      const marker = L.marker([m.lat, m.lng])
        .addTo(map)
        .bindPopup(m.label);
      monumentMarkers.push(marker);
    });
  });
}

// === Установка канала WebChannel ===
new QWebChannel(qt.webChannelTransport, function (channel) {
  window.bridge = channel.objects.bridge;

  // При первом запуске — загрузка маркеров
  updateMarkers();

  // Делаем функцию глобальной, чтобы вызывать из Python
  window.updateMarkersFromQt = updateMarkers;
});
