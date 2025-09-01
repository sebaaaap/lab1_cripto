from scapy.all import rdpcap, Raw, ICMP
import requests
import io

# Descargar y analizar tu captura
url = "https://github.com/sebaaaap/lab1_cripto/raw/main/soy.pcapng"
response = requests.get(url)
pcap_data = io.BytesIO(response.content)
paquetes = rdpcap(pcap_data)

print("🔍 Analizando TU captura pcapng...")
print("=" * 50)

caracteres = []
ultimo_caracter = None
ultimo_timestamp = None

for i, paquete in enumerate(paquetes):
    if paquete.haslayer(ICMP) and paquete.haslayer(Raw):
        payload = bytes(paquete[Raw].load)
        
        if len(payload) >= 9:
            caracter = chr(payload[8])
            timestamp = paquete.time
            
            # FILTRAR DUPLICADOS: Solo agregar si es diferente al anterior
            # o si ha pasado más de 0.1 segundos (evitar duplicados consecutivos)
            if (caracter != ultimo_caracter or 
                (ultimo_timestamp and timestamp - ultimo_timestamp > 0.1)):
                
                caracteres.append(caracter)
                print(f"Paquete {i+1}: '{caracter}' (timestamp: {timestamp})")
            
            ultimo_caracter = caracter
            ultimo_timestamp = timestamp

mensaje_cifrado = ''.join(caracteres)
print(f"\n🎯 MENSAJE CIFRADO CORREGIDO: {mensaje_cifrado}")
print(f"📏 Longitud: {len(mensaje_cifrado)} caracteres")

# Ahora probamos descifrado con corrimiento 3
print("\n🔓 DESCIFRANDO con corrimiento 3:")
mensaje_descifrado = ""
for char in mensaje_cifrado:
    if char.isalpha():
        ascii_base = ord('a') if char.islower() else ord('A')
        nuevo_char = chr((ord(char) - ascii_base - 3) % 26 + ascii_base)
        mensaje_descifrado += nuevo_char
    else:
        mensaje_descifrado += char

print(f"📝 Mensaje descifrado: {mensaje_descifrado}")