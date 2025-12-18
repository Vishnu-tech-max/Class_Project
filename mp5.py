# Science and Games Hub
import tkinter as tk #For the gui, windows and textbar,
from tkinter import scrolledtext#Text with scroll bar
import random#Generates random numbers
import numpy as np#For arrays and numbers in the black hole simiulation
import matplotlib.pyplot as plt#For the graphs and simulations
from PIL import Image, ImageTk#For the display of, and  working with images
import csv#To access the codon data in a csv file
import os#works with file paths and folders


# Config: Update these paths

IMAGEFOLDER = "aminoacids"  # folder containing amino acid PNGs
CSVFILE = "codon_table.csv"  # CSV with columns codon, amino_acid


# 1 Codon Lookup Window

def start_codon_lookup():
    codon_win = tk.Toplevel()
    codon_win.title("Codon Lookup with Image")
    codon_win.geometry("400x500")

    def get_amino_acid(event=None):
        codon = entry.get().upper()
        aminoacid = None

        # Read CSV and find amino acid
        try:
            with open(CSVFILE, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row["codon"].upper() == codon:
                        aminoacid = row["amino_acid"]
                        break
        except Exception as e:
            output_label.config(text=f"CSV Error: {e}")
            return

        # Display amino acid text
        if aminoacid:
            output_label.config(text=f"Amino Acid: {aminoacid}")

            # Try loading the image
            image_path = os.path.join(IMAGEFOLDER, f"{aminoacid}.png")
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((300, int(img.height * (300 / img.width))))  # maintain aspect ratio
                photo = ImageTk.PhotoImage(img)
                image_label.config(image=photo, text="")
                image_label.image = photo  # keep reference
            else:
                image_label.config(image="", text="Image not found")
        else:
            output_label.config(text="Codon not found")
            image_label.config(image="", text="")

    # UI
    tk.Label(codon_win, text="Enter Codon (e.g., AUG):").pack(pady=5)
    entry = tk.Entry(codon_win)
    entry.pack(pady=5)
    entry.bind("<Return>", get_amino_acid)

    tk.Button(codon_win, text="Lookup", command=get_amino_acid).pack(pady=5)
    output_label = tk.Label(codon_win, text="")
    output_label.pack(pady=10)
    image_label = tk.Label(codon_win, text="")
    image_label.pack(pady=10)


# 2 Flappy Bird Game

def start_flappy():
    game = tk.Toplevel()
    game.title("Flappy Bird")
    game.geometry("400x500")
    game.resizable(False, False)

    WIDTH, HEIGHT = 400, 500
    PIPE_WIDTH, PIPE_GAP = 60, 150
    BIRD_SIZE = 30
    GRAVITY, JUMP_FORCE, SPEED = 2, -10, 4

    canvas = tk.Canvas(game, width=WIDTH, height=HEIGHT, bg="skyblue")
    canvas.pack()

    bird_x, bird_y = 80, HEIGHT // 2
    bird = canvas.create_oval(bird_x, bird_y, bird_x + BIRD_SIZE, bird_y + BIRD_SIZE, fill="yellow")
    velocity = 0
    pipes = []
    score = 0
    score_text = canvas.create_text(10, 10, anchor="nw", text="Score: 0", font=("Arial", 16, "bold"))

    def create_pipe():
        gap_top = random.randint(80, HEIGHT - 200)
        top_pipe = canvas.create_rectangle(WIDTH, 0, WIDTH + PIPE_WIDTH, gap_top, fill="green")
        bottom_pipe = canvas.create_rectangle(WIDTH, gap_top + PIPE_GAP, WIDTH + PIPE_WIDTH, HEIGHT, fill="green")
        pipes.append((top_pipe, bottom_pipe))

    create_pipe()

    def flap(event=None):
        nonlocal velocity
        velocity = JUMP_FORCE

    canvas.bind_all("<space>", flap)
    canvas.bind_all("<Up>", flap)

    def game_over():
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text=f"GAME OVER!\nScore: {score}", fill="red", font=("Arial", 26, "bold"))
        canvas.unbind_all("<space>")
        canvas.unbind_all("<Up>")

    def update():
        nonlocal velocity, score
        velocity += GRAVITY
        canvas.move(bird, 0, velocity)

        bx1, by1, bx2, by2 = canvas.coords(bird)
        if by1 <= 0 or by2 >= HEIGHT:
            return game_over()

        for top, bottom in pipes:
            canvas.move(top, -SPEED, 0)
            canvas.move(bottom, -SPEED, 0)

        for top, bottom in pipes:
            tx1, ty1, tx2, ty2 = canvas.coords(top)
            bx1, by1, bx2, by2 = canvas.coords(bird)
            bottom_y1 = canvas.coords(bottom)[1]

            if (bx2 > tx1 and bx1 < tx2) and (by1 < ty2 or by2 > bottom_y1):
                return game_over()

            if tx2 < bird_x and "scored" not in canvas.gettags(top):
                score += 1
                canvas.itemconfig(score_text, text=f"Score: {score}")
                canvas.addtag_withtag("scored", top)

        for top, bottom in pipes.copy():
            tx1, ty1, tx2, ty2 = canvas.coords(top)
            if tx2 < 0:
                canvas.delete(top)
                canvas.delete(bottom)
                pipes.remove((top, bottom))
                create_pipe()

        game.after(30, update)

    update()


