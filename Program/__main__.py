import importlib

def main():
    print("Choisissez une option :")
    print("1 - Caustic")
    print("2 - Newlagrange")
    print("3 - Neweulerian")
   
   
    choix = input("Entrez votre choix (1, 2,3) : ")

    # Mapping des choix aux modules
    choix_modules = {
        "1": "caustic",
        "2": "Newlagrange",
        "3": "Neweulerian",
    }

    if choix in choix_modules:
        try:
            # Import dynamique du module choisi
            module = importlib.import_module(choix_modules[choix])
            # Appel de la fonction `main` du module
            module.main()
        except ImportError:
            print(f"Erreur : Impossible de charger le module {choix_modules[choix]}")
        except AttributeError:
            print(f"Erreur : Le module {choix_modules[choix]} ne contient pas de fonction main()")
    else:
        print("Choix invalide. Veuillez entrer 1 ou 2")

if __name__ == "__main__":
    main()


