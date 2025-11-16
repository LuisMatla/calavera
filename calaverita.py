import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import itertools
from tkinter import ttk
from itertools import cycle
import pygame

class VentanaAnimada:
    def __init__(self, root):
        self.root = root
        self.root.title("Ofrenda Virtual")
        self.root.geometry("1150x750")
        #cargar icono compatible con linux.
        try:
            icon_image = Image.open("calavera.ico")
            self.icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(False, self.icon_photo)
        except Exception as e:
            print(f"Error al cargar el icono: {e}")
        
        #inicializar pygame para el audio.
        pygame.mixer.init()
        try:
            pygame.mixer.music.load("La Muerte y La Ecuación.mp3")
            pygame.mixer.music.play(-1)  #reproducir música automáticamente en loop.
        except Exception as e:
            print(f"Error al cargar la música: {e}")
        
        #marco decorativo.
        self.marco = tk.Frame(self.root, bg="#FF8C00", bd=10)
        self.marco.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        #canvas.
        self.canvas = tk.Canvas(self.marco, bg="#B2EBF2")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        #variables de estado.
        self.frames_gifs = {'izquierda': None, 'centro': None, 'derecha': None}
        self.frame_actual = {'izquierda': 0, 'centro': 0, 'derecha': 0}
        self.gif_en_canvas = {'izquierda': None, 'centro': None, 'derecha': None}
        
        #cargar y colocar las imágenes de tumbitas.
        try:
            #cargar imagen de diana.
            diana_img = Image.open("tumbitawoo.png")
            diana_img = diana_img.resize((150, 140), Image.LANCZOS)
            self.diana_photo = ImageTk.PhotoImage(diana_img)
            self.canvas.create_image(100, 547, anchor="nw", image=self.diana_photo)
            
            #cargar imagen de woo.
            woo_img = Image.open("tumbitadiana.png")
            woo_img = woo_img.resize((150, 140), Image.LANCZOS)
            self.woo_photo = ImageTk.PhotoImage(woo_img)
            self.canvas.create_image(850, 547, anchor="nw", image=self.woo_photo)
        except Exception as e:
            print(f"Error al cargar las imágenes: {e}")
        
        #variables para velitas.
        self.velita_frames = []
        self.velita_items = []
        self.velita_index = 0
        
        #línea decorativa.
        self.canvas.create_line(15, 20, 1100, 15, fill="black", width=2)
        
        #cargar imágenes del papel picado.
        self.imagenes_papel = []
        for i in range(1, 5):
            imagen = Image.open(f"papel{i}.png").resize((50, 42), Image.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.imagenes_papel.append(imagen_tk)
        
        #colocar papeles picados.
        self.colocar_papeles_picados()
        
        #cursor personalizado.
        cursor_image = Image.open("calaveramouse.png").resize((40, 40), Image.LANCZOS)
        self.imagen_cursor_tk = ImageTk.PhotoImage(cursor_image)
        self.imagen_cursor = self.canvas.create_image(0, 0, anchor="center", image=self.imagen_cursor_tk)
        
        #dividir la calaverita en dos partes.
        self.parte1 = """Estaba la muerte resolviendo una ecuacion diferencial,
Que ni la maestra Diana había podido controlar
Pues la integración por partes tampoco era el método para avanzar.

Acudieron al cementerio,
se encontraron a la profesora Woo
Con sus conocimientos de electrónica,
parecía una gurú
No la pudo resolver ella, ni Diana, ni tú."""

        self.parte2 = """Programarla en python quizá era el remedio
Pero en el curso de IA no estaba la ecuación en el libreto
La resolución de esa ecuacion diferencial
parecía el más profundo secreto.

A todas las personas que nos visitan del más allá
Su ayuda para resolver esta ecuacion diferencial
les venimos a implorar
Ya que ni Luis, Poli, Samuel y Matla lograron concretar
Así que una calaverita se pusieron a redactar."""

        #variable para controlar qué parte se muestra.
        self.mostrar_parte1 = True
        
        #crear un rectángulo semitransparente para el fondo del texto.
        self.texto_bg = self.canvas.create_rectangle(
            150, 150, 950, 400,
            fill='#B2EBF2',
            outline='#FF8C00',
            width=8
        )
        
        #texto inicial parte 1.
        self.texto_calaverita = self.canvas.create_text(
            550, 275,
            text=self.parte1,
            fill="black", 
            font=("impact", 14),
            anchor="center",
            justify="center"
        )
        
        #botón para cambiar entre partes.
        self.boton_cambiar = tk.Button(
            self.canvas,
            text="Siguiente Parte",
            font=("arial", 12),
            command=self.cambiar_texto,
            bg="#FF8C00",
            fg="black",
            relief="raised",
            bd=3
        )
        self.boton_cambiar_window = self.canvas.create_window(
            550, 440,
            window=self.boton_cambiar,
            anchor="center"
        )
        
        #cargar gifs y velitas.
        self.cargar_gifs()
        self.cargar_velitas()
        
        #configuración de animación del texto.
        self.animacion = itertools.cycle([0, 2, 4, 2, 0, -2, -4, -2])
        self.animar_calaverita()
        
        #colores para el fondo modificados para día de muertos.
        self.colores = cycle([
            '#800020',  #naranja cempasúchil.
            '#4B0082',  #índigo morado tradicional.
            '#8B4513',  #marrón color tierra barro.
            '#8b1362',
            '#c5c174',
            '#138b75'   #dorado para las veladoras.
        ])
        
        #configuración del cursor.
        self.root.config(cursor="none")
        self.canvas.bind("<Motion>", self.actualizar_posicion)
        
        #iniciar animaciones.
        self.actualizar_velitas()
        self.animar_gifs()
        
        #configurar el cierre de la ventana.
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def cerrar_aplicacion(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.root.destroy()

    def cargar_gifs(self):
        y_position = 550
        
        gif_info = {
            'izquierda': ("Calaverita.gif", (350, y_position)),
            'centro': ("CalaveraBaileSuelo.gif", (550, y_position)),
            'derecha': ("CalaveraTocandoSaxofon.gif", (750, y_position))
        }
        
        for gif_id, (filename, position) in gif_info.items():
            try:
                gif = Image.open(filename)
                frames = []
                
                for frame in ImageSequence.Iterator(gif):
                    frame = frame.resize((200, 200), Image.LANCZOS)
                    frame_tk = ImageTk.PhotoImage(frame)
                    frames.append(frame_tk)
                
                self.frames_gifs[gif_id] = frames
                self.gif_en_canvas[gif_id] = self.canvas.create_image(
                    position[0], position[1],
                    image=frames[0]
                )
                
            except Exception as e:
                print(f"Error al cargar el GIF {filename}: {e}")
                self.frames_gifs[gif_id] = None

    def cambiar_texto(self):
        self.mostrar_parte1 = not self.mostrar_parte1
        texto_actual = self.parte1 if self.mostrar_parte1 else self.parte2
        self.boton_cambiar.config(text="Siguiente Parte" if self.mostrar_parte1 else "Parte Anterior")
        self.canvas.itemconfig(self.texto_calaverita, text=texto_actual)

    def colocar_papeles_picados(self):
        x = 35
        espacio = 74
        for i in range(15):
            imagen = self.imagenes_papel[i % len(self.imagenes_papel)]
            self.canvas.create_image(x, 20, anchor="n", image=imagen)
            x += espacio

    def cargar_velitas(self):
        velita_gif = Image.open("velita.gif")
        for i in range(velita_gif.n_frames):
            velita_gif.seek(i)
            frame = velita_gif.copy().resize((60, 60), Image.LANCZOS).convert("RGBA").convert("P")
            self.velita_frames.append(ImageTk.PhotoImage(frame))

        velita_positions = [(350, 670), (450, 670), (550, 670), 
                          (650, 670), (750, 670)]
        
        for pos in velita_positions:
            velita_item = self.canvas.create_image(pos[0], pos[1], image=self.velita_frames[0])
            self.velita_items.append(velita_item)

    def actualizar_velitas(self):
        self.velita_index = (self.velita_index + 1) % len(self.velita_frames)
        for item in self.velita_items:
            self.canvas.itemconfig(item, image=self.velita_frames[self.velita_index])
        self.root.after(100, self.actualizar_velitas)

    def animar_gifs(self):
        for gif_id in self.frames_gifs:
            if self.frames_gifs[gif_id]:
                self.frame_actual[gif_id] = (self.frame_actual[gif_id] + 1) % len(self.frames_gifs[gif_id])
                self.canvas.itemconfig(
                    self.gif_en_canvas[gif_id],
                    image=self.frames_gifs[gif_id][self.frame_actual[gif_id]]
                )
        
        if self.frame_actual['centro'] % 40 == 0:
            self.canvas.configure(bg=next(self.colores))
            self.canvas.itemconfig(self.texto_bg, fill='#B2EBF2')
        
        self.root.after(20, self.animar_gifs)

    def mover_cursor(self, event):
        if not self.root.winfo_exists():
            return
        self.canvas.coords(self.imagen_cursor, event.x, event.y)
        self.canvas.tag_raise(self.imagen_cursor)
    
    def actualizar_posicion(self, event):
        self.root.after(5, self.mover_cursor, event)
    
    def animar_calaverita(self):
        y_base = 275
        y = y_base + next(self.animacion)
        self.canvas.coords(self.texto_calaverita, 550, y)
        self.canvas.coords(self.texto_bg, 150, y-125, 950, y+125)
        self.root.after(150, self.animar_calaverita)

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaAnimada(root)
    root.mainloop()