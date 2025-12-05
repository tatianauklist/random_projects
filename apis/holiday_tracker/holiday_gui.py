from tkinter import *
from tkinter import ttk
from holiday_countdown import get_holidays, format_results,getCountryCode

def check_holidays():
    countryName = countryCode.get()
    y = year.get()
    print(f"Country Name: {countryName}")
    cResults = getCountryCode(countryName)
    if not cResults["success"]:
        resultsText.delete(1.0,END)
        resultsText.insert(1.0, cResults["error"])
        return
    c = cResults["data"]
    holidays = get_holidays(c,y)
    formatted = format_results(holidays)
    resultsText.delete(1.0, END)
    resultsText.insert(1.0,formatted)
root = Tk()
root.title("Holiday Countdown ⏲️")
mainframe = ttk.Frame(root,padding=15)
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
countryCode = StringVar()
year = StringVar()
ttk.Label(mainframe,text="Country Name:").grid(row=0,column=0)
countryCodeEntry = ttk.Entry(mainframe,textvariable=countryCode)
countryCodeEntry.grid(row=0,column=1)
ttk.Label(mainframe, text="Year:").grid(row=1,column=0)
yearEntry = ttk.Entry(mainframe,textvariable=year)
yearEntry.grid(row=1,column=1)

ttk.Button(mainframe,text="Get Holidays",command=check_holidays).grid(row=2,column=0,columnspan=2)
resultsText = Text(mainframe,width=100,height=15)
resultsText.grid(row=3,column=0,columnspan=2)

root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)
for child in mainframe.winfo_children():
    child.grid_configure(padx=15,pady=15)
countryCodeEntry.focus()
root.bind("<Return>",lambda event: check_holidays())
root.mainloop()
