#!/usr/bin/env python3
"""Arma el APK de Doce Pasos: un WebView a pantalla completa con el juego en los assets.

No usa Gradle ni el SDK de Android. Necesita:
  - aapt2 y android-framework.jar (vienen dentro de apktool-lib, en Maven Central:
    org.apktool:apktool-lib:3.0.3 -> prebuilt/linux/aapt2 y prebuilt/android-framework.jar)
  - smali 2.5.2 con sus dependencias (Maven Central: org.smali:smali:2.5.2), como classpath
  - three@0.128.0 y @fontsource/{big-shoulders-display,archivo} de npm, para jugar sin internet
  - keytool y jarsigner (vienen con el JDK)

Uso:
  python3 android/build.py --aapt2 RUTA --framework RUTA --smali-cp CLASSPATH \
      --three RUTA/three --fonts RUTA_FUENTES --out dist/DocePasos.apk [--keystore android/debug.jks]
"""
import argparse
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

FONTS = {
    # familia, peso -> archivo de @fontsource
    ('Big Shoulders Display', 700): 'big-shoulders-display-latin-700-normal.woff2',
    ('Big Shoulders Display', 800): 'big-shoulders-display-latin-800-normal.woff2',
    ('Big Shoulders Display', 900): 'big-shoulders-display-latin-900-normal.woff2',
    ('Archivo', 400): 'archivo-latin-400-normal.woff2',
    ('Archivo', 500): 'archivo-latin-500-normal.woff2',
    ('Archivo', 700): 'archivo-latin-700-normal.woff2',
}
LIBS = {
    'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js': ('build/three.min.js', 'lib/three.min.js'),
    'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js': ('examples/js/loaders/GLTFLoader.js', 'lib/GLTFLoader.js'),
    'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/utils/SkeletonUtils.js': ('examples/js/utils/SkeletonUtils.js', 'lib/SkeletonUtils.js'),
}


