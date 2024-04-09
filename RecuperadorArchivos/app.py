import os
import shutil
import zipfile
import tempfile
import shutil
from PIL import Image

# Definir una lista de tuplas con el tipo de archivo y su firma hexadecimal correspondiente
tipos_archivo = [
    ("JPEG", "FF D8 FF E0"),
    ("PNG", "89 50 4E 47 0D 0A 1A 0A"),
    ("GIF", "47 49 46 38"),
    ("PDF", "25 50 44 46"),
    ("MP3", "FF FB"),
    ("MP4", "66 74 79 70"),
    ("JPEG2000", "00 00 00 0C 6A 50 20 20"),
    ("BMP", "42 4D"),
    ("TIFF", "49 49 2A 00"),
    ("TIFF", "4D 4D 00 2A"),
    ("AVI", "52 49 46 46"),
    ("WAV", "52 49 46 46"),
    ("FLAC", "66 4C 61 43"),
    ("MOV", "6D 6F 6F 76"),
    ("WMV", "30 26 B2 75"),
    ("EXE", "4D 5A")
]

# Definir la ruta de salida para los archivos recuperados
ruta_salida = "D:/recuperados"

def recuperar_archivos(directorio):
    for tipo, firma_hex in tipos_archivo:
        firma_bytes = bytes.fromhex(firma_hex.replace(" ", ""))
        for root, _, files in os.walk(directorio):
            for filename in files:
                ruta_archivo = os.path.join(root, filename)
                try:
                    with open(ruta_archivo, 'rb') as f:
                        contenido = f.read(len(firma_bytes))
                    if contenido.startswith(firma_bytes):
                        print(f"Archivo encontrado: {ruta_archivo} (Tipo: {tipo})")
                        # Recuperar y reparar archivos según su tipo
                        if tipo == "JPEG":
                            recuperar_y_reparar_jpeg(ruta_archivo)
                        elif tipo == "PNG":
                            recuperar_y_reparar_png(ruta_archivo)
                        elif tipo == "GIF":
                            recuperar_y_reparar_gif(ruta_archivo)
                        elif tipo == "PDF":
                            recuperar_y_reparar_pdf(ruta_archivo)
                        elif tipo == "MP3":
                            recuperar_y_reparar_mp3(ruta_archivo)
                        elif tipo == "MP4":
                            recuperar_y_reparar_mp4(ruta_archivo)
                        elif tipo in ["JPEG2000", "BMP", "TIFF"]:
                            recuperar_y_reparar_imagen(ruta_archivo)
                        elif tipo in ["AVI", "WAV", "FLAC", "MOV", "WMV"]:
                            recuperar_y_reparar_audio_video(ruta_archivo)
                        elif tipo == "EXE":
                            recuperar_y_reparar_exe(ruta_archivo)
                        # Añadir más casos para otros tipos de archivo si es necesario
                except IOError as e:
                    print(f"No se pudo leer el archivo: {ruta_archivo}, Error: {e}")

def recuperar_y_reparar_jpeg(ruta_archivo):
    try:
        # Leer el contenido del archivo JPEG
        with open(ruta_archivo, 'rb') as f:
            contenido = f.read()

        # Identificar la marca de final de archivo JPEG
        end_marker = b'\xff\xd9'

        # Encontrar la posición del final del archivo JPEG
        end_pos = contenido.find(end_marker)
        if end_pos != -1:
            # Si se encuentra la marca de final, recorta el contenido del archivo hasta esa posición
            contenido_recuperado = contenido[:end_pos + len(end_marker)]

            # Guardar el contenido recuperado en un nuevo archivo
            ruta_archivo_recuperado = os.path.join(ruta_salida, os.path.basename(ruta_archivo) + '_recovered.jpg')
            with open(ruta_archivo_recuperado, 'wb') as f:
                f.write(contenido_recuperado)

            print(f"Archivo JPEG recuperado y guardado en: {ruta_archivo_recuperado}")

            # Opcionalmente, puedes eliminar el archivo original
            # os.remove(ruta_archivo)
    except Exception as e:
        print(f"Error al recuperar y reparar el archivo JPEG: {e}")