# 3 3D Black Hole Simulation

def start_blackhole():
    G, M, dt, steps = 1.0, 4000.0, 0.002, 5000
    r_s = 2 * G * M
    num_particles = 3000
    r_min, r_max = r_s*3, r_s*25

    r = np.random.uniform(r_min, r_max, num_particles)
    theta = np.random.uniform(0, 2*np.pi, num_particles)
    tilt = np.radians(25)
    #COnverting the polar co ordinates to 3D space.
    x = r * np.cos(theta)
    y = r * np.sin(theta) * np.cos(tilt)
    z = r * np.sin(theta) * np.sin(tilt)
    v = np.sqrt(G*M/r)
    vx = -v*np.sin(theta)
    vy = v*np.cos(theta)*np.cos(tilt)
    vz = v*np.cos(theta)*np.sin(tilt)

    blackhole_win = tk.Toplevel()#Creates a new window/daughter window(Blackhole window)
    blackhole_win.title("3D Black Hole Simulation")

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')#For the 3d projection
    ax.set_facecolor("black")

    u = np.linspace(0, 2*np.pi, 50)
    v_sph = np.linspace(0, np.pi, 50)
    bh_x = r_s*np.outer(np.cos(u), np.sin(v_sph))
    bh_y = r_s*np.outer(np.sin(u), np.sin(v_sph))
    bh_z = r_s*np.outer(np.ones_like(u), np.cos(v_sph))
    ax.plot_surface(bh_x, bh_y, bh_z, color="black", zorder=10)#For the drawing of the sphere
    #Setting the limits for the simulation
    scatter = ax.scatter(x, y, z, s=2)
    ax.set_xlim(-r_max, r_max)
    ax.set_ylim(-r_max, r_max)
    ax.set_zlim(-r_max, r_max)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_title("3D Interstellar-Style Black Hole", color="white")

    plt.ion()
    plt.show(block=False)
    #Setting the parameters for the visualisation of the black hole(Ex:The color,size etc)
    #Drawing the orbiting particles
    for step in range(steps):
        dist = np.sqrt(x**2 + y**2 + z**2)
        mask = dist > r_s
        x, y, z = x[mask], y[mask], z[mask]
        vx, vy, vz = vx[mask], vy[mask], vz[mask]
        #Nature of particles near the blackhole, the behaviour, the velocities and the distance of closest approach
        #The radius of the acretion disc
        ax_r = -G*M*x / dist[mask]**3
        ay_r = -G*M*y / dist[mask]**3
        az_r = -G*M*z / dist[mask]**3

        vx += ax_r*dt
        vy += ay_r*dt
        vz += az_r*dt

        x += vx*dt
        y += vy*dt
        z += vz*dt

        speed = np.sqrt(vx**2 + vy**2 + vz**2)
        heat = np.clip(speed / np.nanmax(speed), 0, 1)
        colors = np.zeros((len(heat), 3))
        colors[:,0] = heat
        colors[:,1] = 0.4 + 0.6*heat
        colors[:,2] = 0.1 + 0.3*heat
        glow = 0.3*np.exp(-((dist[mask]-r_s*1.2)/(r_s*0.3))**2)
        colors += glow[:,None]
        colors = np.clip(colors,0,1)

        scatter._offsets3d = (x, y, z)
        scatter.set_color(colors)
        plt.pause(0.001)

    plt.ioff()
    plt.show()


# 4️ Chatbot / Movies Backend

def get_top_movies():
    movies = [
        {"Title": "Dune: Part Two", "Rating": "9.0/10", "Genre": "Sci-Fi"},
        {"Title": "Oppenheimer", "Rating": "8.8/10", "Genre": "Biography/Drama"},
        {"Title": "Poor Things", "Rating": "8.4/10", "Genre": "Fantasy/Comedy"},
        {"Title": "Interstellar", "Rating": "9.0/10", "Genre": "Sci-Fi"},
        {"Title": "Inception", "Rating": "9.0/10", "Genre": "Sci-Fi"},
        {"Title": "The Dark Knight", "Rating": "9.0/10", "Genre": "Actin"}
    ]
    output = "\ Top-Rated Movies\n" + "-"*37 + "\n"
    for m in movies:
        output += f"{m['Title']} — {m['Rating']} — {m['Genre']}\n"
    output += "-"*37 + "\n"
    return output




# 5 Main GUI

def create_gui():
    window = tk.Tk()
    window.title("Science & Games Hub")
    window.geometry("700x550")

    output_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
    output_box.pack(pady=10)#Adds the vertical spacing
    #For the input from the user
    user_input = tk.Entry(window, width=60, font=("Arial", 12))
    user_input.pack(pady=5)

    def show_movies():
        output_box.insert(tk.END, get_top_movies() + "\n")
        output_box.see(tk.END)
    
    def quit_app():
        window.destroy()

    # Buttons: 2 rows
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Flappy Bird", width=15, command=start_flappy).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Black Hole", width=15, command=start_blackhole).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(btn_frame, text="Codon Lookup", width=15, command=start_codon_lookup).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(btn_frame, text="Movies", width=15, command=show_movies).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Quit", width=15, command=quit_app).grid(row=1, column=1, padx=5, pady=5)

    window.mainloop()


# Run the Hub
create_gui()
