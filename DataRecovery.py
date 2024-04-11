"""
ESPAÑOL

Mouse Data Recovery es un programa diseñado para recuperar archivos perdidos o eliminados accidentalmente de discos duros o memorias USB. 
Utiliza firmas hexadecimales específicas para identificar archivos de diferentes tipos y los recupera a partir de bloques de lectura del dispositivo de almacenamiento.

Para utilizar el programa, simplemente especifique el disco duro o memoria USB a escanear y el directorio de salida para los archivos recuperados. 
El programa buscará archivos de diversos tipos, como imágenes, documentos y archivos de video, entre otros, y los recuperará en la carpeta especificada.

¡Recupera tus archivos perdidos con facilidad utilizando Mouse Data Recovery!

ENGLISH

Mouse Data Recovery is a program designed to recover lost or accidentally deleted files from hard drives or USB sticks.
It uses specific hexadecimal signatures to identify files of different types and recovers them from read blocks on the storage device.

To use the program, simply specify the hard drive or USB stick to scan and the output directory for the recovered files.
The program will search for files of various types, such as images, documents, and video files, among others, and recover them to the specified folder.

Recover your lost files with ease using Mouse Data Recovery!
"""


import os # Módulo para interactuar con el sistema operativo / Module to interact with the operating system
import time # Módulo para trabajar con fechas y horas / Module to work with dates and times
from datetime import timedelta # Clase para representar un intervalo de tiempo / Class to represent a time interval
import hashlib # Módulo para calcular resúmenes de mensajes y códigos hash / Module to calculate message digests and hash codes

# La cantidad de bytes a leer depende de la capacidad del disco duro o memoria USB / The amount of bytes to read depends on the capacity of the hard drive or USB stick
# Tambien depende de cuanta ram tenga el sistema operativo / It also depends on how much RAM the operating system has
# Gama Baja 512 bytes y 2048 bytes / Low Range 512 bytes to 2048 bytes
# Gama Media 2048 bytes a 8192 bytes / Medium Range 2048 bytes to 8192 bytes
# Gama Alta 8192 bytes y 65536 bytes o más / High Range 8192 bytes to 65536 bytes or more
size = 16777216  # Tamaño del bloque de lectura en bytes (16 MB) / Read block size in bytes (16 MB)

# Directorio a escanear en busca de archivos para recuperar / Directory to scan for files to recover
drive = "\\\\.\\D:" # Disco duro o memoria USB a escanear / Hard drive or USB stick to scan
ruta_salida_base = "D:\\recuperados" # Directorio de salida para los archivos recuperados / Output directory for the recovered files
total_time = 0  # Variable para almacenar el tiempo total transcurrido / Variable to store the total elapsed time

# Función para formatear un timedelta como una cadena / Function to format a timedelta as a string
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days} # Crear un diccionario con los días transcurridos / Create a dictionary with the elapsed days
    d["hours"], rem = divmod(tdelta.seconds, 3600) # Calcular las horas transcurridas / Calculate the elapsed hours
    d["minutes"], d["seconds"] = divmod(rem, 60) # Calcular los minutos y segundos transcurridos / Calculate the elapsed minutes and seconds
    return fmt.format(**d) # Formatear la cadena con los valores del diccionario / Format the string with the dictionary values

# Calcular el hash MD5 de un archivo / Calculate the MD5 hash of a file
def generate_file_hash(file_path):
    hash_md5 = hashlib.md5() # Crear un objeto hash MD5 / Create an MD5 hash object
    with open(file_path, "rb") as file: # Leer el archivo en modo binario / Read the file in binary mode
        # Leer el archivo en bloques del valor de la variable size / Read the file in blocks of the value of the size variable
        for chunk in iter(lambda: file.read(size), b""):
            hash_md5.update(chunk) # Actualizar el hash MD5 con el bloque actual / Update the MD5 hash with the current block
    return hash_md5.hexdigest() # Retornar el hash MD5 en formato hexadecimal / Return the MD5 hash in hexadecimal format

