import subprocess
import os

VM_PATH = "C:\\Users\\Julien\\VirtualBox VMs"
ISO_PATH = "C:\\Users\\Julien\\Documents\\I4\\ubuntu-24.04.1-live-server-amd64.iso"

def main_menu():
    menu_options = {
        '1': deploy_from_template,
        '2': create_vm_from_scratch,
        '3': export_vm_to_ova,
        '4': delete_vm,
        '5': create_vm_from_ova,
        '6': list_vms,
        '7': exit_program
    }
    
    while True:
        print("\n[MENU PRINCIPAL] - Choisissez une option :")
        print("1. Déployer à partir d'un modèle")
        print("2. Créer une VM à partir de zéro")
        print("3. Exporter la VM en OVA")
        print("4. Supprimer la VM")
        print("5. Créer une VM à partir d'un modèle OVA")
        print("6. Lister les VMs")
        print("7. Quitter")
        
        choice = input("Entrez votre choix : ").strip()
        action = menu_options.get(choice, invalid_choice)
        action()

def invalid_choice():
    print("[ERREUR] - Choix invalide. Réessayez.")

def exit_program():
    print("Quitter...")
    exit()

def list_vms():
    try:
        vms = os.listdir(VM_PATH)
        if vms:
            print("[LISTE] - VMs disponibles :")
            for vm in vms:
                print(f"- {vm}")
        else:
            print("[LISTE] - Aucune VM trouvée.")
    except FileNotFoundError:
        print("[ERREUR] - Répertoire VM introuvable.")

def deploy_from_template():
    list_vms()
    template_name = input("[DÉPLOIEMENT] - Entrez le nom du modèle : ").strip()
    clone_name = input("[DÉPLOIEMENT] - Entrez le nom du clone : ").strip()
    try:
        subprocess.run([
            "VBoxManage", "clonevm", template_name, "--name", clone_name, "--register"
        ], check=True)
        print(f"[DÉPLOIEMENT] - Clone '{clone_name}' créé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] - Échec du clonage de la VM : {e}")

def create_vm_from_scratch():
    vm_name = input("[CRÉATION] - Entrez le nom de la VM : ").strip()
    memory_size = input("[CRÉATION] - Entrez la taille de la mémoire (MB) : ").strip()
    disk_size = input("[CRÉATION] - Entrez la taille du disque (MB) : ").strip()
    
    if not (memory_size.isdigit() and disk_size.isdigit()):
        print("[ERREUR] - La taille de la mémoire et du disque doit être un nombre.")
        return

    try:
        vm_dir = os.path.join(VM_PATH, vm_name)
        subprocess.run([
            "VBoxManage", "createvm", "--name", vm_name, "--ostype", "Ubuntu_64", "--register", "--basefolder", VM_PATH
        ], check=True)
        subprocess.run([
            "VBoxManage", "modifyvm", vm_name, "--memory", memory_size, "--vram", "9"
        ], check=True)
        subprocess.run([
            "VBoxManage", "createhd", "--filename", os.path.join(vm_dir, f"{vm_name}.vdi"), "--size", disk_size
        ], check=True)
        subprocess.run([
            "VBoxManage", "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--controller", "IntelAhci"
        ], check=True)
        subprocess.run([
            "VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", os.path.join(vm_dir, f"{vm_name}.vdi")
        ], check=True)
        subprocess.run([
            "VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", ISO_PATH
        ], check=True)
        print(f"[CRÉATION] - VM '{vm_name}' créée avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] - Échec de la création de la VM : {e}")

def create_vm_from_ova():
    list_vms()
    ova_file = input("[IMPORT] - Entrez le chemin du fichier OVA : ").strip()
    if not os.path.isabs(ova_file):
        ova_file = os.path.join(VM_PATH, ova_file)
    try:
        subprocess.run([
            "VBoxManage", "import", ova_file
        ], check=True)
        print(f"[IMPORT] - VM importée depuis '{ova_file}' avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] - Échec de l'importation de la VM : {e}")

def export_vm_to_ova():
    list_vms()
    vm_name = input("[EXPORT] - Entrez le nom de la VM à exporter : ").strip()
    export_path = os.path.join(VM_PATH, f"{vm_name}.ova")
    try:
        subprocess.run([
            "VBoxManage", "export", vm_name, "--output", export_path
        ], check=True)
        print(f"[EXPORT] - VM '{vm_name}' exportée vers '{export_path}' avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] - Échec de l'exportation de la VM : {e}")

def delete_vm():
    list_vms()
    vm_name = input("[SUPPRESSION] - Entrez le nom de la VM ou le fichier OVA à supprimer : ").strip()
    try:
        result = subprocess.run([
            "VBoxManage", "list", "vms"
        ], capture_output=True, text=True, check=True)
        vms = [line.split('"')[1] for line in result.stdout.splitlines()]
        files = os.listdir(VM_PATH)
        
        if vm_name in vms:
            subprocess.run([
                "VBoxManage", "unregistervm", vm_name, "--delete"
            ], check=True)
            print(f"[SUPPRESSION] - VM '{vm_name}' supprimée avec succès.")
        elif vm_name in files and vm_name.lower().endswith('.ova'):
            os.remove(os.path.join(VM_PATH, vm_name))
            print(f"[SUPPRESSION] - Fichier OVA '{vm_name}' supprimé avec succès.")
        else:
            print(f"[ERREUR] - '{vm_name}' introuvable.")
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] - Échec de la suppression : {e}")

if __name__ == "__main__":
    main_menu()
