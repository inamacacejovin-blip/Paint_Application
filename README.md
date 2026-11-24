# README.md file

# REQUIREMENTS COMPLETED:

✓ **Bigger brush range**

What I did here, ma'am, was change the brush-size slider. Originally, the maximum brush size was only 30. I increased it to 100 so the user can draw with thicker lines.

**Code:**

![image alt](https://github.com/inamacacejovin-blip/Paint_Application/blob/main/Bigger_brush_range.png?raw=true)

To change the range, I simply changed `to=30` to `to=100`. The minimum size remains 1.

---

✓ **Undo button**

I added an Undo button so the user can reverse the most recent drawing action. Before drawing, the program saves a copy of the current image. When Undo is clicked, the previous image is restored.

**Code:**

![image alt](https://github.com/inamacacejovin-blip/Paint_Application/blob/main/Undo%20button.png?raw=true)

---

✓ **Filled shapes**

I added a Fill Shapes checkbox. When the checkbox is selected, rectangles and ovals are filled with the currently selected color. When it is not selected, the shapes remain outlines.

**Code:**

![image](https://github.com/inamacacejovin-blip/Paint_Application/blob/main/Filled_shapes.png?raw=true)

I used the same fill setting for the rectangle, oval and the additional triangle shape.

---

✓ **Extra shape tool: Triangle**

I added a Triangle button alongside the original drawing tools. The user can click and drag on the canvas to create a triangle. A preview appears while dragging, and the final triangle is drawn when the mouse button is released. (same to all shapes)

**Code:**

![image alt](https://github.com/inamacacejovin-blip/Paint_Application/blob/main/Addedshape(Triangle).png?raw=true)

I added the triangle to the shape preview function as well, so the user can see its size before finishing the drawing.

---

✓ **Confirm before clearing**

I modified the original Clear function. Instead of immediately deleting the drawing, the program now asks the user to confirm the action. If the user selects Yes, the canvas is cleared. If the user selects No, the drawing stays on the canvas.

**Code:**

![image alt](https://github.com/inamacacejovin-blip/Paint_Application/blob/main/Confirm_before_clearing.png?raw=true)

This also saves the previous canvas before clearing, so the user can use Undo to restore it.

---

✓ **Quick colors**

I added six quick-color buttons so the user does not need to open the color chooser every time they want to change colors. The buttons are Black, Red, Blue, Green, Yellow, and Purple.

**Code:**

![image](https://github.com/inamacacejovin-blip/Paint_Application/blob/main/Quick_colors.png?raw=true)

Each button calls `set_quick_color()` with its own color. The original Choose Color button is still available for selecting a custom color.

---

✓ **Green and white user interface**

I changed the original peach color palette to a green-and-white theme. The window background is light green, the toolbar panels are white, the buttons are soft green, and the text is dark green.

**Code:**

![image](https://github.com/inamacacejovin-blip/Paint_Application/blob/main/UI%20(Green%20and%20white).png?raw=true)

The existing color variable names were retained to avoid changing the original code structure. Only their color values were changed.

---

# ORIGINAL BUTTONS RETAINED

I kept all the buttons from the original program:

- Choose Color
- Brush
- Eraser
- Line
- Rectangle
- Oval
- Brush Size
- Clear
- Open
- Save

The new Triangle, Fill Shapes, Undo, and Quick Colors controls were added without removing the original buttons.


# SCREENSHOT

After running the program, take a screenshot showing the complete application window, including the canvas and both toolbar rows. On Windows, press **Win + Shift + S** to capture the screen.
