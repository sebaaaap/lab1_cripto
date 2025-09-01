from scapy.all import rdpcap, Raw, ICMP

def descifrar_cesar(mensaje_cifrado, corrimiento):
    """Descifra mensaje usando César"""
    resultado = ""
    for char in mensaje_cifrado:
        if char.isalpha():
            ascii_base = ord('a') if char.islower() else ord('A')
            nuevo_char = chr((ord(char) - ascii_base - corrimiento) % 26 + ascii_base)
            resultado += nuevo_char
        else:
            resultado += char
    return resultado

# Leer captura y procesar
paquetes = rdpcap("holasoyelseby3.pcapng")
caracteres = []
ultimo_caracter = None

for paquete in paquetes:
    if paquete.haslayer(ICMP) and paquete.haslayer(Raw):
        payload = bytes(paquete[Raw].load)
        if len(payload) >= 9:
            caracter = chr(payload[8])
            # Filtrar duplicados consecutivos
            if caracter != ultimo_caracter:
                caracteres.append(caracter)
            ultimo_caracter = caracter

mensaje_cifrado = ''.join(caracteres)
print(f"Mensaje cifrado: {mensaje_cifrado}")

# Probar todos los corrimientos
print("\n🔓 PROBANDO TODOS LOS CORRIMIENTOS:")
print("=" * 50)

for corrimiento in range(1, 26):
    descifrado = descifrar_cesar(mensaje_cifrado, corrimiento)
    if "hola" in descifrado and "soy" in descifrado:
        # MENSAJE CORRECTO EN VERDE COMPLETO
        print(f"\033[92m Corrimiento {corrimiento:2d}: {descifrado}\033[0m")
    else:
        print(f"   Corrimiento {corrimiento:2d}: {descifrado}")

