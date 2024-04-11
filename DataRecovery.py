import os # Módulo para interactuar con el sistema operativo
import time # Módulo para trabajar con fechas y horas
from datetime import timedelta # Clase para representar un intervalo de tiempo
import hashlib # Módulo para calcular resúmenes de mensajes y códigos hash

# La cantidad de bytes a leer depende de la capacidad del disco duro o memoria USB
# Tambien depende de cuanta ram tenga el sistema operativo
# Gama Baja 512 bytes y 2048 bytes
# Gama Media 2048 bytes a 8192 bytes
# Gama Alta 8192 bytes y 65536 bytes o más
size = 16777216  # Tamaño del bloque de lectura

# Directorio a escanear en busca de archivos para recuperar
drive = "\\\\.\\D:" # Disco duro o memoria USB a escanear
ruta_salida_base = "D:\\recuperados" # Directorio de salida para los archivos recuperados
total_time = 0  # Variable para almacenar el tiempo total transcurrido

# Función para formatear un timedelta como una cadena
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days} # Crear un diccionario con los días transcurridos
    d["hours"], rem = divmod(tdelta.seconds, 3600) # Calcular las horas transcurridas
    d["minutes"], d["seconds"] = divmod(rem, 60) # Calcular los minutos y segundos transcurridos
    return fmt.format(**d) # Formatear la cadena con los valores del diccionario

# Calcular el hash MD5 de un archivo
def generate_file_hash(file_path):
    hash_md5 = hashlib.md5() # Crear un objeto hash MD5
    with open(file_path, "rb") as file: # Leer el archivo en modo binario
        # Leer el archivo en bloques del valor de la variable size
        for chunk in iter(lambda: file.read(size), b""):
            hash_md5.update(chunk) # Actualizar el hash MD5 con el bloque actual
    return hash_md5.hexdigest() # Retornar el hash MD5 en formato hexadecimal

# Recuperar archivos de un disco duro o memoria USB
def recover_files(drive, signature, tipo, output_dir):
    start_time = time.time()  # Capturar el tiempo de inicio

    # Recuperar archivos de un disco duro o memoria USB
    try:
        # Leer el disco duro o memoria USB
        with open(drive, "rb") as fileD:
            offs = 0 # Desplazamiento de lectura
            rcvd = 0 # Contador de archivos recuperados
            recoveredPositions = {} # Diccionario para almacenar las posiciones de los archivos recuperados

            # Leer el disco duro o memoria USB en bloques de 4096 bytes
            while True:
                byte = fileD.read(size) # Leer un bloque de 4096 bytes

                # Si no se lee ningún byte, salir del bucle
                if not byte:
                    break

                found = byte.find(bytes.fromhex(signature)) # Buscar la firma hexadecimal en el bloque leído

                # Si se encuentra la firma hexadecimal, recuperar el archivo
                if found >= 0:
                    elapsed_time_seconds = time.time() - start_time  # Calcular el tiempo transcurrido en segundos

                    # Formatear el tiempo transcurrido en el formato deseado
                    elapsed_time_str = strfdelta(timedelta(seconds=int(elapsed_time_seconds)), "{days}:{hours}:{minutes}")

                    print(f'=============>Tiempo transcurrido: {elapsed_time_str} <=============\n') # Mostrar el tiempo transcurrido

                    print(f'=============> Archivo encontrado en la ubicación: {str(hex(found+(size*offs)))} <=============') # Mostrar la ubicación del archivo encontrado

                    # Verificar si la posición de recuperación ya está en el diccionario
                    if offs not in recoveredPositions:
                        recoveredPositions[offs] = set()  # Usar un conjunto para almacenar hashes de archivos recuperados en esta posición

                    # Leer el archivo desde la firma hexadecimal encontrada
                    file_content = byte[found:] # Leer el archivo desde la firma hexadecimal encontrada
                    file_hash = hashlib.md5(file_content).hexdigest() # Calcular el hash MD5 del contenido del archivo

                    # Verificar si el hash del contenido del archivo ya está en los archivos recuperados en esta posición
                    if file_hash not in recoveredPositions[offs]:
                        file_path = os.path.join(output_dir, f'{rcvd}.{tipo.lower()}') # Crear la ruta del archivo recuperado

                        # Escribir el archivo recuperado en la carpeta de salida
                        with open(file_path, "wb") as fileN:
                            fileN.write(file_content) # Escribir el contenido del archivo
                            recoveredPositions[offs].add(file_hash)  # Agregar el hash del archivo recuperado
                            
                            # Leer el resto del archivo desde el bloque actual
                            while True:
                                byte = fileD.read(size) # Leer un bloque de 4096 bytes
                                bfind = byte.find(bytes.fromhex(signature)) # Buscar la firma hexadecimal en el bloque leído

                                # Si se encuentra la firma hexadecimal, escribir el archivo recuperado
                                if bfind >= 0:
                                    fileN.write(byte[:bfind+len(bytes.fromhex(signature))]) # Escribir el archivo recuperado
                                    offs += byte[:bfind+len(bytes.fromhex(signature))].count(b'\n') # Actualizar el desplazamiento
                                    print(f'=============> Escribiendo archivo en la ubicación: {rcvd}.{tipo.lower()} <=============\n') # Mostrar la ubicación del archivo recuperado
                                    break
                                else:
                                    fileN.write(byte) # Escribir el bloque leído
                        rcvd += 1 # Incrementar el contador de archivos recuperados
                    else:
                        offs += byte.count(b'\n') # Actualizar el desplazamiento

                offs += 1 # Incrementar el desplazamiento

    except Exception as e:
        print(f"Error: {e}\n") # Mostrar mensaje de error

    end_time = time.time()  # Capturar el tiempo de finalización
    elapsed_time_seconds = end_time - start_time  # Calcular el tiempo transcurrido en segundos

    # Formatear el tiempo transcurrido en el formato deseado
    elapsed_time_str = strfdelta(timedelta(seconds=int(elapsed_time_seconds)), "{days}:{hours}:{minutes}")

    print(f'=============>Tiempo transcurrido para recuperar archivos de tipo {tipo}: {elapsed_time_str} <=============\n') # Mostrar el tiempo transcurrido

    return elapsed_time_seconds  # Retornar el tiempo transcurrido en segundos

