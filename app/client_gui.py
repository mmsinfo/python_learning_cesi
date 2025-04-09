import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Utilisateurs")
        self.api_url = "http://localhost:8081"

        # Création des widgets
        self.create_widgets()
        self.refresh_user_list()

    def create_widgets(self):
        # Frame pour la création d'utilisateur
        create_frame = ttk.LabelFrame(self.root, text="Créer un utilisateur", padding="10")
        create_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(create_frame, text="Login:").grid(row=0, column=0, sticky="w")
        self.login_entry = ttk.Entry(create_frame)
        self.login_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(create_frame, text="Mot de passe:").grid(row=1, column=0, sticky="w")
        self.password_entry = ttk.Entry(create_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(create_frame, text="Nom:").grid(row=2, column=0, sticky="w")
        self.name_entry = ttk.Entry(create_frame)
        self.name_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Button(create_frame, text="Créer", command=self.create_user).grid(row=3, column=0, columnspan=2, pady=5)

        # Frame pour la liste des utilisateurs
        list_frame = ttk.LabelFrame(self.root, text="Liste des utilisateurs", padding="10")
        list_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.tree = ttk.Treeview(list_frame, columns=("ID", "Login", "Nom"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Login", text="Login")
        self.tree.heading("Nom", text="Nom")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Boutons de contrôle
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=1, column=0, pady=5)
        ttk.Button(btn_frame, text="Rafraîchir", command=self.refresh_user_list).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Supprimer", command=self.delete_user).pack(side="left", padx=5)

    def create_user(self):
        user_data = {
            "login": self.login_entry.get(),
            "password": self.password_entry.get(),
            "name": self.name_entry.get()
        }

        try:
            response = requests.post(f"{self.api_url}/user", json=user_data)
            if response.status_code == 201:
                messagebox.showinfo("Succès", "Utilisateur créé avec succès!")
                self.refresh_user_list()
                self.clear_entries()
            else:
                messagebox.showerror("Erreur", f"Erreur lors de la création: {response.text}")
        except requests.RequestException as e:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(e)}")

    def refresh_user_list(self):
        try:
            response = requests.get(f"{self.api_url}/user")
            if response.status_code == 200:
                users = response.json()
                self.tree.delete(*self.tree.get_children())
                for user in users:
                    self.tree.insert("", "end", values=(user["id"], user["login"], user["name"]))
        except requests.RequestException as e:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(e)}")

    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un utilisateur")
            return

        user_id = self.tree.item(selected_item[0])["values"][0]
        try:
            response = requests.delete(f"{self.api_url}/user/{user_id}")
            if response.status_code == 204:
                messagebox.showinfo("Succès", "Utilisateur supprimé avec succès!")
                self.refresh_user_list()
            else:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {response.text}")
        except requests.RequestException as e:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(e)}")

    def clear_entries(self):
        self.login_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementApp(root)
    root.mainloop()