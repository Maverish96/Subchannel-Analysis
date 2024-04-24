from tkinter import messagebox
import os, warnings
import customtkinter as ctk
import tkinter as tk
from CTkTable import CTkTable
import pandas as pd
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


warnings.simplefilter(action='ignore', category=FutureWarning)

def plotting(LOCATION, Axial_length):
    # Define the DIRECtory
    DIREC = os.path.dirname(os.path.abspath(__file__))

    def on_close():
        if messagebox.askyesno("Confirmation", "Are you sure you want to close the application?", parent=win):
            win.quit()
            win.destroy()
            
    # Creating the main tkinter window
    win = tk.Tk()
    win.iconbitmap(DIREC + r"\images\favicon.ico")
    win.title(LOCATION[1:])
    win.protocol("WM_DELETE_WINDOW", on_close)
    win.geometry("+0+0")
    win.resizable(0, 0)
    
    # DATA
    scaling = 0.95
    w, h = win.winfo_screenwidth(), win.winfo_screenheight()
    screen_width = int(w*scaling)
    screen_height = int(h*scaling)
    
    light_col2 = "#494949"
    light_col3 = "#383838"
    light_col = "#2c2c2c"
    dark_col = "#202020"
    button_fg = "#005c4b"
    button_hover = "#1daa61"
    font_type = "Inter"
    width_size = screen_width
    height_size = (screen_height/16)
    padding = 10
    win.configure(bg=dark_col)

    # Function to draw the table when the subchannel is selected
    oldChannel = [r"\Subchannel Data\Channel 1.csv"]
    def drawTable():
        try:
            step = int(stepValue.get())
            if step == 0:
                raise ValueError
            df = pd.read_csv(DIREC+LOCATION+selectedChannel.get())
            
            nonlocal table, table_frame
            table_frame.destroy()
            table_frame = ctk.CTkScrollableFrame(frame2, width=(3/8)*width_size-padding, height=10*height_size, fg_color=light_col3, bg_color=light_col3, corner_radius=0)
            table_frame.grid(row=1, column=0, columnspan=3)
            table.destroy()
            table_data = [list(df.columns[:4])] + df.iloc[::step,:4].values.tolist() + [""]
            table = CTkTable(table_frame, values=table_data, width=(2/7)*(3/8)*width_size-0.7*padding, height=0.6*height_size, font=("Arial Bold", table_body_font), justify="left", anchor="w", colors=["#454545", "#515151"], header_color=dark_col, hover_color=light_col3)
            table.grid(row=0, column=0, padx=padding, pady=padding)
            table.edit_column(0, width=(1/7)*(3/8)*width_size-0.7*padding, anchor="w")
            table.edit_row(0, font=(font_type, table_head_font, "bold"), anchor="c")
            oldChannel[0] = selectedChannel.get()
            try:    
                pressure_plot()
            except:
                return
        except:
            selectedChannel.set(oldChannel[0])
            messagebox.showerror("Error!", "Please enter a valid Step Value!")

    # PLOTS
    def pressure_plot():
        fig, ax = plt.subplots()
        fig.set_size_inches(((4/8)*width_size-5.5*padding) / 96, (height_size*11-4.6*padding) / 96)  # Convert pixels to inches (96 pixels per inch)
        df = pd.read_csv(DIREC + LOCATION + selectedChannel.get())
        Pressure = df["Pressure"].tolist()
        ax.plot(Axial_length, Pressure, marker='.', label="Pressure")
        ax.legend()
        ax.grid(True)
        ax.set_title(selectedChannel.get())
        ax.set_xlabel("Axial Length")
        ax.set_ylabel("Pressure")
        
        # Clear previous plot
        for widget in frame3.winfo_children():
            widget.destroy()
        
        # Plot Embedding with padding
        canvas = FigureCanvasTkAgg(fig, master=frame3)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=padding, pady=padding)
        
        # Toolbar Embedding
        toolbar1 = NavigationToolbar2Tk(canvas, frame3)
        toolbar1.update()
        toolbar1.pack(side=tk.BOTTOM, fill=tk.X, padx=padding, pady=padding)

    def enthalpy_plot():
        fig, ax = plt.subplots()
        fig.set_size_inches(((4/8)*width_size-5.5*padding) / 96, (height_size*11-4.6*padding) / 96)  # Convert pixels to inches (96 pixels per inch)
        df = pd.read_csv(DIREC + LOCATION + selectedChannel.get())
        Enthalpy = df["Enthalpy"].tolist()
        ax.plot(Axial_length, Enthalpy, marker='.', label="Enthalpy")
        ax.legend()
        ax.grid(True)
        ax.set_title(selectedChannel.get())
        ax.set_xlabel("Axial Length")
        ax.set_ylabel("Enthalpy")
        
        # Clear previous plot
        for widget in frame3.winfo_children():
            widget.destroy()
        
        # Plot Embedding with padding
        canvas = FigureCanvasTkAgg(fig, master=frame3)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=padding, pady=padding)
        
        # Toolbar Embedding
        toolbar1 = NavigationToolbar2Tk(canvas, frame3)
        toolbar1.update()
        toolbar1.pack(side=tk.BOTTOM, fill=tk.X, padx=padding, pady=padding)

    def massflowrate_plot():
        fig, ax = plt.subplots()
        fig.set_size_inches(((4/8)*width_size-5.5*padding) / 96, (height_size*11-4.6*padding) / 96)  # Convert pixels to inches (96 pixels per inch)
        df = pd.read_csv(DIREC + LOCATION + selectedChannel.get())
        MassFlowRate = df["Mass Flow Rate"].tolist()
        ax.plot(Axial_length, MassFlowRate, marker='.', label="Mass Flow Rate")
        ax.legend()
        ax.grid(True)
        ax.set_title(selectedChannel.get())
        ax.set_xlabel("Axial Length")
        ax.set_ylabel("Mass Flow Rate")
        
        # Clear previous plot
        for widget in frame3.winfo_children():
            widget.destroy()
        
        # Plot Embedding with padding
        canvas = FigureCanvasTkAgg(fig, master=frame3)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=padding, pady=padding)
        
        # Toolbar Embedding
        toolbar1 = NavigationToolbar2Tk(canvas, frame3)
        toolbar1.update()
        toolbar1.pack(side=tk.BOTTOM, fill=tk.X, padx=padding, pady=padding)

    # Creating the main frame
    frame0 = ctk.CTkFrame(win, fg_color=dark_col, bg_color=dark_col, corner_radius=0)
    frame0.grid(row=0, column=0, columnspan=3)
    frame1 = ctk.CTkScrollableFrame(win, width=(1/8)*width_size, height=height_size*12, fg_color=light_col, bg_color=light_col, corner_radius=0)
    frame1.grid(row=1, column=0)
    frame2 = ctk.CTkFrame(win, width=(3/8)*width_size, height=height_size*12, fg_color=light_col3, bg_color=light_col3, corner_radius=0)
    frame2.grid(row=1, column=1)
    frame3 = ctk.CTkFrame(win, width=(4/8)*width_size, height=height_size*12, fg_color=light_col2, bg_color=light_col2, corner_radius=0)
    frame3.grid(row=1, column=2)

    # HEADING label
    head_label = ctk.CTkLabel(frame0, width=width_size - 4*padding, height=height_size*2, text="".join(LOCATION[1:].replace('_', ' ')), font=(font_type, height_size, "bold"), bg_color=dark_col, fg_color=dark_col, anchor="w")
    head_label.grid(row=0, column=0, padx=2*padding, pady=2*padding)

    NCHANL = int(LOCATION[1:].replace('_', ' ').split()[1])

    radioButtons = []
    selectedChannel = ctk.StringVar(value="None")
    for i in range(NCHANL):
        rb = ctk.CTkRadioButton(frame1, fg_color=button_fg, hover_color=button_hover, radiobutton_width=height_size/1.6-2*padding, radiobutton_height=height_size/1.6-2*padding, width=(1/8)*width_size, height=height_size/1.4, font=(font_type, height_size/1.6-2*padding), text=f" Subchannel {i+1}", value=fr"\Subchannel Data\Channel {i+1}.csv", variable=selectedChannel, command=drawTable)
        rb.grid(row=i, column=0, padx=padding*2)
        radioButtons.append(rb)
    selectedChannel.set(r"\Subchannel Data\Channel 1.csv")

    # BUTTONS
    button_font_size = height_size/3
    
    pressure_button = ctk.CTkButton(frame2, width=(1/3)*(3/8)*width_size - 1.6*padding, height=height_size-2*padding, text="Pressure Plot", command=pressure_plot, font=(font_type, button_font_size, "bold"), hover_color=button_hover, bg_color=light_col3, fg_color=button_fg, anchor="w")
    pressure_button.grid(row=0, column=0, padx=padding, pady=padding)

    enthalpy_button = ctk.CTkButton(frame2, width=(1/3)*(3/8)*width_size - 1.6*padding, height=height_size-2*padding, text="Enthalpy Plot", command=enthalpy_plot, font=(font_type, button_font_size, "bold"), hover_color=button_hover, bg_color=light_col3, fg_color=button_fg, anchor="w")
    enthalpy_button.grid(row=0, column=1, padx=padding, pady=padding)

    massflowrate_button = ctk.CTkButton(frame2, width=(1/3)*(3/8)*width_size - 1.6*padding, height=height_size-2*padding, text="Mass Flow Rate Plot", command=massflowrate_plot, font=(font_type, button_font_size, "bold"), hover_color=button_hover, bg_color=light_col3, fg_color=button_fg, anchor="w")
    massflowrate_button.grid(row=0, column=2, padx=padding, pady=padding)

    # TABLE For Excel
    df = pd.read_csv(DIREC+LOCATION+selectedChannel.get())
    table_data = [list(df.columns[:4])] + df.iloc[::1,:4].values.tolist() + [""]
    
    table_head_font = (3/12)*height_size
    table_body_font = (3/12)*height_size

    table_frame = ctk.CTkScrollableFrame(frame2, width=(3/8)*width_size-padding, height=10*height_size, fg_color=light_col3, bg_color=light_col3, corner_radius=0)
    table_frame.grid(row=1, column=0, columnspan=3)
    table = CTkTable(table_frame, values=table_data, width=(2/7)*(3/8)*width_size-0.7*padding, height=0.6*height_size, font=("Arial Bold", table_body_font), justify="left", anchor="w", colors=["#454545", "#515151"], header_color=dark_col, hover_color=light_col3)
    table.grid(row=0, column=0, padx=padding, pady=padding)
    table.edit_column(0, width=(1/7)*(3/8)*width_size-0.7*padding, anchor="w")
    table.edit_row(0, font=(font_type, table_head_font, "bold"), anchor="c")

    # Default plot
    pressure_plot()

    # Creating a step value for NODE display for subchannel
    stepLabel = ctk.CTkLabel(frame2, width=(2/7)*(3/8)*width_size-0.7*padding, height=height_size-2*padding, text="Step Value:", font=(font_type, 1.5*button_font_size))
    stepLabel.grid(row=2, column=0, padx=padding, pady=padding, sticky='w')
    stepValue = ctk.CTkEntry(frame2, width=(2/7)*(3/8)*width_size-0.7*padding, height=height_size-2*padding, font=(font_type, button_font_size))
    stepValue.grid(row=2, column=1, padx=padding, pady=padding, sticky='w')
    stepValue.insert(0, "1")
   
    win.mainloop()

# DEBUG
#LOCATION = r"\RESULTS_14_Channels_100_Nodes"
#plotting(LOCATION, [(0.1/99)*i for i in range(100)])