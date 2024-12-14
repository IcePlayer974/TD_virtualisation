import subprocess
import os

VM_PATH = "C:\\Users\\Julien\\VirtualBox VMs"

def main_menu():
    while True:
        print("[MAIN MENU] - Choose an option:")
        print("1. Deploy from Template")
        print("2. Create VM from Scratch")
        print("3. Export VM to OVA")
        print("4. Delete VM")
        print("5. Create VM from OVA Template")
        print("6. List VMs")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            deploy_from_template()
        elif choice == '2':
            create_vm_from_scratch()
        elif choice == '3':
            export_vm_to_ova()
        elif choice == '4':
            delete_vm()
        elif choice == '5':
            create_vm_from_ova()
        elif choice == '6':
            list_vms()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

def list_vms():
    try:
        vms = os.listdir(VM_PATH)
        if vms:
            print("[LIST] - Available VMs:")
            for vm in vms:
                print(f"- {vm}")
        else:
            print("[LIST] - No VMs found.")
    except FileNotFoundError:
        print("[ERROR] - VM directory not found.")

def deploy_from_template():
    list_vms()
    template_name = input("[DEPLOY] - Enter the template name: ")
    clone_name = input("[DEPLOY] - Enter the clone name: ")
    try:
        subprocess.run(["VBoxManage", "clonevm", template_name, "--name", clone_name, "--register"], check=True)
        print(f"[DEPLOY] - Clone '{clone_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] - Failed to clone VM: {e}")

def create_vm_from_scratch():
    vm_name = input("[CREATE] - Enter the VM name: ")
    os_type = input("[CREATE] - Enter the OS type (e.g., Ubuntu_64) or press Enter to use default: ")
    if not os_type:
        os_type = "Ubuntu_64"
    memory_size = input("[CREATE] - Enter the memory size (MB): ")
    disk_size = input("[CREATE] - Enter the disk size (MB): ")

    try:
        vm_dir = os.path.join(VM_PATH, vm_name)
        subprocess.run(["VBoxManage", "createvm", "--name", vm_name, "--ostype", os_type, "--register", "--basefolder", VM_PATH], check=True)
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--memory", memory_size, "--vram", "9"], check=True)
        subprocess.run(["VBoxManage", "createhd", "--filename", os.path.join(vm_dir, f"{vm_name}.vdi"), "--size", disk_size], check=True)
        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--controller", "IntelAhci"], check=True)
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", os.path.join(vm_dir, f"{vm_name}.vdi")], check=True)
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", "C:\\Users\\Julien\\Downloads\\ubuntu-24.04.1-live-server-amd64.iso"], check=True)
        subprocess.run(["VBoxManage", "unattended install", vm_name, "--disable"], check=True)
        print(f"[CREATE] - VM '{vm_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] - Failed to create VM: {e}")

def create_vm_from_ova():
    list_vms()
    ova_file = input("[IMPORT] - Enter the path to the OVA file: ")
    if not os.path.isabs(ova_file):
        ova_file = os.path.join(VM_PATH, ova_file)
    try:
        subprocess.run(["VBoxManage", "import", ova_file], check=True)
        print(f"[IMPORT] - VM imported from '{ova_file}' successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] - Failed to import VM: {e}")

def export_vm_to_ova():
    list_vms()
    vm_name = input("[EXPORT] - Enter the VM name to export: ")
    export_path = os.path.join(VM_PATH, f"{vm_name}.ova")
    try:
        subprocess.run(["VBoxManage", "export", vm_name, "--output", export_path], check=True)
        print(f"[EXPORT] - VM '{vm_name}' exported to '{export_path}' successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] - Failed to export VM: {e}")

def delete_vm():
    try:
        result = subprocess.run(["VBoxManage", "list", "vms"], capture_output=True, text=True, check=True)
        vms = [line.split('"')[1] for line in result.stdout.splitlines()]
        files = os.listdir(VM_PATH)
        if not vms and not files:
            print("[LIST] - No VMs or OVA files found.")
            return
        print("[LIST] - Available VMs and OVA files:")
        for vm in vms:
            print(f"- VM: {vm}")
        for file in files:
            if file.lower().endswith('.ova'):
                print(f"- OVA: {file}")
        vm_name = input("[DELETE] - Enter the VM name or OVA file to delete: ")
        if vm_name in vms:
            subprocess.run(["VBoxManage", "unregistervm", vm_name, "--delete"], check=True)
            print(f"[DELETE] - VM '{vm_name}' deleted successfully.")
        elif vm_name in files and vm_name.lower().endswith('.ova'):
            os.remove(os.path.join(VM_PATH, vm_name))
            print(f"[DELETE] - OVA file '{vm_name}' deleted successfully.")
        else:
            print(f"[ERROR] - '{vm_name}' not found.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] - Failed to delete: {e}")

if __name__ == "__main__":
    main_menu()
