import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = tk.Tk()
root.title("Database Management System")
root.configure(bg="#FFEBCD")
root.geometry("1200x750")
root.resizable(False, False)


# Fungsi untuk menghubungkan ke database dan mengambil data
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='tubes' 
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None

# Fungsi untuk menampilkan data keseluruhan
def show_all_data():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM airlinesafety")  
        records = cursor.fetchall()
        display_data(records, columns)
        cursor.close()
        conn.close()

# Fungsi untuk menampilkan data dalam Treeview
def display_data(data, columns):
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    tree = ttk.Treeview(display_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col, anchor='center')  
        tree.column(col, width=100, anchor='center')  
    
    for row in data:
        tree.insert("", "end", values=row)
    
    tree.pack(fill="both", expand=True)

# Fungsi untuk input data
def input_data():
    def save_data():
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO airlinesafety (airline, avail_seat_km_per_week, incidents_85_99, fatal_accidents_85_99, fatalities_85_99, incidents_00_14, fatal_accidents_00_14, fatalities_00_14) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (entry_airline.get(), entry_avail.get(), entry_incidents_85_99.get(), entry_fatal_85_99.get(), entry_fatalities_85_99.get(), entry_incidents_00_14.get(), entry_fatal_00_14.get(), entry_fatalities_00_14.get())
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Data inserted successfully")
            show_all_data()
    
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    labels = ["Airline", "Avail Seat Km Per Week", "Incidents 85-99", "Fatal Accidents 85-99", "Fatalities 85-99", "Incidents 00-14", "Fatal Accidents 00-14", "Fatalities 00-14"]
    entries = []

    for i, label in enumerate(labels):
        lbl = tk.Label(display_frame, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(display_frame)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    entry_airline, entry_avail, entry_incidents_85_99, entry_fatal_85_99, entry_fatalities_85_99, entry_incidents_00_14, entry_fatal_00_14, entry_fatalities_00_14 = entries
    
    btn_save = tk.Button(display_frame, text="Save Data", command=save_data, bg="lightblue", fg="black")
    btn_save.grid(row=len(labels), columnspan=2, pady=10)

# Fungsi untuk menampilkan 10 data teratas
def show_top_10():
    conn = connect_db()
    if conn:
        df = pd.read_sql("SELECT * FROM airlinesafety", conn)
        top_10 = df.head(10).values.tolist()
        display_data(top_10, columns)
        conn.close()

# Fungsi untuk menampilkan 10 data terbawah
def show_bottom_10():
    conn = connect_db()
    if conn:
        df = pd.read_sql("SELECT * FROM airlinesafety", conn)
        bottom_10 = df.tail(10).values.tolist()
        display_data(bottom_10, columns)
        conn.close()

# Fungsi untuk select data
def select_data():
    def fetch_data():
        airline = entry_airline.get()
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM airlinesafety WHERE airline = %s", (airline,))
            records = cursor.fetchall()
            display_data(records, columns)
            cursor.close()
            conn.close()
    
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    lbl = tk.Label(display_frame, text="Enter Airline")
    lbl.pack(pady=5)
    entry_airline = tk.Entry(display_frame)
    entry_airline.pack(pady=5)
    btn_fetch = tk.Button(display_frame, text="Fetch Data", command=fetch_data, bg="lightgreen", fg="black")
    btn_fetch.pack(pady=10)

# Fungsi untuk menghapus data
def delete_data():
    def remove_data():
        airline = entry_airline.get()
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM airlinesafety WHERE airline = %s", (airline,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Data deleted successfully")
            show_all_data()
    
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    lbl = tk.Label(display_frame, text="Enter Airline to Delete")
    lbl.pack(pady=5)
    entry_airline = tk.Entry(display_frame)
    entry_airline.pack(pady=5)
    btn_delete = tk.Button(display_frame, text="Delete Data", command=remove_data, bg="red", fg="white")
    btn_delete.pack(pady=10)