# Recuperar archivos de un disco duro o memoria USB / Recover files from a hard drive or USB stick
def recover_files(drive, signature, tipo, output_dir):
    start_time = time.time()  # Capturar el tiempo de inicio / Capture the start time

    # Recuperar archivos de un disco duro o memoria USB / Recover files from a hard drive or USB stick
    try:
        # Leer el disco duro o memoria USB en modo binario / Read the hard drive or USB stick in binary mode
        with open(drive, "rb") as fileD:
            offs = 0 # Desplazamiento de lectura en el disco duro o memoria USB / Reading offset on the hard drive or USB stick
            rcvd = 0 # Contador de archivos recuperados / Recovered files counter
            recoveredPositions = {} # Diccionario para almacenar las posiciones de los archivos recuperados / Dictionary to store the positions of the recovered files

            # Leer el disco duro o memoria USB en bloques de 4096 bytes / Read the hard drive or USB stick in blocks of 4096 bytes
            while True:
                byte = fileD.read(size) # Leer un bloque de 4096 bytes / Read a block of 4096 bytes

                # Si no se lee ningún byte, salir del bucle / If no byte is read, exit the loop
                if not byte:
                    break

                found = byte.find(bytes.fromhex(signature)) # Buscar la firma hexadecimal en el bloque leído / Search for the hexadecimal signature in the read block

                # Si se encuentra la firma hexadecimal, recuperar el archivo / If the hexadecimal signature is found, recover the file
                if found >= 0:
                    elapsed_time_seconds = time.time() - start_time  # Calcular el tiempo transcurrido en segundos / Calculate the elapsed time in seconds

                    # Formatear el tiempo transcurrido en el formato deseado / Format the elapsed time in the desired format
                    elapsed_time_str = strfdelta(timedelta(seconds=int(elapsed_time_seconds)), "{days}:{hours}:{minutes}")

                    print(f'=============>Tiempo transcurrido: {elapsed_time_str} <=============\n') # Mostrar el tiempo transcurrido / Show the elapsed time

                    print(f'=============> Archivo encontrado en la ubicación: {str(hex(found+(size*offs)))} <=============') # Mostrar la ubicación del archivo encontrado / Show the location of the found file

                    # Verificar si la posición de recuperación ya está en el diccionario / Check if the recovery position is already in the dictionary
                    if offs not in recoveredPositions:
                        recoveredPositions[offs] = set()  # Usar un conjunto para almacenar hashes de archivos recuperados en esta posición / Use a set to store hashes of recovered files at this position

                    # Leer el archivo desde la firma hexadecimal encontrada / Read the file from the found hexadecimal signature
                    file_content = byte[found:] # Leer el archivo desde la firma hexadecimal encontrada / Read the file from the found hexadecimal signature
                    file_hash = hashlib.md5(file_content).hexdigest() # Calcular el hash MD5 del contenido del archivo / Calculate the MD5 hash of the file content

                    # Verificar si el hash del contenido del archivo ya está en los archivos recuperados en esta posición / Check if the hash of the file content is already in the recovered files at this position
                    if file_hash not in recoveredPositions[offs]:
                        file_path = os.path.join(output_dir, f'{rcvd}.{tipo.lower()}') # Crear la ruta del archivo recuperado / Create the path of the recovered file

                        # Escribir el archivo recuperado en la carpeta de salida / Write the recovered file to the output folder
                        with open(file_path, "wb") as fileN:
                            fileN.write(file_content) # Escribir el contenido del archivo recuperado / Write the content of the recovered file
                            recoveredPositions[offs].add(file_hash)  # Agregar el hash del archivo recuperado / Add the hash of the recovered file
                            
                            # Leer el resto del archivo desde el bloque actual / Read the rest of the file from the current block
                            while True:
                                byte = fileD.read(size) # Leer un bloque de size bytes / Read a block of size bytes
                                bfind = byte.find(bytes.fromhex(signature)) # Buscar la firma hexadecimal en el bloque leído / Search for the hexadecimal signature in the read block

                                # Si se encuentra la firma hexadecimal, escribir el archivo recuperado / If the hexadecimal signature is found, write the recovered file
                                if bfind >= 0:
                                    fileN.write(byte[:bfind+len(bytes.fromhex(signature))]) # Escribir el archivo recuperado / Write the recovered file
                                    offs += byte[:bfind+len(bytes.fromhex(signature))].count(b'\n') # Actualizar el desplazamiento / Update the offset
                                    print(f'=============> Escribiendo archivo en la ubicación: {rcvd}.{tipo.lower()} <=============\n') # Mostrar la ubicación del archivo recuperado / Show the location of the recovered file
                                    break
                                else:
                                    fileN.write(byte) # Escribir el bloque leído en el archivo recuperado / Write the read block to the recovered file
                        rcvd += 1 # Incrementar el contador de archivos recuperados / Increment the recovered files counter
                    else:
                        offs += byte.count(b'\n') # Actualizar el desplazamiento / Update the offset

                offs += 1 # Incrementar el desplazamiento / Increment the offset

    except Exception as e:
        print(f"Error: {e}\n") # Mostrar mensaje de error / Show error message

    end_time = time.time()  # Capturar el tiempo de finalización / Capture the end time
    elapsed_time_seconds = end_time - start_time  # Calcular el tiempo transcurrido en segundos / Calculate the elapsed time in seconds

    # Formatear el tiempo transcurrido en el formato deseado / Format the elapsed time in the desired format
    elapsed_time_str = strfdelta(timedelta(seconds=int(elapsed_time_seconds)), "{days}:{hours}:{minutes}")

    print(f'=============>Tiempo transcurrido para recuperar archivos de tipo {tipo}: {elapsed_time_str} <=============\n') # Mostrar el tiempo transcurrido / Show the elapsed time

    return elapsed_time_seconds  # Retornar el tiempo transcurrido en segundos / Return the elapsed time in seconds

