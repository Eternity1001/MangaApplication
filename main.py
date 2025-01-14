
import tkinter as tk
from PIL import ImageTk, Image
from Application.database import get_con, read, create_database
from sys import argv
from Application.scraper import refresh
from os import remove, rmdir, mkdir
from shutil import rmtree
import platform
from re import sub
class Store:
    def __init__(self):
        self.photo = {}
        self.main_frame = None
        self.manga_frames = {}  
        self.latest_title = ''
    
    def append(self, img):
        self.photo.append(img)
        

class Application():
    
    def __init__(self):
        self.root: tk.Tk = tk.Tk()
        self.store: Store = Store()
        self.con = get_con()

    
    def configure(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
    
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
    
        canvas = tk.Canvas(main_frame, bg='black', width=1280, height=1440)
        canvas.grid(row=0, column=0, sticky='nsew')
    
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollbar.grid(row=0, column=0, sticky='nse', padx=0, pady=0)
    
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas_frame = tk.Frame(canvas, bg='black')
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(1, weight=1)
    
        canvas_window = canvas.create_window(
            (0, 0),
            window=canvas_frame,
            anchor='nw',
            width=1280
        )
    
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
    
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        def on_mousewheel(event):
            if platform.system() == 'Windows':
                canvas.yview_scroll(int(-1 * (event.delta/120)), "units")
            elif platform.system() == 'Darwin':  # macOS
                canvas.yview_scroll(int(-1 * event.delta), "units")
            else:  
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
    
        canvas.bind("<MouseWheel>", on_mousewheel)  
        canvas.bind("<Button-4>", on_mousewheel)    
        canvas.bind("<Button-5>", on_mousewheel)    
        canvas.bind("<Command-MouseWheel>", on_mousewheel)  
        canvas_frame.bind("<MouseWheel>", on_mousewheel)
        canvas_frame.bind("<Button-4>", on_mousewheel)
        canvas_frame.bind("<Button-5>", on_mousewheel)
        canvas_frame.bind("<Command-MouseWheel>", on_mousewheel)
    
        def bind_tree(widget):
            widget.bind("<MouseWheel>", on_mousewheel)
            widget.bind("<Button-4>", on_mousewheel)
            widget.bind("<Button-5>", on_mousewheel)
            widget.bind("<Command-MouseWheel>", on_mousewheel)
            for child in widget.children.values():
                bind_tree(child)
    
        bind_tree(canvas_frame)
        canvas_frame.bind('<Configure>', on_frame_configure)
        canvas.bind('<Configure>', on_canvas_configure)
        return canvas_frame
    
    
    def back(self, store: Store, manga_frame):
        manga_frame.grid_remove()
        store.main_frame.grid()
    
    def label_click(self, event):
        manga_name = event.widget['text'].split('\n')[0].split("Title: ")[1].strip(" ")
    
        self.store.main_frame.grid_remove()
    
        if manga_name in self.store.manga_frames:
            self.store.manga_frames[manga_name].grid()
            return
    
        manga_frame = tk.Frame(self.root)
        manga_frame.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
        manga_frame.grid_rowconfigure(0, weight=1)
        manga_frame.grid_columnconfigure(0, weight=1)
        canvas = tk.Canvas(manga_frame, bg='black', width=1280, height=1440)
        canvas.grid(row=0, column=0, sticky='nsew')
        canvas_frame = tk.Frame(canvas, bg='black')
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(1, weight=1)
    
        canvas_window = canvas.create_window(
            (0, 0),
            window=canvas_frame,
            anchor='nw',
            width=1280
        )
    
        back_button = tk.Button(
            canvas_frame, 
            text="← Back", 
            fg='white', 
            bg='black',
            command=lambda: self.back(self.store, manga_frame)
        )
        back_button.grid(column=0, row=0, sticky='w', padx=10, pady=10)
    
        title_label = tk.Label(
            canvas_frame, 
            text=manga_name, 
            fg='white', 
            bg='black',
            font=('Arial', 16, 'bold'),
            justify='center', 
        )
      
        manga_info = tk.Label(
            canvas_frame, 
            text = "Hello Wolrd, are you gaY?", 
            fg = 'white',
            bg ='black',
            padx = 10,
            justify = 'left',
            wraplength = 400,
            borderwidth = 20,
            image = self.store.photo[manga_name],
            compound = 'top'
        
        )
        chapters = {}
        for i in self.con.cursor().execute(f"SELECT Chapter FROM Manga WHERE Title='{self.store.latest_title}'"):
            chapters = self.to_dict(i[0])
        
        
        
        for key, value in chapters.items():
            chapter_label = tk.Label(
                canvas_frame,
                
            )
        
        # chapter_label = tk.Label(
        #     canvas_frame, 
            
        # )
        
    
        manga_info.grid(column=1, row = 2, sticky= 'w')
        title_label.grid(column=1, row=1, sticky='w', padx=10, pady=10)

        self.store.manga_frames[manga_name] = manga_frame
    
    def to_dict(self, i):
        
        i = i[1:-2].split(",")
        chapter_link = {}
        for chapters in i:
            chapter = chapters.split("'")[1].split("'")[0]
            link = chapters.split(": '")[1].split("'")[0]
            chapter_link[chapter] = link
            
        return chapter_link                    
    
    
    def image_grid(self, root):
        count = 0
        row = 0
        cursor = self.con.cursor()
    
        for i in cursor.execute("SELECT * FROM Manga"):
            try:
                image = ImageTk.PhotoImage(Image.open(f".venv/Manga/{i[0]}/thumpnail/thumpnail.jpeg").resize((100, 100)))

                description = f"Title: {i[0]}\n\nGenre: {i[1][1:-2]}'"
                manga_img = tk.Label(
                    root, 
                    bg='black', 
                    text=description, 
                    fg='white', 
                    justify='left', 
                    wraplength=400,
                    borderwidth=20, 
                    padx=10, 
                    image=image, 
                    compound="left"
                )
                manga_img.grid(column=count % 2, row=row, sticky='w', padx=10, pady=5)
                self.store.latest_title = i[0]
                manga_img.bind("<Button-1>", lambda e, s=self.store: self.label_click(e))

                count += 1
                if count % 2 == 0:
                    row += 1
                self.store.photo[i[0]] = image
            except FileNotFoundError:
                print(f'{i[0]} Doesnt exist')

    
    def start(self):
        self.root.geometry("1280x1440")
        canvas_frame = self.configure()
        self.store.main_frame = canvas_frame.master.master
        self.image_grid(canvas_frame)
        self.root.mainloop()
        
        




if __name__ == "__main__":  
    
    app = Application()
    if argv.__contains__("-reset"):
        remove(".venv/Manga.db")
        rmtree('./.venv/Manga')
        mkdir("./.venv/Manga")
        create_database()

    if argv.__contains__("-read"):
        read()
    
    if argv.__contains__("-refresh"):
        refresh(app.con)
        
        
    app.start()
    
        
    
    
