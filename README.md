# Doce Pasos

Juego de fútbol en 3D en el navegador: tanda de penales contra la computadora y serie de tiros libres con barrera. No necesita build: son `index.html`, el modelo de los jugadores (`jugador.js`) y la captura de movimiento (`mocap.js`). Usa three.js r128 (desde cdnjs y jsDelivr), así que necesita internet y un navegador con WebGL.

## Cómo jugar

Abrí `index.html` en el navegador, directo desde el disco o desde cualquier servidor estático. Si falta `jugador.js`, el juego usa jugadores simples hechos con cilindros; si falta `mocap.js`, el remate se anima por código.

- **Pateando:** deslizá el dedo (o arrastrá el mouse) desde la pelota hacia el arco. Donde termina el trazo es adonde va la pelota; si el trazo es curvo, la pelota toma efecto para ese lado; cuanto más rápido, más fuerte, pero si te pasás de la franja verde se puede ir arriba. Mientras deslizás ves la trayectoria.
- **Atajando (penales):** tocá el arco donde creés que va la pelota. Si te tirás antes del remate, el pateador te puede leer y cambiar de palo.
- **Penales:** cinco por lado, alternados, y muerte súbita si hay empate.
- **Tiros libres:** cinco tiros desde distintos lugares, entre 18 y 28 metros, con barrera que salta y arquero que lee la trayectoria. Pasala por arriba de la barrera o rodeala con efecto. El récord queda guardado en el navegador.

Teclado: flechas para apuntar, `A` y `D` para el efecto, `W` y `S` para la potencia y `Espacio` para patear. Atajando: `←` `→` para tirarte (con `Shift`, arriba), `↑` salto, `↓` bloqueo.

Tres dificultades: Fácil, Normal y Difícil.

## Jugadores y animación

Cada equipo tiene un plantel con nombre, número, altura, tono de piel, peinado, barba, botines y estilo de remate propios.

`jugador.js` es el avatar de Ready Player Me que viene en los ejemplos de three.js (`examples/models/gltf/readyplayer.me.glb`), sin el sombrero. Va como script, con el GLB en base64, para que cargue también desde el disco y en páginas aisladas, donde no se pueden descargar archivos. El juego le cambia la ropa en el shader según el equipo y le arma el pelo con una segunda capa sobre la cabeza.

`mocap.js` tiene cuatro remates reales con carrera previa, tomados de la base de captura de movimiento de Carnegie Mellon (clips 10_02, 10_05, 10_06 y 11_01, conversión BVH de B. Hahne) y reducidos a posiciones de articulaciones. El arquero y la barrera se animan por código.

The data used in this project was obtained from mocap.cs.cmu.edu. The database was created with funding from NSF EIA-0196217.
