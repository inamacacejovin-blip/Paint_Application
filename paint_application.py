import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk

# 1. PEACH COLOR PALETTE AND FONT (change these to make the design your own)
PEACH_BG = "#EAF7EA"       # light green window background       # window background
PEACH_PANEL = "#FFFFFF"    # white toolbar background    # toolbar background
PEACH_BUTTON = "#A8D5A2"   # soft green buttons   # button color
PEACH_HOVER = "#78B879"    # darker green on hover    # button color while it is pressed
TEXT_COLOR = "#214D2B"     # dark green text     # text color
FONT_MAIN = ("Arial", 10, "bold")

CANVAS_WIDTH = 900
CANVAS_HEIGHT = 550

root = tk.Tk()
root.title("My Paint Application")
root.geometry("1000x735")
root.configure(bg=PEACH_BG)

# A frame around the canvas works as a peach border.
canvas_frame = tk.Frame(root, bg=PEACH_BUTTON, padx=4, pady=4)
canvas_frame.pack(padx=20, pady=15)

canvas = tk.Canvas(canvas_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                   bg="white", cursor="cross", highlightthickness=0)
canvas.pack()

# Pillow image stores the drawing so it can be saved.
image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")
draw = ImageDraw.Draw(image)
canvas_image = None

current_color = "black"
brush_size = 5
tool = "brush"
start_x = start_y = None
last_x = last_y = None
preview_shape = None

# Store previous canvas images for the Undo button.
undo_history = []
MAX_UNDO_STEPS = 50

# Checkbox setting for filled shapes.
fill_shapes = tk.BooleanVar(value=False)


# Save the canvas before each drawing action.
def save_undo_state():
    undo_history.append(image.copy())
    if len(undo_history) > MAX_UNDO_STEPS:
        undo_history.pop(0)


def choose_color():
    """Open the color chooser and update the drawing color."""
    global current_color, tool
    selected = colorchooser.askcolor(title="Choose a color")
    if selected[1] is not None:
        current_color = selected[1]
        tool = "brush"
        color_button.config(bg=current_color)


def set_tool(selected_tool):
    """Change the active drawing tool."""
    global tool
    tool = selected_tool


def change_brush_size(value):
    """Update the brush size using the slider."""
    global brush_size
    brush_size = int(float(value))


# Change the drawing color using a quick-color button.
def set_quick_color(color):
    global current_color, tool
    current_color = color
    tool = "brush"
    color_button.config(bg=current_color)


def start_drawing(event):
    """Remember the mouse position when drawing starts."""
    global last_x, last_y, start_x, start_y
    last_x, last_y = event.x, event.y
    start_x, start_y = event.x, event.y

    # Save one undo point for this complete mouse action.
    save_undo_state()


def draw_motion(event):
    """Draw while the left mouse button is held."""
    global last_x, last_y
    color = "white" if tool == "eraser" else current_color
    if tool in ("brush", "eraser"):
        # Draw on the visible Tkinter canvas.
        canvas.create_line(last_x, last_y, event.x, event.y,
                           fill=color, width=brush_size,
                           capstyle=tk.ROUND, smooth=True)
        # Draw on the Pillow image for saving.
        draw.line((last_x, last_y, event.x, event.y),
                  fill=color, width=brush_size)
        last_x, last_y = event.x, event.y
    else:
        preview_shape_drawing(event)

# Shape preview when mouse is being dragged
def preview_shape_drawing(event):
    """Show a temporary shape while the mouse is dragged."""
    global preview_shape
    if preview_shape is not None:
        canvas.delete(preview_shape)

    if tool == "line":
        preview_shape = canvas.create_line(
            start_x, start_y, event.x, event.y,
            fill=current_color, width=brush_size)

    elif tool == "rectangle":
        preview_shape = canvas.create_rectangle(
            start_x, start_y, event.x, event.y,
            outline=current_color, width=brush_size,
            fill=current_color if fill_shapes.get() else "")

    elif tool == "oval":
        preview_shape = canvas.create_oval(
            start_x, start_y, event.x, event.y,
            outline=current_color, width=brush_size,
            fill=current_color if fill_shapes.get() else "")

    elif tool == "triangle":
        points = [( (start_x + event.x) / 2, start_y),
                  (start_x, event.y),
                  (event.x, event.y)]
        preview_shape = canvas.create_polygon(
            points, outline=current_color, width=brush_size,
            fill=current_color if fill_shapes.get() else "")


# store shapes in the pillow image
def finish_drawing(event):
    """Store the selected shape in the Pillow image."""
    global preview_shape

    if tool == "line":
        draw.line((start_x, start_y, event.x, event.y),
                  fill=current_color, width=brush_size)

    elif tool == "rectangle":
        if fill_shapes.get():
            draw.rectangle((start_x, start_y, event.x, event.y),
                           fill=current_color, outline=current_color,
                           width=brush_size)
        else:
            draw.rectangle((start_x, start_y, event.x, event.y),
                           outline=current_color, width=brush_size)

    elif tool == "oval":
        if fill_shapes.get():
            draw.ellipse((start_x, start_y, event.x, event.y),
                         fill=current_color, outline=current_color,
                         width=brush_size)
        else:
            draw.ellipse((start_x, start_y, event.x, event.y),
                         outline=current_color, width=brush_size)

    elif tool == "triangle":
        points = [((start_x + event.x) / 2, start_y),
                  (start_x, event.y),
                  (event.x, event.y)]
        if fill_shapes.get():
            draw.polygon(points, fill=current_color, outline=current_color)
        else:
            draw.polygon(points, outline=current_color)

    if tool in ("line", "rectangle", "oval", "triangle"):
        preview_shape = None
        refresh_canvas()


