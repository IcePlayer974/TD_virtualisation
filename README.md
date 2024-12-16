# TD Virtualisation Project

Ce projet gère les machines virtuelles avec VirtualBox.

## Fonctionnalités Principales
- Création de VM à partir de zéro
- Déploiement de VMs à partir de modèles
- Exportation et importation de fichiers OVA
- Suppression de machines virtuelles et de fichiers OVA
- Liste des VMs disponibles

---
## Réponses aux questions

Partie 2. 

Les possibilités de mode pour la carte réseau sont NAT, Accès par pont, Réseau interne, Réseau privé hôte et pas de réseau. 
Le réseau NAT est utile lorsque l'on souhaite que la VM prenne la même adresse ip que la machine hôte.
Le réseau accès par pont permet de donner une nouvelle adresse ip à la VM est qu'elle soit considéré comme une machine à part entière. 
Le réseau permet à plusieurs VM de communiquer entre elles dans un réseau isolé.
Le réseau privé hôte limite l'accès de la VM à uniquement la machine hôte. 


Partie 3.

Le premier mode est l'exportation de la VM en fichier puis l'importation du fichier dans la nouvelle VM.
Les avantages sont la facilité de personnalisation de la VM, la possibilité d'utiliser cette méthode sur plusieurs logiciels (compatibilité du fichier OVF)
Néanmois, les inconvénients sont la taille des fichiers qui sont volumineux et le processus de exportation et d'importation qui peut être long.

Le second mode est le clonage via Virtual Box directement. 
L'avantage est la rapidité.
Les inconvénients sont le maintien totale de la configuration de la VM source, l'impossibilité d'utiliser cette méthode pour cloner sur un autre logiciel.

---

## Captures d'écran

### 1. Création de VM à partir de zéro
![Création de VM](screenshots/screen1.png)

### 2. Clone de VM
![Clone de VM](screenshots/screen2.png)

### 3. Export en modèle OVA
![Export en OVA](screenshots/screen3.png)

### 4. Suppression d'une VM
![Suppression de VM](screenshots/screen4.png)

### 5. Création à partir d'un modèle OVA
![Création à partir d'un modèle](screenshots/screen5.png)

### 6. Liste des VMs disponibles
![Liste des VMs](screenshots/screen6.png)

---

## ⚠️ Disclaimer
Si vous souhaitez cloner ou utiliser ce projet, **veillez à redéfinir les chemins** (`VM_PATH` et `ISO_PATH`) dans le fichier `TD_virtualisation.py` pour correspondre à votre environnement local. Cela garantira le bon fonctionnement du script.
