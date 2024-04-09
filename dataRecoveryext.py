import os

def recover_files(drive, signature, output_dir):
    fileD = open(drive, "rb")
    size = 512
    byte = fileD.read(size)
    offs = 0
    drec = False
    rcvd = 0
    while byte:
        found = byte.find(bytes.fromhex(signature))
        if found >= 0:
            drec = True
            print(f'=============> Archivo encontrado en la ubicación: {str(hex(found+(size*offs)))} <=============')
            fileN = open(os.path.join(output_dir, f'{rcvd}.{signature.lower()}'), "wb")
            fileN.write(byte[found:])
            while drec:
                byte = fileD.read(size)
                bfind = byte.find(bytes.fromhex(''.join(signature.split())))
                if bfind >= 0:
                    fileN.write(byte[:bfind+len(bytes.fromhex(''.join(signature.split())))])
                    fileD.seek((offs+1)*size)
                    print(f'=============> Escribiendo archivo en la ubicación: {rcvd}.{signature.lower()} <=============\n')
                    drec = False
                    rcvd += 1
                    fileN.close()
                else: 
                    fileN.write(byte)
        byte = fileD.read(size)
        offs += 1
    fileD.close()

# Lista de tipos de archivo con sus respectivas firmas hexadecimales
tipos_archivo = [
    ("AI", "255044462D312E"),
    ("EPS", "252150532D41646F6265"),
    ("INDD", "06054B50"),
    ("PSD", "38425053"),
    ("PDF", "25504446"),
    ("JPEG", "FFD8FFE0"),
    ("PNG", "89504E470D0A1A0A"),
    ("GIF", "47494638"),
    ("MP3", "FFF8"),
    ("MP4", "66747970"),
    ("JPEG2000", "0000000C6A502020"),
    ("BMP", "424D"),
    ("TIFF", "49492A00"),
    ("TIFF", "4D4D002A"),
    ("AVI", "52494646"),
    ("WAV", "52494646"),
    ("FLAC", "664C6143"),
    ("MOV", "6D6F6F76"),
    ("WMV", "3026B275"),
    ("EXE", "4D5A"),
    ("PDF", "25504446"),
    ("AIFF", "464F524D00"),
    ("INDD", "494E4444"),
    ("FLA", "464C5601"),
    ("SWF", "435753"),
    ("F4V", "464432"),
    ("IND", "494E44"),
    ("ZIP", "504B0304"),
    ("RAR", "526172211A0700"),
    ("7Z", "377ABCAF271C"),
    ("TAR", "7573746172"),
    ("GZ", "1F8B0800"),
    ("XZ", "FD377A585A00"),
    ("TAR.GZ", "1F8B080000000000"),
    ("TAR.XZ", "FD377A585A00"),
    ("TAR.BZ2", "425A68"),
    ("DOCX", "504B0304"),
    ("XLSX", "504B0304"),
    ("PPTX", "504B0304"),
    ("ODT", "504B0304"),
    ("ODS", "504B0304"),
    ("ODP", "504B0304"),
]

# Directorio a escanear en busca de archivos para recuperar
drive = "\\\\.\\D:"
ruta_salida_base = "D:\\recuperados"

# Recuperar archivos para cada tipo de archivo en la lista
for tipo, firma_hex in tipos_archivo:
    ruta_salida = os.path.join(ruta_salida_base, tipo)
    os.makedirs(ruta_salida, exist_ok=True)  # Crear la carpeta si no existe
    recover_files(drive, firma_hex, ruta_salida)
