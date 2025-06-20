function addMousePositionControl(map) {
  L.control
    .mousePosition({
      position: "bottomleft",
      separator: " , ",
      numDigits: 6,
      prefix: "Координаты:",
    })
    .addTo(map);
}