def recuperar_y_reparar_png(ruta_archivo):
    try:
        # Leer el contenido del archivo PNG
        with open(ruta_archivo, 'rb') as f:
            contenido = f.read()

        # Identificar la marca de final de archivo PNG
        end_marker = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'

        # Encontrar la posición del final del archivo PNG
        end_pos = contenido.find(end_marker)
        if end_pos != -1:
            # Si se encuentra la marca de final, recorta el contenido del archivo hasta esa posición
            contenido_recuperado = contenido[:end_pos + len(end_marker)]

            # Guardar el contenido recuperado en un nuevo archivo
            ruta_archivo_recuperado = os.path.join(ruta_salida, os.path.basename(ruta_archivo) + '_recovered.png')
            with open(ruta_archivo_recuperado, 'wb') as f:
                f.write(contenido_recuperado)

            print(f"Archivo PNG recuperado y guardado en: {ruta_archivo_recuperado}")

            # Opcionalmente, puedes eliminar el archivo original
            # os.remove(ruta_archivo)
    except Exception as e:
        print(f"Error al recuperar y reparar el archivo PNG: {e}")
    pass

def recuperar_y_reparar_gif(ruta_archivo):
    try:
        # Leer el contenido del archivo GIF
        with open(ruta_archivo, 'rb') as f:
            contenido = f.read()

        # Identificar la marca de final de archivo GIF
        end_marker = b'\x3B'

        # Encontrar la posición del final del archivo GIF
        end_pos = contenido.rfind(end_marker)
        if end_pos != -1:
            # Si se encuentra la marca de final, recorta el contenido del archivo hasta esa posición
            contenido_recuperado = contenido[:end_pos + len(end_marker)]

            # Guardar el contenido recuperado en un nuevo archivo
            ruta_archivo_recuperado = os.path.join(ruta_salida, os.path.basename(ruta_archivo) + '_recovered.gif')
            with open(ruta_archivo_recuperado, 'wb') as f:
                f.write(contenido_recuperado)

            print(f"Archivo GIF recuperado y guardado en: {ruta_archivo_recuperado}")

            # Opcionalmente, puedes eliminar el archivo original
            # os.remove(ruta_archivo)
    except Exception as e:
        print(f"Error al recuperar y reparar el archivo GIF: {e}")
    pass

def recuperar_y_reparar_pdf(ruta_archivo):
    try:
        # Leer el contenido del archivo PDF
        with open(ruta_archivo, 'rb') as f:
            contenido = f.read()

        # Identificar la marca de final de archivo PDF
        end_marker = b'\x25\x25\x45\x4F\x46'

        # Encontrar la posición del final del archivo PDF
        end_pos = contenido.find(end_marker)
        if end_pos != -1:
            # Si se encuentra la marca de final, recorta el contenido del archivo hasta esa posición
            contenido_recuperado = contenido[:end_pos + len(end_marker)]

            # Guardar el contenido recuperado en un nuevo archivo
            ruta_archivo_recuperado = os.path.join(ruta_salida, os.path.basename(ruta_archivo) + '_recovered.pdf')
            with open(ruta_archivo_recuperado, 'wb') as f:
                f.write(contenido_recuperado)

            print(f"Archivo PDF recuperado y guardado en: {ruta_archivo_recuperado}")

            # Opcionalmente, puedes eliminar el archivo original
            # os.remove(ruta_archivo)
    except Exception as e:
        print(f"Error al recuperar y reparar el archivo PDF: {e}")
    pass

def recuperar_y_reparar_mp3(ruta_archivo):
    try:
        # Leer el contenido del archivo MP3
        with open(ruta_archivo, 'rb') as f:
            contenido = f.read()

        # Identificar la marca de final de archivo MP3
        end_marker = b'\xFF\xFB'

        # Encontrar la posición del final del archivo MP3
        end_pos = contenido.find(end_marker)
        if end_pos != -1:
            # Si se encuentra la marca de final, recorta el contenido del archivo hasta esa posición
            contenido_recuperado = contenido[:end_pos + len(end_marker)]

            # Guardar el contenido recuperado en un nuevo archivo
            ruta_archivo_recuperado = os.path.join(ruta_salida, os.path.basename(ruta_archivo) + '_recovered.mp3')
            with open(ruta_archivo_recuperado, 'wb') as f:
                f.write(contenido_recuperado)

            print(f"Archivo MP3 recuperado y guardado en: {ruta_archivo_recuperado}")

            # Opcionalmente, puedes eliminar el archivo original
            # os.remove(ruta_archivo)
    except Exception as e:
        print(f"Error al recuperar y reparar el archivo MP3: {e}")
    pass