def refresh_canvas():
    """Display the current Pillow image on the Tkinter canvas."""
    global canvas_image
    canvas.delete("all")
    canvas_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=canvas_image)


def clear_canvas():
    """Ask for confirmation, then replace the drawing with a blank image."""
    global image, draw, preview_shape

    # ask the user if it wants to clear the canvas
    answer = messagebox.askyesno(
        "Clear Canvas",
        "Are you sure you want to clear the canvas?"
    )
    if answer:
        save_undo_state()
        image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")
        draw = ImageDraw.Draw(image)
        preview_shape = None
        refresh_canvas()


# Undo button added
def undo():
    global image, draw, preview_shape
    if undo_history:
        image = undo_history.pop()
        draw = ImageDraw.Draw(image)
        preview_shape = None
        refresh_canvas()
    else:
        messagebox.showinfo("Undo", "There is no action to undo.")


def open_image():
    """Open an image and display it on the canvas."""
    global image, draw
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
    if file_path:
        try:
            opened_image = Image.open(file_path).convert("RGB")
            opened_image = opened_image.resize((CANVAS_WIDTH, CANVAS_HEIGHT))
            save_undo_state()
            image = opened_image
            draw = ImageDraw.Draw(image)
            refresh_canvas()
        except Exception as error:
            messagebox.showerror("Error", f"Could not open image:\n{error}")


def save_image():
    """Save the current drawing as an image file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png"),
                   ("JPEG Image", "*.jpg"),
                   ("Bitmap Image", "*.bmp")])
    if file_path:
        try:
            image.save(file_path)
            messagebox.showinfo("Saved", "Your drawing has been saved!")
        except Exception as error:
            messagebox.showerror("Error", f"Could not save image:\n{error}")


def make_button(parent, text, command):
    """Create one green button so we do not repeat the styling."""
    return tk.Button(parent, text=text, command=command,
                     bg=PEACH_BUTTON, fg=TEXT_COLOR,
                     activebackground=PEACH_HOVER, activeforeground=TEXT_COLOR,
                     font=FONT_MAIN, relief="flat", padx=10, pady=4,
                     cursor="hand2")


toolbar = tk.Frame(root, bg=PEACH_PANEL, padx=10, pady=8)
toolbar.pack(pady=5)

# Buttons
color_button = make_button(toolbar, "Choose Color", choose_color)
color_button.pack(side="left", padx=4)

make_button(toolbar, "Brush",
            lambda: set_tool("brush")).pack(side="left", padx=4)
make_button(toolbar, "Eraser",
            lambda: set_tool("eraser")).pack(side="left", padx=4)
make_button(toolbar, "Line",
            lambda: set_tool("line")).pack(side="left", padx=4)
make_button(toolbar, "Rectangle",
            lambda: set_tool("rectangle")).pack(side="left", padx=4)
make_button(toolbar, "Oval",
            lambda: set_tool("oval")).pack(side="left", padx=4)

tk.Label(toolbar, text="Brush Size:", bg=PEACH_PANEL,
         fg=TEXT_COLOR, font=FONT_MAIN).pack(side="left", padx=(10, 3))

#Brush-size range increased from 1-30 to 1-100.
size_slider = tk.Scale(toolbar, from_=1, to=100, orient="horizontal",
                       command=change_brush_size, length=100,
                       bg=PEACH_PANEL, fg=TEXT_COLOR,
                       troughcolor=PEACH_BUTTON, highlightthickness=0)
size_slider.set(5)
size_slider.pack(side="left", padx=3)

# Clear, save, and open buttons
make_button(toolbar, "Clear", clear_canvas).pack(side="left", padx=4)
make_button(toolbar, "Open", open_image).pack(side="left", padx=4)
make_button(toolbar, "Save", save_image).pack(side="left", padx=4)

# Added shape (triangle)
extra_toolbar = tk.Frame(root, bg=PEACH_PANEL, padx=8, pady=5)
extra_toolbar.pack(pady=(0, 5))

make_button(extra_toolbar, "Triangle",
            lambda: set_tool("triangle")).pack(side="left", padx=4)

tk.Checkbutton(extra_toolbar, text="Fill Shapes", variable=fill_shapes,
               bg=PEACH_PANEL, fg=TEXT_COLOR,
               activebackground=PEACH_PANEL,
               selectcolor=PEACH_BUTTON,
               font=FONT_MAIN).pack(side="left", padx=4)

make_button(extra_toolbar, "Undo", undo).pack(side="left", padx=4)

tk.Label(extra_toolbar, text="Quick Colors:",
         bg=PEACH_PANEL, fg=TEXT_COLOR,
         font=FONT_MAIN).pack(side="left", padx=4)

quick_colors = [
    ("Black", "black", "white"),
    ("Red", "red", "white"),
    ("Blue", "blue", "white"),
    ("Green", "green", "white"),
    ("Yellow", "yellow", "black"),
    ("Purple", "purple", "white")
]

for color_name, color_code, text_color in quick_colors:
    tk.Button(
        extra_toolbar,
        text=color_name,
        command=lambda chosen_color=color_code: set_quick_color(chosen_color),
        bg=color_code,
        fg=text_color,
        activebackground=color_code,
        font=FONT_MAIN,
        relief="flat",
        padx=8,
        pady=4,
        cursor="hand2"
    ).pack(side="left", padx=3)

canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw_motion)
canvas.bind("<ButtonRelease-1>", finish_drawing)

# 11. RUN THE APPLICATION
root.mainloop()
