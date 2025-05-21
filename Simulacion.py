import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

def simulate_bb84(n_bits):
    results = {
        "alice_bits": [],
        "alice_bases": [],
        "photons_sent": [],
        "bob_bases": [],
        "bob_bits": [],
        "bases_match": [],
        "use_bit": []
    }
    
    # Generación de bits y bases aleatorias para Alice
    results["alice_bits"] = np.random.randint(0, 2, n_bits).tolist()
    results["alice_bases"] = np.random.randint(0, 2, n_bits).tolist()
    
    # Calcula los fotones que envía Alice
    for i in range(n_bits):
        bit = results["alice_bits"][i]
        base = results["alice_bases"][i]
        
        if base == 0:
            photon = bit
        else:
            photon = 1 - bit
            
        results["photons_sent"].append(photon)
    
    # Bases aleatorias para Bob
    results["bob_bases"] = np.random.randint(0, 2, n_bits).tolist()
    
    # Bob mide los fotones
    for i in range(n_bits):
        photon = results["photons_sent"][i]
        bob_base = results["bob_bases"][i]
        alice_base = results["alice_bases"][i]
        
        # Si Bob usa la misma base que Alice, obtiene el bit correcto
        if bob_base == alice_base:
            bob_bit = results["alice_bits"][i]
        # Si las bases no coinciden, resultado aleatorio
        else:
            bob_bit = np.random.randint(0, 2)
                
        results["bob_bits"].append(bob_bit)
    
    # Comparación de bases
    for i in range(n_bits):
        # Verificar si las bases coinciden
        match = results["alice_bases"][i] == results["bob_bases"][i]
        results["bases_match"].append(match)
        
        # Si las bases coinciden, usar el bit para la clave
        results["use_bit"].append(match)
    
    # Clave secreta final
    secret_key = []
    for i in range(n_bits):
        if results["use_bit"][i]:
            secret_key.append(results["alice_bits"][i])
    
    results["secret_key"] = secret_key
        
    return results

def display_simulation(results):
    table_data = []
    for i in range(len(results["alice_bits"])):
        alice_base_symbol = "↕" if results["alice_bases"][i] == 0 else "↗"
        bob_base_symbol = "↕" if results["bob_bases"][i] == 0 else "↗"
        
        row = [
            i + 1,
            results["alice_bits"][i],
            alice_base_symbol,
            results["photons_sent"][i],
            bob_base_symbol,
            results["bob_bits"][i],
            "sí" if results["bases_match"][i] else "no",
            "sí" if results["use_bit"][i] else "no"
        ]
            
        table_data.append(row)
    
    headers = ["N°", "Bit de Alice", "Base de Alice", "Fotón enviado", "Base de Bob", "Bit recibido", "¿Bases coinciden?", "¿Usar bit?"]
    
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    print(f"\nTotal de bits transmitidos: {len(results['alice_bits'])}")
    print(f"Bits útiles para la clave: {len(results['secret_key'])}")
    print(f"Porcentaje útil: {len(results['secret_key'])/len(results['alice_bits'])*100:.2f}%")    
    print(f"\nClave secreta: {' '.join(map(str, results['secret_key']))}")

def visualize_bases(results):
    n_bits = len(results["alice_bits"])    
    alice_bases_visual = ["Recta (↕)" if b == 0 else "Diagonal (↗)" for b in results["alice_bases"]]
    bob_bases_visual = ["Recta (↕)" if b == 0 else "Diagonal (↗)" for b in results["bob_bases"]]
    
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.bar(range(1, n_bits + 1), [0.5] * n_bits, color=['blue' if b == 0 else 'red' for b in results["alice_bases"]])
    plt.yticks([])
    plt.title("Bases utilizadas por Alice")
    plt.xlabel("Número de bit")
    plt.xticks(range(1, n_bits + 1))
    plt.legend(["Recta (↕)", "Diagonal (↗)"], loc='upper right')
    
    plt.subplot(2, 1, 2)
    plt.bar(range(1, n_bits + 1), [0.5] * n_bits, color=['blue' if b == 0 else 'red' for b in results["bob_bases"]])
    plt.yticks([])
    plt.title("Bases utilizadas por Bob")
    plt.xlabel("Número de bit")
    plt.xticks(range(1, n_bits + 1))
    plt.legend(["Recta (↕)", "Diagonal (↗)"], loc='upper right')
    
    plt.tight_layout()
    plt.show()

def main():
    print("Simulación del Protocolo BB84")
    
    while True:
        try:
            n_bits = int(input("\nIngrese el número de bits a transmitir: "))
            results = simulate_bb84(n_bits)
            display_simulation(results)

            try:
                visualize_bases(results)
            except Exception as e:
                print(f"No se pudo mostrar la visualización: {e}")
            
            repet = input("\n¿Desea realizar otra simulación? (s/n): ").lower()
            if repet != 's':
                break
                
        except Exception as e:
            print(f"Error en la simulación: {e}")
            break

    print("\nFin de la simulación.")
    
if __name__ == "__main__":
    main()
