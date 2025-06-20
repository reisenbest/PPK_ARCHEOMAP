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

addLocalTileLayer(map, mapBounds);



// === Статичный маркер Петропавловской крепости ===
L.marker([59.95, 30.3167], { icon: monumentIcon })
  .addTo(map)
  .bindPopup("Петропавловская крепость")
  .openPopup();

// === Координаты мыши ===

// Добавляем контрол координат
addMousePositionControl(map);

// === Работа с Qt WebChannel и маркерами ===
let monumentMarkers = [];      // маркеры памятников
let polygonPointMarkers = [];  // маркеры точек полигонов (если нужны, можно убрать)
let polygonLayers = [];        // отрисованные полигоны

function clearPolygonPointMarkers() {
  polygonPointMarkers.forEach(m => map.removeLayer(m));
  polygonPointMarkers = [];
}

function clearPolygonLayers() {
  polygonLayers.forEach(layer => map.removeLayer(layer));
  polygonLayers = [];
}

function updateMarkers() {
  // Удаляем старые маркеры памятников
  monumentMarkers.forEach(marker => map.removeLayer(marker));
  monumentMarkers = [];

  // Удаляем старые полигоны и точки
  clearPolygonLayers();
  clearPolygonPointMarkers();

  bridge.get_monuments_markers(function (markers) {
    markers.forEach(m => {
      const marker = L.marker([m.lat, m.lng], { icon: monumentIcon })
        .addTo(map)
        .bindPopup(m.label);

      marker.on('click', () => {
        // При клике удаляем старые полигоны и точки
        clearPolygonLayers();
        clearPolygonPointMarkers();

        if (m.polygons && m.polygons.length > 0) {
          m.polygons.forEach(polygonCoords => {
            // polygonCoords — массив списков точек (обычно polygonCoords[0] — внешняя граница)
            // Преобразуем каждую точку из [lng, lat] в [lat, lng]
            const latlngs = polygonCoords[0].map(pt => [pt[1], pt[0]]);

            // Создаем и добавляем полигон с заливкой и границей
            const polygon = L.polygon(latlngs, {
              color: 'blue',       // цвет линии
              weight: 2,           // толщина линии
              fillColor: 'lightblue', // цвет заливки
              fillOpacity: 0.4     // прозрачность заливки
            }).addTo(map);

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

// === Установка канала WebChannel ===
new QWebChannel(qt.webChannelTransport, function (channel) {
  window.bridge = channel.objects.bridge;

  // При первом запуске — загрузка маркеров
  updateMarkers();

  // Делаем функцию глобальной, чтобы вызывать из Python
  window.updateMarkersFromQt = updateMarkers;
});