# Lista de tipos de archivo con sus respectivas firmas hexadecimales
def main():
    tipos_archivo = [
        # ("JPEG", "FFD8FFE0"),  # Archivo de imagen JPEG
        # ("PNG", "89504E470D0A1A0A"),  # Archivo de imagen PNG
        ("AI", "255044462D312E"),  # Archivo Adobe Illustrator
        ("EPS", "252150532D41646F6265"),  # Archivo Encapsulated PostScript
        ("INDD", "06054B50"),  # Archivo Adobe InDesign
        ("PSD", "38425053"),  # Archivo Adobe Photoshop
        ("PDF", "25504446"),  # Archivo Adobe PDF
        ("BMP", "424D"),  # Archivo de imagen BMP
        ("TIFF", "49492A00"),  # Archivo de imagen TIFF (Intel)
        ("TIFF", "4D4D002A"),  # Archivo de imagen TIFF (Motorola)
        ("FLA", "464C5601"),  # Archivo Adobe Flash FLA
        ("SWF", "435753"),  # Archivo Adobe Flash SWF
        ("F4V", "464432"),  # Archivo de video Adobe Flash F4V
        # ("GIF", "47494638"),  # Archivo de imagen GIF
        # ("MP3", "FFF8"),  # Archivo de audio MP3
        # ("MP4", "66747970"),  # Archivo de video MP4
        # ("JPEG2000", "0000000C6A502020"),  # Archivo de imagen JPEG2000
        # ("AVI", "52494646"),  # Archivo de video AVI
        # ("WAV", "52494646"),  # Archivo de audio WAV
        # ("FLAC", "664C6143"),  # Archivo de audio FLAC
        # ("MOV", "6D6F6F76"),  # Archivo de video QuickTime MOV
        # ("WMV", "3026B275"),  # Archivo de video Windows Media WMV
        # ("EXE", "4D5A"),  # Archivo ejecutable EXE
        # ("AIFF", "464F524D00"),  # Archivo de audio AIFF
        # ("ZIP", "504B0304"),  # Archivo comprimido ZIP
        # ("RAR", "526172211A0700"),  # Archivo comprimido RAR
        # ("7Z", "377ABCAF271C"),  # Archivo comprimido 7Z
        # ("TAR", "7573746172"),  # Archivo comprimido TAR
        # ("GZ", "1F8B0800"),  # Archivo comprimido GZ
        # ("XZ", "FD377A585A00"),  # Archivo comprimido XZ
        # ("TAR.GZ", "1F8B080000000000"),  # Archivo comprimido TAR.GZ
        # ("TAR.XZ", "FD377A585A00"),  # Archivo comprimido TAR.XZ
        # ("TAR.BZ2", "425A68"),  # Archivo comprimido TAR.BZ2
        # ("DOCX", "504B0304"),  # Archivo de documento Microsoft Word DOCX
        # ("XLSX", "504B0304"),  # Archivo de documento Microsoft Excel XLSX
        # ("PPTX", "504B0304"),  # Archivo de documento Microsoft PowerPoint PPTX
        # ("ODT", "504B0304"),  # Archivo de documento OpenDocument ODT
        # ("ODS", "504B0304"),  # Archivo de documento OpenDocument ODS
        # ("ODP", "504B0304"),  # Archivo de documento OpenDocument ODP
    ]

    # Recuperar archivos para cada tipo de archivo en la lista
    for tipo, firma_hex in tipos_archivo:
        ruta_salida = os.path.join(ruta_salida_base, tipo)  # Directorio de salida para los archivos recuperados
        os.makedirs(ruta_salida, exist_ok=True)  # Crear la carpeta si no existe
        elapsed_time = recover_files(drive, firma_hex, tipo, ruta_salida)  # Recuperar archivos y obtener el tiempo transcurrido
        total_time += elapsed_time  # Sumar el tiempo transcurrido al tiempo total
        print(f'=============>Todos los archivos de Tipo {tipo} han sido Recuperados<=============\n')

    total_time = timedelta(seconds=total_time) # Convertir el tiempo total a un objeto timedelta
    print(f'=============>Tiempo total transcurrido: {total_time} <=============\n')

# Ejecutar el script
if __name__ == "__main__":
    main()