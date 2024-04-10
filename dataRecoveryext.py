import os # Módulo para interactuar con el sistema operativo
import time # Módulo para trabajar con fechas y horas
from datetime import timedelta # Clase para representar un intervalo de tiempo

# Recuperar archivos de un disco duro o memoria USB
def recover_files(drive, signature, tipo, output_dir):
    start_time = time.time()  # Capturar el tiempo de inicio

    # Recuperar archivos de un disco duro o memoria USB
    try:
        # Leer el disco duro o memoria USB
        with open(drive, "rb") as fileD:
            size = 4096 # Tamaño de bloque/buffer a leer
            offs = 0 # Desplazamiento de bytes
            rcvd = 0 # Contador de archivos recuperados
            recoveredPositions = set()  # Almacenar posiciones de archivos recuperados para evitar duplicados

            # Leer el disco duro o memoria USB en bloques de tamaño 'size'
            while True:
                byte = fileD.read(size) # Leer un bloque de tamaño 'size'
                
                # Si no hay más bloques por leer, salir del bucle
                if not byte:
                    break

                # Buscar la firma hexadecimal en el bloque leído
                found = byte.find(bytes.fromhex(signature))

                # Si se encuentra la firma hexadecimal en el bloque leído
                if found >= 0:
                    elapsed_time = timedelta(seconds=time.time() - start_time)  # Calcular el tiempo transcurrido
                    print(f'=============>Tiempo transcurrido: {elapsed_time} <=============\n')  # Mostrar el tiempo transcurrido
                    print(f'=============> Archivo encontrado en la ubicación: {str(hex(found+(size*offs)))} <=============') # Mostrar la ubicación del archivo encontrado

                    # Verificar si ya se ha recuperado un archivo en esta posición
                    if offs not in recoveredPositions:
                        # Crear el archivo recuperado
                        with open(os.path.join(output_dir, f'{rcvd}.{tipo.lower()}'), "wb") as fileN:
                            fileN.write(byte[found:]) # Escribir el bloque leído desde la firma hexadecimal encontrada
                            recoveredPositions.add(offs) # Almacenar la posición del archivo recuperado

                            # Leer el disco duro o memoria USB en bloques de tamaño 'size'
                            while True:
                                byte = fileD.read(size) # Leer un bloque de tamaño 'size'
                                bfind = byte.find(bytes.fromhex(signature)) # Buscar la firma hexadecimal en el bloque leído

                                # Si se encuentra la firma hexadecimal en el bloque leído
                                if bfind >= 0:
                                    fileN.write(byte[:bfind+len(bytes.fromhex(signature))]) # Escribir el bloque leído desde la firma hexadecimal encontrada
                                    offs += byte[:bfind+len(bytes.fromhex(signature))].count(b'\n') # Actualizar el desplazamiento
                                    print(f'=============> Escribiendo archivo en la ubicación: {rcvd}.{tipo.lower()} <=============\n') # Mostrar la ubicación del archivo recuperado
                                    recoveredPositions.add(offs) # Almacenar la posición del archivo recuperado
                                    rcvd += 1 # Actualizar el contador de archivos recuperados
                                    break
                                else:
                                    fileN.write(byte) # Escribir el bloque leído
                    else:
                        # Si ya se recuperó un archivo en esta posición, avanzar el desplazamiento
                        offs += byte.count(b'\n')

                offs += 1 # Actualizar el desplazamiento

    except Exception as e:
        print(f"Error: {e}\n") # Mostrar mensaje de error

    end_time = time.time()  # Capturar el tiempo de finalización
    elapsed_time = timedelta(seconds=end_time - start_time)  # Calcular el tiempo transcurrido
    print(f'=============>Tiempo transcurrido para recuperar archivos de tipo {tipo}: {elapsed_time} <=============\n')
    return elapsed_time.total_seconds()  # Retornar el tiempo transcurrido en segundos

# Lista de tipos de archivo con sus respectivas firmas hexadecimales
def main():
    tipos_archivo = [
        ("PNG", "89504E470D0A1A0A"),  # Archivo de imagen PNG
        ("JPEG", "FFD8FFE0"),  # Archivo de imagen JPEG
        ("AI", "255044462D312E"),  # Archivo Adobe Illustrator
        ("EPS", "252150532D41646F6265"),  # Archivo Encapsulated PostScript
        ("INDD", "06054B50"),  # Archivo Adobe InDesign
        ("PSD", "38425053"),  # Archivo Adobe Photoshop
        ("PDF", "25504446"),  # Archivo Adobe PDF
        ("BMP", "424D"),  # Archivo de imagen BMP
        ("TIFF", "49492A00"),  # Archivo de imagen TIFF (Intel)
        ("TIFF", "4D4D002A"),  # Archivo de imagen TIFF (Motorola)
        ("PDF", "25504446"),  # Archivo Adobe PDF (repetido, parece ser un error en la lista original)
        ("INDD", "494E4444"),  # Archivo Adobe InDesign (repetido, parece ser un error en la lista original)
        ("FLA", "464C5601"),  # Archivo Adobe Flash FLA
        ("SWF", "435753"),  # Archivo Adobe Flash SWF
        ("F4V", "464432"),  # Archivo de video Adobe Flash F4V
        ("IND", "494E44"),  # Archivo Adobe InDesign (repetido, parece ser un error en la lista original)
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

    # Directorio a escanear en busca de archivos para recuperar
    drive = "\\\\.\\D:" # Disco duro o memoria USB
    ruta_salida_base = "D:\\recuperados" # Directorio de salida para los archivos recuperados
    total_time = 0  # Variable para almacenar el tiempo total transcurrido

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