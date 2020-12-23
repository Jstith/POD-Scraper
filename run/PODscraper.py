# Imports tkinter and references local script
import tkinter as tk
import seleniumScraper as ss

# Function that runs when the button is pressed
def click():

    # Disables button while information is being gathered
    scrapeButton.config(state='disabled')

    # Gets data from seleniumScraper and dispalys it
    data = ss.getWeather()
    infoText.config(state='normal')
    infoText.delete('1.0', tk.END)
    infoText.insert('end-1c', data)

    data = ss.getDuty()
    infoText.insert('end-1c', data)

    data = ss.getUOD()
    infoText.insert('end-1c', data)

    infoText.config(state='disabled')

    # Re-enables the button
    scrapeButton.config(state='normal')

# Hard coded defaults for height and width
# ALl elements are placed in frames so they all scale
HEIGHT = 600
WIDTH = 700

# Master window
root = tk.Tk()
root.title('Plan Of The Day Web Scraper')

# Canvas for initial size
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# Frames for format and color
backgroundTopFrame = tk.Frame(root, bg='#303F9F')
backgroundTopFrame.place(relx=0, rely=0, relwidth=1, relheight=0.05)

backgroundMainFrame = tk.Frame(root, bg='#3F51B5')
backgroundMainFrame.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

# Frame for content
contentTopFrame = tk.Frame(root, bg='#3F51B5')
contentTopFrame.place(relx=0.5, rely=0.1, relwidth=0.85, relheight=0.25, anchor='n')

# Content for top frame
mainLabel = tk.Label(contentTopFrame, text='POD Web Scraper', font=('Arial', '16'), fg='#FFFFFF', bg='#3F51B5')
mainLabel.grid(row=0, column=0, sticky='W')

creditLabel = tk.Label(contentTopFrame, text='By: Joram Stith', font=('Arial', '10'), fg='#FFFFFF', bg='#3F51B5')
creditLabel.grid(row=1, column=0, sticky='W')

scrapeButton = tk.Button(contentTopFrame, text='Scrape POD Info', font=('Arial', '10'), fg='#212121', bg='#9E9E9E', command=click)
scrapeButton.grid(row=2, column=0, sticky='W', pady=15)

# Frame for content
contentBottomFrame = tk.Frame(root, bg='#C5CAE9')
contentBottomFrame.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)

# Content for bottom frame
infoText = tk.Text(contentBottomFrame, state='disabled', fg='#212121', bg='#9E9E9E')
infoText.place(relx=0.1, rely=0.1, relwidth=0.8, relheigh=0.8)

# Runs GUI
root.mainloop()