# Fungsi untuk update data
def update_data():
    def save_updates():
        airline = entry_airline.get()
        column = entry_column.get()
        new_value = entry_value.get()
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = f"UPDATE airlinesafety SET {column} = %s WHERE airline = %s"
            cursor.execute(query, (new_value, airline))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Data updated successfully")
            show_all_data()
    
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    lbl_airline = tk.Label(display_frame, text="Airline")
    lbl_airline.grid(row=0, column=0, padx=10, pady=5)
    entry_airline = tk.Entry(display_frame)
    entry_airline.grid(row=0, column=1, padx=10, pady=5)
    
    lbl_column = tk.Label(display_frame, text="Column")
    lbl_column.grid(row=1, column=0, padx=10, pady=5)
    entry_column = tk.Entry(display_frame)
    entry_column.grid(row=1, column=1, padx=10, pady=5)
    
    lbl_value = tk.Label(display_frame, text="New Value")
    lbl_value.grid(row=2, column=0, padx=10, pady=5)
    entry_value = tk.Entry(display_frame)
    entry_value.grid(row=2, column=1, padx=10, pady=5)
    
    btn_save = tk.Button(display_frame, text="Update Data", command=save_updates, bg="orange", fg="black")
    btn_save.grid(row=3, columnspan=2, pady=10)

# Fungsi untuk visualisasi data
def visualize_data():
    conn = connect_db()
    if conn:
        df = pd.read_sql("SELECT airline, fatal_accidents_85_99, fatal_accidents_00_14 FROM airlinesafety", conn)
        conn.close()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 5))
        
        fig.patch.set_facecolor('lightblue')  

        # Grafik 1: Fatal Accidents 85-99
        ax1.bar(df['airline'], df['fatal_accidents_85_99'], color='skyblue')
        ax1.set_title('Fatal Accidents 85-99',fontsize=10)
        ax1.set_xlabel('Airline',fontsize=1)
        ax1.set_ylabel('Fatal Accidents',fontsize=10)
        ax1.set_xticklabels(df['airline'], rotation=90)
        ax1.set_yticks(range(0, 17, 2))  # Set yticks from 0 to 16 with step 2
        ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Grafik 2: Fatal Accidents 00-14
        ax2.bar(df['airline'], df['fatal_accidents_00_14'], color='salmon')
        ax2.set_title('Fatal Accidents 00-14',fontsize=10)
        ax2.set_xlabel('Airline',fontsize=1)
        ax2.set_ylabel('Fatal Accidents',fontsize=10)
        ax2.set_xticklabels(df['airline'], rotation=90)
        ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Menyesuaikan layout
        plt.subplots_adjust(hspace=1)

        # Menampilkan grafik dalam Tkinter
        for widget in display_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)



# Frame untuk tombol di sisi kiri
button_frame = tk.Frame(root, width=200, height=500, bg="lightgrey")
button_frame.pack(side="left", fill="y")

# Frame untuk menampilkan data di sisi kanan
display_frame = tk.Frame(root, width=700, height=500, bg="#FFEBCD")
display_frame.pack(side="right", fill="both", expand=True)

# Daftar kolom
columns = ["airline", "avail_seat_km_per_week", "incidents_85_99", "fatal_accidents_85_99", "fatalities_85_99", "incidents_00_14", "fatal_accidents_00_14", "fatalities_00_14"]

# Membuat tombol di sisi kiri
buttons = [
    ("Tampilkan Data Keseluruhan", show_all_data),
    ("Input Data", input_data),
    ("10 Data Teratas", show_top_10),
    ("10 Data Terbawah", show_bottom_10),
    ("Delete Data", delete_data),
    ("Update Data", update_data),
    ("Select Data", select_data),
    ("Visualisasi Fatal Accidents", visualize_data)
]

for text, command in buttons:
    btn = tk.Button(button_frame, text=text, command=command, width=25, bg='lightblue', padx=10, pady=5)
    btn.pack(pady=20)


root.mainloop()


