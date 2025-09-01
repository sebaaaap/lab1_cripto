import sys

def cifrado_cesar(texto, corrimiento):
    texto_cifrado = ""
    for caracter in texto:
        if caracter.isalpha():
            base = ord('A') if caracter.isupper() else ord('a')
            nuevo_caracter = chr((ord(caracter) - base + corrimiento) % 26 + base)
            texto_cifrado += nuevo_caracter
        else:
            texto_cifrado += caracter
    return texto_cifrado

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 cesar.py 'texto' corrimiento")
        sys.exit(1)
    
    texto = sys.argv[1]
    try:
        corrimiento = int(sys.argv[2])
    except ValueError:
        print("Error: El corrimiento debe ser un número entero.")
        sys.exit(1)
    
    texto_cifrado = cifrado_cesar(texto, corrimiento)
    print(texto_cifrado)

if __name__ == "__main__":
    main()