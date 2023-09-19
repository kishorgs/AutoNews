from tkinter import *
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import io
import webbrowser

class NewsApp:
    def __init__(self, parent):
        self.parent = parent
        self.parent.geometry("900x600")
        self.parent.title("NMIT News")
        self.parent.configure(bg="#1E2534")  # Dark background color

        self.show_home_page()

    def show_home_page(self):
        home_frame = Frame(self.parent, bg="#1E2534")  # Dark background color
        home_frame.pack(fill="both", expand=True)

        # Add a heading label
        heading_label = Label(
            home_frame,
            text="Welcome to our news app",
            bg="#1E2534",  # Dark background color
            fg="#FFAB40",  # Custom highlight color
            font=("Helvetica", 18, "bold"),
            pady=20  # Add some padding below the heading
        )
        heading_label.pack()

        news_articles = self.get_top_trending_news()

        canvas = Canvas(home_frame, bg="#1E2534", borderwidth=0, highlightthickness=0)  # Dark background color, remove border
        canvas.pack(side="left", fill="both", expand=True)

        canvas.bind("<Configure>", self.on_canvas_configure)

        news_frame = Frame(canvas, bg="#1E2534")  # Dark background color
        canvas.create_window((0, 0), window=news_frame, anchor="nw")

        scrollbar = ttk.Scrollbar(
            home_frame,
            orient="vertical",
            command=canvas.yview,
            style="Custom.Vertical.TScrollbar"  # Apply the custom scrollbar style
        )
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        for i, (title, image_url, description, news_url) in enumerate(news_articles):
            news_item_frame = Frame(
                news_frame,
                bg="#1E2534",  # Dark background color
                padx=40,  # Add 40-pixel padding
                pady=40   # Add 40-pixel padding
            )
            news_item_frame.grid(sticky="nsew")

            image_response = requests.get(image_url)
            image = Image.open(io.BytesIO(image_response.content))
            image = image.resize((200, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image=image)

            image_label = Label(news_item_frame, image=photo, bg="#1E2534")  # Dark background color
            image_label.photo = photo
            image_label.grid(row=0, column=0, rowspan=3, sticky="w")

            title_label = Label(
                news_item_frame,
                text=title,
                bg="#1E2534",  # Dark background color
                fg="#FFAB40",  # Custom highlight color
                font=("Helvetica", 14, "bold"),
                wraplength=600,
                justify="left"
            )
            title_label.grid(row=0, column=1, sticky="w")

            description_text = Text(
                news_item_frame,
                wrap=WORD,
                bg="#1E2534",  # Dark background color
                fg="#FFFFFF",  # White text color
                font=("Helvetica", 12),
                height=4,
                width=40,
                borderwidth=0  # Remove border
            )
            description_text.insert(INSERT, description)
            description_text.config(state=DISABLED)

            description_text.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

            view_button = Button(
                news_item_frame,
                text="View Full News",
                bg="#FFAB40",  # Custom highlight color
                fg="#1E2534",  # Dark background color
                font=("Helvetica", 12, "bold"),
                command=lambda url=news_url: self.open_news_source(url)
            )
            view_button.grid(row=3, column=1, sticky="e")  # Move to row 3, remove padding, and stick to the right
            view_button.grid_propagate(False)  # Prevent the button from resizing

            news_item_frame.grid_columnconfigure(1, weight=1)  # Expand column 1
            news_item_frame.grid_rowconfigure(1, weight=1)  # Expand row 1

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def open_news_source(self, url):
        webbrowser.open_new(url)

    def get_top_trending_news(self):
        main_url = "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=1e686cc3f51f4e23ba548d706ca463c9&pageSize=50"
        try:
            news_data = requests.get(main_url).json()
            articles = news_data["articles"]
            return [(article['title'], article['urlToImage'], article['description'], article['url']) for article in articles]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news data: {e}")
            return []

if __name__ == "__main__":
    root = Tk()
    app = NewsApp(root)
    root.mainloop()