def recuperar_y_reparar_mp4(ruta_archivo):
    try:
        # Leer el contenido del archivo MP4
        with open(ruta_archivo, 'rb') as f:
            contenido = f.read()

        # Identificar la marca de final de archivo MP4
        end_marker = b'\x00\x00\x00\x00\x1C\x66\x74\x79\x70\x6D\x70\x34\x32\x00\x00\x00\x00\x6D\x70\x34\x32\x69\x73\x6F\x6D'

        # Encontrar la posición del final del archivo MP4
        end_pos = contenido.find(end_marker)
        if end_pos != -1:
            # Si se encuentra la marca de final, recorta el contenido del archivo hasta esa posición
            contenido_recuperado = contenido[:end_pos + len(end_marker)]

            # Guardar el contenido recuperado en un nuevo archivo
            ruta_archivo_recuperado = os.path.join(ruta_salida, os.path.basename(ruta_archivo) + '_recovered.mp4')
            with open(ruta_archivo_recuperado, 'wb') as f:
                f.write(contenido_recuperado)

            print(f"Archivo MP4 recuperado y guardado en: {ruta_archivo_recuperado}")

            # Opcionalmente, puedes eliminar el archivo original
            # os.remove(ruta_archivo)
    except Exception as e:
        print(f"Error al recuperar y reparar el archivo MP4: {e}")
    pass

def recuperar_y_reparar_imagen(ruta_archivo):
    try:
        # Abrir la imagen usando PIL (Python Imaging Library)
        with Image.open(ruta_archivo) as img:            
            # Guardar la imagen reparada
            ruta_archivo_reparado = os.path.join(ruta_salida, os.path.basename(ruta_archivo) + '_repaired' + os.path.splitext(ruta_archivo)[1])
            img.save(ruta_archivo_reparado)
            
            print(f"Imagen reparada guardada en: {ruta_archivo_reparado}")
    except Exception as e:
        print(f"Error al recuperar y reparar la imagen: {e}")
    pass

def recuperar_y_reparar_audio_video(ruta_archivo):
    def recuperar_y_reparar_audio_video(ruta_archivo):
        try:
            # Leer el contenido del archivo de audio/video
            with open(ruta_archivo, 'rb') as f:
                contenido = f.read()

            # Identificar la marca de final de archivo de audio/video
            end_marker = b'\x00\x00\x00\x00\x00\x00\x00\x00'

            # Encontrar la posición del final del archivo de audio/video
            end_pos = contenido.find(end_marker)
            if end_pos != -1:
                # Si se encuentra la marca de final, recorta el contenido del archivo hasta esa posición
                contenido_recuperado = contenido[:end_pos + len(end_marker)]

                # Guardar el contenido recuperado en un nuevo archivo
                ruta_archivo_recuperado = os.path.join(ruta_salida, os.path.basename(ruta_archivo) + '_recovered')
                with open(ruta_archivo_recuperado, 'wb') as f:
                    f.write(contenido_recuperado)

                print(f"Archivo de audio/video recuperado y guardado en: {ruta_archivo_recuperado}")

                # Opcionalmente, puedes eliminar el archivo original
                # os.remove(ruta_archivo)
        except Exception as e:
            print(f"Error al recuperar y reparar el archivo de audio/video: {e}")
    pass

def recuperar_y_reparar_exe(ruta_archivo):
    try:
        # Leer el contenido del archivo EXE
        with open(ruta_archivo, 'rb') as f:
            contenido = f.read()

        # Identificar la marca de final de archivo EXE
        end_marker = b'\x4D\x5A'

        # Encontrar la posición del final del archivo EXE
        end_pos = contenido.find(end_marker)
        if end_pos != -1:
            # Si se encuentra la marca de final, recorta el contenido del archivo hasta esa posición
            contenido_recuperado = contenido[:end_pos + len(end_marker)]

            # Guardar el contenido recuperado en un nuevo archivo
            ruta_archivo_recuperado = os.path.join(ruta_salida, os.path.basename(ruta_archivo) + '_recovered.exe')
            with open(ruta_archivo_recuperado, 'wb') as f:
                f.write(contenido_recuperado)

            print(f"Archivo EXE recuperado y guardado en: {ruta_archivo_recuperado}")

            # Opcionalmente, puedes eliminar el archivo original
            # os.remove(ruta_archivo)
    except Exception as e:
        print(f"Error al recuperar y reparar el archivo EXE: {e}")
    pass

# Directorio a escanear en busca de archivos para recuperar
directorio_a_escanear = '\\\\.\\D:'
recuperar_archivos(directorio_a_escanear)
