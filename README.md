# Doce Pasos

Juego de fútbol en 3D en el navegador: tanda de penales contra la computadora y serie de tiros libres con barrera. No necesita build: son `index.html`, el modelo de los jugadores (`jugador.js`) y la captura de movimiento (`mocap.js`). Usa three.js r128 (desde cdnjs y jsDelivr), así que necesita internet y un navegador con WebGL.

## Cómo jugar

Abrí `index.html` en el navegador, directo desde el disco o desde cualquier servidor estático. Si falta `jugador.js`, el juego usa jugadores simples hechos con cilindros; si falta `mocap.js`, el remate se anima por código.

- **Pateando:** primero apuntás deslizando el dedo (o arrastrando el mouse) desde la pelota hacia el arco: donde termina el trazo es adonde va la pelota. El efecto es opcional: un trazo recto sale sin efecto, y si lo curvás a propósito la pelota toma efecto para ese lado. Después elegís la potencia frenando la barra con un toque: en la franja verde sale precisa; si te pasás, se puede ir arriba. La trayectoria se ve antes de patear.
- **Atajando (penales):** tocá el arco donde creés que va la pelota. Si te tirás antes del remate, el pateador te puede leer y cambiar de palo.
- **Penales:** cinco por lado, alternados, y muerte súbita si hay empate.
- **Tiros libres:** cinco tiros desde distintos lugares, entre 25 y 34 metros, con barrera que salta y arquero que lee la trayectoria (cuanto más lejos, más tiempo tiene para acomodarse). Pasala por arriba de la barrera o rodeala con efecto. El récord queda guardado en el navegador.

Teclado: flechas para apuntar, `A` y `D` para el efecto (opcional) y `Espacio` para pasar a la potencia; otro `Espacio` frena la barra y patea. Atajando: `←` `→` para tirarte (con `Shift`, arriba), `↑` salto, `↓` bloqueo.

Tres dificultades: Fácil, Normal y Difícil.

## Jugadores y animación

Cada equipo tiene un plantel con nombre, número, altura, tono de piel, peinado, barba, botines y estilo de remate propios.

`jugador.js` es el avatar de Ready Player Me que viene en los ejemplos de three.js (`examples/models/gltf/readyplayer.me.glb`), sin el sombrero. Va como script, con el GLB en base64, para que cargue también desde el disco y en páginas aisladas, donde no se pueden descargar archivos. El juego le cambia la ropa en el shader según el equipo y le arma el pelo con una segunda capa sobre la cabeza.

`mocap.js` tiene cuatro remates reales con carrera previa, tomados de la base de captura de movimiento de Carnegie Mellon (clips 10_02, 10_05, 10_06 y 11_01, conversión BVH de B. Hahne) y reducidos a posiciones de articulaciones. El arquero y la barrera se animan por código.

The data used in this project was obtained from mocap.cs.cmu.edu. The database was created with funding from NSF EIA-0196217.

## APK de Android

`dist/DocePasos.apk` es la app para Android 5.0 o superior: abre el juego a pantalla completa en un WebView, con todo incluido (three.js, tipografías, modelo y captura de movimiento), así que funciona sin internet. Para instalarla hay que permitir la instalación de apps de origen desconocido.

Se arma con `android/build.py`, sin Gradle ni el SDK de Android: usa el `aapt2` y la plataforma que vienen dentro de apktool, smali para el código de la actividad (`android/smali`) y `jarsigner` del JDK. Las instrucciones están al principio del script. La firma es de prueba (`android/debug.jks`, contraseña `docepasos`); para publicar en Play Store haría falta una clave propia y un `targetSdkVersion` más nuevo.
