// === Инициализация карты ===
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

addLocalTileLayer(map, mapBounds);

// === Статичный маркер Петропавловской крепости ===
L.marker([59.95, 30.3167], { icon: monumentIcon })
  .addTo(map)
  .bindPopup("Петропавловская крепость")
  .openPopup();

// === Координаты мыши ===
addMousePositionControl(map);

// === Работа с Qt WebChannel и маркерами ===
let monumentMarkers = [];
let polygonPointMarkers = [];
let polygonLayers = [];
let selectedPolygon = null;

function clearPolygonPointMarkers() {
  polygonPointMarkers.forEach(m => map.removeLayer(m));
  polygonPointMarkers = [];
}

function clearPolygonLayers() {
  polygonLayers.forEach(layer => map.removeLayer(layer));
  polygonLayers = [];
  selectedPolygon = null;
}

function updateMarkers() {
  monumentMarkers.forEach(marker => map.removeLayer(marker));
  monumentMarkers = [];

  clearPolygonLayers();
  clearPolygonPointMarkers();

  bridge.get_monuments_markers(function (markers) {
    markers.forEach(m => {
      // === ВСТАВКА кастомного popup с кнопкой ===
      const popupContent = `
        <strong>${m.label}</strong><br>
        <a href="#" onclick="showMonumentDetails(${m.monument_id}); return false;">
          Смотреть подробнее
        </a>
      `;

      const marker = L.marker([m.lat, m.lng], { icon: monumentIcon })
        .addTo(map)
        .bindPopup(popupContent);

      // === Клик по маркеру — загрузка полигонов ===
      marker.on('click', () => {
        clearPolygonLayers();
        clearPolygonPointMarkers();

        if (m.polygons && m.polygons.length > 0) {
          m.polygons.forEach(polygonCoords => {
            const latlngs = polygonCoords[0].map(pt => [pt[1], pt[0]]);

            const polygon = L.polygon(latlngs, {
              color: 'blue',
              weight: 2,
              fillColor: 'lightblue',
              fillOpacity: 0.4
            }).addTo(map);

            // === Реакция на клик по полигону (выделение, центрирование) ===
            polygon.on('click', () => {
              if (selectedPolygon) {
                selectedPolygon.setStyle({
                  color: 'blue',
                  weight: 2
                });
              }

              polygon.setStyle({
                color: 'red',
                weight: 4
              });

              map.fitBounds(polygon.getBounds(), { padding: [20, 20] });
              selectedPolygon = polygon;
            });

            polygonLayers.push(polygon);
          });
        } else {
          console.log(`Памятник "${m.label}" не содержит полигонов`);
        }
      });

      monumentMarkers.push(marker);
    });
  });
}

// === ВСТАВКА функции открытия деталей ===
function showMonumentDetails(monumentId) {
  if (window.bridge && bridge.open_monument_details) {
    bridge.open_monument_details(monumentId);
  } else {
    console.error("bridge или open_monument_details не определён");
  }
}

// === Установка канала WebChannel ===
new QWebChannel(qt.webChannelTransport, function (channel) {
  window.bridge = channel.objects.bridge;
  updateMarkers();
  window.updateMarkersFromQt = updateMarkers;
});
