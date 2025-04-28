import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
from ImageProcessor import ImageProcessor

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Edycja Obrazów")
        self.processor = None
        self.display_image = None

        # GUI Elements
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        self.brightness_label = tk.Label(root, text="Jasność:")
        self.brightness_label.pack()
        self.brightness_slider = tk.Scale(root, from_=-100, to=100, orient=tk.HORIZONTAL)
        self.brightness_slider.pack()

        self.contrast_label = tk.Label(root, text="Kontrast:")
        self.contrast_label.pack()
        self.contrast_slider = tk.Scale(root, from_=0, to=3, resolution=0.1, orient=tk.HORIZONTAL)
        self.contrast_slider.set(1)  # Default contrast is 1
        self.contrast_slider.pack()

        self.load_button = tk.Button(root, text="Wczytaj Obraz", command=self.load_image)
        self.load_button.pack()

        self.apply_button = tk.Button(root, text="Zastosuj Transformację", command=self.apply_linear)
        self.apply_button.pack()

    def load_image(self):
        path = filedialog.askopenfilename(
            title="Wybierz obraz",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if path:
            try:
                print(f"Załadowano obraz z: {path}")  # Debug: wyświetlenie ścieżki
                self.processor = ImageProcessor(path)
                self.display_image = self.processor.image
                print(f"Załadowany obraz: {self.display_image}")  # Debug: potwierdzenie załadowania obrazu
                self.update_image_display()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się załadować obrazu: {str(e)}")

    def apply_linear(self):
        if self.processor:
            brightness = self.brightness_slider.get()
            contrast = self.contrast_slider.get()
            print(f"Zastosowanie transformacji: Jasność={brightness}, Kontrast={contrast}")  # Debug
            transformed_image = self.processor.linear_transform(brightness=brightness, contrast=contrast)
            self.display_image = transformed_image
            self.update_image_display()
        else:
            messagebox.showerror("Błąd", "Proszę najpierw załadować obraz.")

    def update_image_display(self):
        if self.display_image:
            self.display_image = self.display_image.resize((500, 500))  # Resize for display in the canvas
            self.display_image = ImageTk.PhotoImage(self.display_image)

            # Debug: Sprawdzenie czy obraz jest poprawnie przekonwertowany
            print(f"Obraz do wyświetlenia: {self.display_image}")

            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)
        else:
            messagebox.showerror("Błąd", "Obraz nie został załadowany.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
