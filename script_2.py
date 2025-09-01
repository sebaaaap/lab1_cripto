import os
import sys
import time
import random
from scapy.all import ICMP, IP, send, Raw

def cifrado_cesar(texto, corrimiento):
   
    resultado = ""
    
    if len(texto) == 0:
        return "b"
    
    # Cifrar todos los caracteres excepto el último
    for i in range(len(texto) - 1):
        char = texto[i]
        if char.isalpha():
            ascii_base = ord('A') if char.isupper() else ord('a')
            nuevo_char = chr((ord(char) - ascii_base + corrimiento) % 26 + ascii_base)
            resultado += nuevo_char
        else:
            resultado += char
    
    # Forzar el último carácter a ser 'b'
    resultado += 'b'
    
    return resultado

def enviar_ping_stealth(mensaje_cifrado, destino="8.8.8.8"):
    """
    Envía cada carácter del mensaje cifrado en paquetes ICMP de 48 bytes
    (como un ping normal de Linux/Windows)
    """
    print("Enviando paquetes ICMP stealth de 48 bytes...")
    print(f"Mensaje cifrado: {mensaje_cifrado}")
    print("-" * 50)
    
    # Patrón típico de datos de ping (48 bytes)
    # Los primeros 8 bytes son timestamp, el resto son datos aleatorios
    patron_ping = bytes([0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
    
    for i, caracter in enumerate(mensaje_cifrado):
        # Crear payload de 48 bytes como un ping real
        # Byte 0-7: timestamp falso (como ping real)
        # Byte 8: nuestro carácter secreto
        # Bytes 9-47: datos aleatorios (como ping real)
        
        payload = patron_ping + bytes([ord(caracter)]) + bytes([random.randint(0, 255) for _ in range(39)])
        
        # Crear paquete ICMP
        paquete = IP(dst=destino)/ICMP()/Raw(load=payload)
        
        # Enviar paquete
        send(paquete, verbose=False)
        
        print(f"Paquete {i+1}: enviado carácter '{caracter}' oculto en payload de 48 bytes")
        print(f"  Payload: {payload[:12].hex()}... (total: 48 bytes)")
        time.sleep(1)  # Pausa realista entre pings
    
    print("-" * 50)
    print("Todos los paquetes enviados exitosamente")
    print(f"Último carácter transmitido: '{mensaje_cifrado[-1]}'")
    print("Tamaño de cada paquete: 48 bytes (como ping real)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: sudo python3 pingv4.py \"mensaje\" corrimiento")
        print("Ejemplo: sudo python3 pingv4.py \"criptografía y seguridad en redes\" 9")
        sys.exit(1)
    
    mensaje = sys.argv[1]
    corrimiento = int(sys.argv[2])
    
    # Cifrar el mensaje
    mensaje_cifrado = cifrado_cesar(mensaje, corrimiento)
    
    # Enviar paquetes
    enviar_ping_stealth(mensaje_cifrado)