# Lista de tipos de archivo con sus respectivas firmas hexadecimales / List of file types with their respective hexadecimal signatures
def main():
    tipos_archivo = [
        # ("JPEG", "FFD8FFE0"),             # Archivo de imagen JPEG / JPEG image file
        # ("PNG", "89504E470D0A1A0A"),      # Archivo de imagen PNG / PNG image file
        ("AI", "255044462D312E"),           # Archivo Adobe Illustrator / Adobe Illustrator file
        ("EPS", "252150532D41646F6265"),    # Archivo Encapsulated PostScript / Encapsulated PostScript file
        ("INDD", "06054B50"),               # Archivo Adobe InDesign / Adobe InDesign file
        ("PSD", "38425053"),                # Archivo Adobe Photoshop / Adobe Photoshop file
        ("PDF", "25504446"),                # Archivo Adobe PDF / Adobe PDF file
        ("BMP", "424D"),                    # Archivo de imagen BMP / BMP image file
        ("TIFF", "49492A00"),               # Archivo de imagen TIFF (Intel) / TIFF image file (Intel)
        ("TIFF", "4D4D002A"),               # Archivo de imagen TIFF (Motorola) / TIFF image file (Motorola)
        ("FLA", "464C5601"),                # Archivo Adobe Flash FLA / Adobe Flash FLA file
        ("SWF", "435753"),                  # Archivo Adobe Flash SWF / Adobe Flash SWF file
        ("F4V", "464432"),                  # Archivo de video Adobe Flash F4V / Adobe Flash F4V video file
        # ("GIF", "47494638"),              # Archivo de imagen GIF / GIF image file
        # ("MP3", "FFF8"),                  # Archivo de audio MP3 / MP3 audio file
        # ("MP4", "66747970"),              # Archivo de video MP4 / MP4 video file
        # ("JPEG2000", "0000000C6A502020"), # Archivo de imagen JPEG2000 / JPEG2000 image file
        # ("AVI", "52494646"),              # Archivo de video AVI / AVI video file
        # ("WAV", "52494646"),              # Archivo de audio WAV / WAV audio file
        # ("FLAC", "664C6143"),             # Archivo de audio FLAC / FLAC audio file
        # ("MOV", "6D6F6F76"),              # Archivo de video QuickTime MOV / QuickTime MOV video file
        # ("WMV", "3026B275"),              # Archivo de video Windows Media WMV / Windows Media WMV video file
        # ("EXE", "4D5A"),                  # Archivo ejecutable EXE / EXE executable file
        # ("AIFF", "464F524D00"),           # Archivo de audio AIFF / AIFF audio file
        # ("ZIP", "504B0304"),              # Archivo comprimido ZIP / ZIP compressed file
        # ("RAR", "526172211A0700"),        # Archivo comprimido RAR / RAR compressed file
        # ("7Z", "377ABCAF271C"),           # Archivo comprimido 7Z / 7Z compressed file
        # ("TAR", "7573746172"),            # Archivo comprimido TAR / TAR compressed file
        # ("GZ", "1F8B0800"),               # Archivo comprimido GZ / GZ compressed file
        # ("XZ", "FD377A585A00"),           # Archivo comprimido XZ / XZ compressed file
        # ("TAR.GZ", "1F8B080000000000"),   # Archivo comprimido TAR.GZ / TAR.GZ compressed file
        # ("TAR.XZ", "FD377A585A00"),       # Archivo comprimido TAR.XZ / TAR.XZ compressed file
        # ("TAR.BZ2", "425A68"),            # Archivo comprimido TAR.BZ2 / TAR.BZ2 compressed file
        # ("DOCX", "504B0304"),             # Archivo de documento Microsoft Word DOCX / Microsoft Word DOCX document file
        # ("XLSX", "504B0304"),             # Archivo de documento Microsoft Excel XLSX / Microsoft Excel XLSX document file
        # ("PPTX", "504B0304"),             # Archivo de documento Microsoft PowerPoint PPTX / Microsoft PowerPoint PPTX document file
        # ("ODT", "504B0304"),              # Archivo de documento OpenDocument ODT / OpenDocument ODT document file
        # ("ODS", "504B0304"),              # Archivo de documento OpenDocument ODS / OpenDocument ODS document file
        # ("ODP", "504B0304"),              # Archivo de documento OpenDocument ODP / OpenDocument ODP document file
    ]

    # Recuperar archivos para cada tipo de archivo en la lista / Recover files for each file type in the list
    for tipo, firma_hex in tipos_archivo:
        ruta_salida = os.path.join(ruta_salida_base, tipo)  # Directorio de salida para los archivos recuperados / Output directory for the recovered files
        os.makedirs(ruta_salida, exist_ok=True)  # Crear la carpeta si no existe / Create the folder if it does not exist
        elapsed_time = recover_files(drive, firma_hex, tipo, ruta_salida)  # Recuperar archivos y obtener el tiempo transcurrido / Recover files and get the elapsed time
        total_time += elapsed_time  # Sumar el tiempo transcurrido al tiempo total / Add the elapsed time to the total time
        print(f'=============>Todos los archivos de Tipo {tipo} han sido Recuperados<=============\n')

    total_time = timedelta(seconds=total_time) # Convertir el tiempo total a un objeto timedelta / Convert the total time to a timedelta object
    print(f'=============>Tiempo total transcurrido: {total_time} <=============\n')

# Ejecutar el script principal / Run the main script
if __name__ == "__main__":
    main()