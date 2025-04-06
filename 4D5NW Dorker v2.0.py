import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from duckduckgo_search import DDGS
import requests
import re
import time

class DorkScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("4D5NW Dorker v2.0")
        self.root.geometry("850x750")

        self.dork_list = []
        self.results = []
        self.emails = set()
        self.delay = tk.IntVar(value=3)
        self.darkmode = tk.BooleanVar(value=False)

        # GUI Elemente
        tk.Button(root, text="Dork-Liste laden", command=self.load_dork_file).pack(pady=5)
        tk.Button(root, text="Normale Suche starten", command=self.run_search).pack(pady=5)
        tk.Button(root, text="Nur E-Mails extrahieren", command=self.run_email_extraction).pack(pady=5)

        tk.Label(root, text="Verzögerung zwischen Anfragen (Sekunden):").pack()
        tk.Scale(root, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.delay).pack()

        tk.Label(root, text="E-Mail-Domains (z. B. icloud.com, beispiel.de):").pack()
        self.domain_entry = tk.Entry(root, width=50)
        self.domain_entry.insert(0, "wunschdomain.de")
        self.domain_entry.pack(pady=5)

        self.result_box = scrolledtext.ScrolledText(root, width=105, height=25)
        self.result_box.pack(pady=10)

        tk.Label(root, text="Fortschritt:").pack()
        self.progress = tk.DoubleVar()
        self.progressbar = ttk.Progressbar(root, maximum=100, variable=self.progress, length=600)
        self.progressbar.pack(pady=5)

        tk.Button(root, text="Ergebnisse speichern", command=self.save_results).pack(pady=5)
        tk.Checkbutton(root, text="Darkmode aktivieren", variable=self.darkmode, command=self.toggle_darkmode).pack(pady=5)
        tk.Button(root, text="Hilfe anzeigen", command=self.show_help).pack(pady=5)

        self.apply_theme()

    def toggle_darkmode(self):
        self.apply_theme()

    def apply_theme(self):
        dark = self.darkmode.get()
        bg = "#1e1e1e" if dark else "#f0f0f0"
        fg = "#ffffff" if dark else "#000000"
        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=bg, fg=fg)
            except:
                pass
        self.result_box.configure(bg="#2e2e2e" if dark else "#ffffff", fg=fg, insertbackground=fg)

    def show_help(self):
        help_text = (
            "4D5NW Dorker v2.0 - Hilfe\n\n"
            "1. Lade eine Dork-Liste (.txt)\n"
            "2. Gib Domains ein (z. B. wunschdomain.de, icloud.com)\n"
            "3. Wähle eine Verzögerung (empfohlen: 15–20 Sekunden)\n"
            "4. Starte entweder:\n"
            "   - Normale Suche (zeigt URLs)\n"
            "   - E-Mail-Extraktion (scannt Seiten nach E-Mails)\n"
            "5. Aktiviere optional den Darkmode\n"
            "6. Speichere die Ergebnisse\n\n"
            "Nur für ethische und legale Zwecke verwenden!"
        )
        help_win = tk.Toplevel(self.root)
        help_win.title("Hilfe")
        help_win.geometry("600x400")
        text = scrolledtext.ScrolledText(help_win, wrap=tk.WORD)
        text.insert(tk.END, help_text)
        text.configure(state="disabled")
        text.pack(expand=True, fill="both", padx=10, pady=10)

    def load_dork_file(self):
        path = filedialog.askopenfilename(filetypes=[("Textdateien", "*.txt")])
        if path:
            with open(path, "r") as file:
                self.dork_list = [line.strip() for line in file if line.strip()]
            messagebox.showinfo("Dorks geladen", f"{len(self.dork_list)} Dorks wurden geladen.")

    def run_search(self):
        if not self.dork_list:
            messagebox.showwarning("Keine Dorks", "Bitte zuerst eine Dork-Liste laden.")
            return

        self.result_box.delete(1.0, tk.END)
        self.results.clear()
        delay_time = self.delay.get()
        total = len(self.dork_list)

        with DDGS() as ddgs:
            for index, dork in enumerate(self.dork_list):
                percent = (index + 1) / total * 100
                self.progress.set(percent)
                self.root.update()

                self.result_box.insert(tk.END, f"[+] Suche nach: {dork}\n")
                self.root.update()

                try:
                    hits = ddgs.text(dork, max_results=10)
                    for res in hits:
                        result_line = f"{dork} | {res['href']}\n"
                        self.result_box.insert(tk.END, result_line)
                        self.results.append(result_line)
                except Exception as e:
                    self.result_box.insert(tk.END, f"[!] Fehler bei '{dork}': {e}\n")

                self.result_box.insert(tk.END, "-"*60 + "\n")
                self.root.update()
                time.sleep(delay_time)

        messagebox.showinfo("Fertig", "Die Suche ist abgeschlossen.")

    def run_email_extraction(self):
        if not self.dork_list:
            messagebox.showwarning("Keine Dorks", "Bitte zuerst eine Dork-Liste laden.")
            return

        domains_raw = self.domain_entry.get().strip()
        if not domains_raw:
            messagebox.showwarning("Keine Domains", "Bitte mindestens eine Domain eingeben.")
            return

        domains = [d.strip() for d in domains_raw.split(",") if d.strip()]
        if not domains:
            messagebox.showerror("Fehler", "Die Domains konnten nicht korrekt gelesen werden.")
            return

        self.result_box.delete(1.0, tk.END)
        self.results.clear()
        self.emails.clear()

        pattern = "|".join(re.escape(domain) for domain in domains)
        email_regex = rf"[a-zA-Z0-9._%+-]+@(?:{pattern})"
        self.result_box.insert(tk.END, f"[i] Verwende Regex: {email_regex}\n\n")
        self.root.update()

        delay_time = self.delay.get()
        total = len(self.dork_list)

        with DDGS() as ddgs:
            for index, dork in enumerate(self.dork_list):
                percent = (index + 1) / total * 100
                self.progress.set(percent)
                self.root.update()

                self.result_box.insert(tk.END, f"[+] Suche nach: {dork}\n")
                self.root.update()

                try:
                    hits = ddgs.text(dork, max_results=10)
                    if not hits:
                        self.result_box.insert(tk.END, "  [!] Keine Treffer für diesen Dork.\n")
                        continue

                    for res in hits:
                        url = res['href']
                        self.result_box.insert(tk.END, f"  > Lade: {url}\n")
                        self.root.update()
                        try:
                            response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
                            if response.status_code != 200:
                                self.result_box.insert(tk.END, f"    [!] HTTP {response.status_code} – wird übersprungen\n")
                                continue

                            emails = re.findall(email_regex, response.text)
                            if emails:
                                for email in emails:
                                    if email not in self.emails:
                                        self.result_box.insert(tk.END, f"    [✓] {email}\n")
                                        self.emails.add(email)
                            else:
                                self.result_box.insert(tk.END, f"    [-] Keine E-Mails gefunden.\n")

                        except Exception as req_err:
                            self.result_box.insert(tk.END, f"    [!] Fehler beim Abrufen: {req_err}\n")

                        time.sleep(delay_time)

                except Exception as e:
                    self.result_box.insert(tk.END, f"[!] Fehler bei '{dork}': {e}\n")

                self.result_box.insert(tk.END, "-"*60 + "\n")
                self.root.update()

        if self.emails:
            self.result_box.insert(tk.END, "\n[✓] Alle gefundenen E-Mail-Adressen:\n")
            for mail in sorted(self.emails):
                self.result_box.insert(tk.END, f"{mail}\n")
        else:
            self.result_box.insert(tk.END, "\n[-] Keine E-Mail-Adressen gefunden.\n")

        messagebox.showinfo("Fertig", f"E-Mail-Extraktion abgeschlossen. {len(self.emails)} E-Mails gefunden.")

    def save_results(self):
        if not self.results and not self.emails:
            messagebox.showwarning("Keine Ergebnisse", "Es gibt keine Ergebnisse zum Speichern.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Textdateien", "*.txt")])
        if path:
            with open(path, "w") as file:
                if self.results:
                    file.write("[+] Normale Suchergebnisse:\n")
                    file.writelines(self.results)
                    file.write("\n")

                if self.emails:
                    file.write("[+] Gefundene E-Mail-Adressen:\n")
                    for mail in sorted(self.emails):
                        file.write(mail + "\n")

            messagebox.showinfo("Gespeichert", "Ergebnisse wurden gespeichert.")

# Start
if __name__ == "__main__":
    root = tk.Tk()
    app = DorkScannerApp(root)
    root.mainloop()