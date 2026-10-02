# Doce Pasos

Juego de penales en 3D en el navegador. No necesita build: son `index.html` y el modelo de los jugadores, `jugador.js`. Usa three.js r128 (desde cdnjs y jsDelivr), así que necesita internet y un navegador con WebGL.

## Cómo jugar

Abrí `index.html` en el navegador, directo desde el disco o desde cualquier servidor estático. `jugador.js` tiene que estar en la misma carpeta; si falta, el juego usa jugadores simples hechos con cilindros.

Cada equipo patea cinco penales, alternados; si quedan empatados se sigue a muerte súbita. Tanto pateando como atajando ves la jugada desde atrás del pateador.

- **Pateando:** tocá el arco donde querés poner la pelota y frená la barra de potencia en la franja verde. Más fuerte va más rápido, pero se puede ir arriba.
- **Atajando:** tocá el arco donde creés que va la pelota y el arquero se tira ahí. Si te tirás antes del remate, el pateador te puede leer y cambiar de palo.

Teclado: flechas para apuntar y `Espacio` para patear. Atajando: `←` `→` para tirarte (con `Shift`, arriba), `↑` salto, `↓` bloqueo.

Tres dificultades: Fácil, Normal y Difícil.

## Jugadores

`jugador.js` es el avatar de Ready Player Me que viene en los ejemplos de three.js (`examples/models/gltf/readyplayer.me.glb`), sin el sombrero. Va como script, con el GLB en base64, para que cargue también desde el disco y en páginas aisladas, donde no se pueden descargar archivos. El juego le cambia la ropa en el shader según el equipo: camiseta (con bastones y número), cortos, medias, botines, guantes del arquero y pelo. El esqueleto se anima por código para la carrera, el remate y la atajada.