def run(cmd):
    print('$', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def offline_assets(assets, three_dir, fonts_dir):
    """Copia el juego a assets/, con three.js y las fuentes locales en vez de los CDN."""
    html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    for url, (src, dst) in LIBS.items():
        if url not in html:
            sys.exit('index.html ya no usa ' + url + '; actualizá LIBS en build.py')
        html = html.replace(url, dst)
        os.makedirs(os.path.join(assets, os.path.dirname(dst)), exist_ok=True)
        shutil.copy(os.path.join(three_dir, src), os.path.join(assets, dst))
    faces = []
    os.makedirs(os.path.join(assets, 'fonts'), exist_ok=True)
    for (family, weight), name in FONTS.items():
        found = None
        for base, _, files in os.walk(fonts_dir):
            if name in files:
                found = os.path.join(base, name)
                break
        if not found:
            sys.exit('falta la fuente ' + name)
        shutil.copy(found, os.path.join(assets, 'fonts', name))
        faces.append('@font-face{font-family:"%s";font-weight:%d;font-style:normal;font-display:swap;src:url(fonts/%s) format("woff2")}' % (family, weight, name))
    # las fuentes de Google Fonts se reemplazan por las locales
    html, n = re.subn(r'<link rel="preconnect"[^>]*>\n|<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\n', '', html)
    html = html.replace('<style>', '<style>\n' + '\n'.join(faces) + '\n', 1)
    open(os.path.join(assets, 'index.html'), 'w', encoding='utf-8').write(html)
    for name in ('jugador.js', 'mocap.js'):
        shutil.copy(os.path.join(ROOT, name), os.path.join(assets, name))


def align(src, dst, boundary=4):
    """zipalign: las entradas sin comprimir quedan alineadas a 4 bytes (lo que hace zipalign -p 4)."""
    zin = zipfile.ZipFile(src)
    with open(dst, 'wb') as out:
        entries = []
        for info in zin.infolist():
            data = zin.read(info.filename)
            raw = data
            method = info.compress_type
            if method == zipfile.ZIP_DEFLATED:
                import zlib
                c = zlib.compressobj(9, zlib.DEFLATED, -15)
                raw = c.compress(data) + c.flush()
            name = info.filename.encode('utf-8')
            offset = out.tell()
            extra = b''
            if method == zipfile.ZIP_STORED:
                pad = (boundary - (offset + 30 + len(name)) % boundary) % boundary
                extra = b'\x00' * pad
            crc = zipfile.crc32(data) & 0xffffffff
            dt = info.date_time
            dostime = (dt[3] << 11) | (dt[4] << 5) | (dt[5] // 2)
            dosdate = ((dt[0] - 1980) << 9) | (dt[1] << 5) | dt[2]
            out.write(struct.pack('<IHHHHHIIIHH', 0x04034b50, 20, 0x0800, method, dostime, dosdate, crc, len(raw), len(data), len(name), len(extra)))
            out.write(name)
            out.write(extra)
            out.write(raw)
            entries.append((name, method, dostime, dosdate, crc, len(raw), len(data), offset))
        cd = out.tell()
        for name, method, dostime, dosdate, crc, csize, usize, offset in entries:
            out.write(struct.pack('<IHHHHHHIIIHHHHHII', 0x02014b50, 20, 20, 0x0800, method, dostime, dosdate, crc, csize, usize, len(name), 0, 0, 0, 0, 0, offset))
            out.write(name)
        end = out.tell()
        out.write(struct.pack('<IHHHHIIH', 0x06054b50, 0, 0, len(entries), len(entries), end - cd, cd, 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--aapt2', required=True)
    ap.add_argument('--framework', required=True)
    ap.add_argument('--smali-cp', required=True)
    ap.add_argument('--three', required=True, help='carpeta del paquete npm three@0.128.0')
    ap.add_argument('--fonts', required=True, help='carpeta con los paquetes @fontsource')
    ap.add_argument('--out', default=os.path.join(ROOT, 'dist', 'DocePasos.apk'))
    ap.add_argument('--keystore', default=os.path.join(HERE, 'debug.jks'))
    a = ap.parse_args()

    work = tempfile.mkdtemp(prefix='docepasos-apk-')
    assets = os.path.join(work, 'assets')
    os.makedirs(assets)
    offline_assets(assets, a.three, a.fonts)

    compiled = os.path.join(work, 'res.zip')
    run([a.aapt2, 'compile', '--dir', os.path.join(HERE, 'res'), '-o', compiled])
    unsigned = os.path.join(work, 'unsigned.apk')
    run([a.aapt2, 'link', '-o', unsigned, '-I', a.framework, '--manifest', os.path.join(HERE, 'AndroidManifest.xml'),
         '-A', assets, '--min-sdk-version', '21', '--target-sdk-version', '28', '--version-code', '1', '--version-name', '1.0',
         '-0', 'glb', compiled])

    dex_dir = os.path.join(work, 'dex')
    os.makedirs(dex_dir)
    run(['java', '-cp', a.smali_cp, 'org.jf.smali.Main', 'assemble', '--api', '21', '-o', os.path.join(dex_dir, 'classes.dex'), os.path.join(HERE, 'smali')])
    with zipfile.ZipFile(unsigned, 'a', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(dex_dir, 'classes.dex'), 'classes.dex')

    if not os.path.exists(a.keystore):
        run(['keytool', '-genkeypair', '-keystore', a.keystore, '-storepass', 'docepasos', '-keypass', 'docepasos', '-alias', 'docepasos',
             '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000', '-dname', 'CN=Doce Pasos, O=Doce Pasos, C=AR'])
    run(['jarsigner', '-keystore', a.keystore, '-storepass', 'docepasos', '-keypass', 'docepasos', '-sigalg', 'SHA256withRSA',
         '-digestalg', 'SHA-256', unsigned, 'docepasos'])
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    align(unsigned, a.out)
    run(['jarsigner', '-verify', a.out])
    print('APK:', a.out, os.path.getsize(a.out) // 1024, 'KB')


if __name__ == '__main__':
    main()
