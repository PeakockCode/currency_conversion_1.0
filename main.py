import os
from dotenv import load_dotenv
from tkinter import *
import customtkinter
import requests


load_dotenv(override=True)

# fonts
main_font = ("Verdana", 10)

# main window (size, title, icon, background)
root = customtkinter.CTk()
root.geometry("400x220+750+350")
root.resizable(False, False)
root.configure(fg_color="#202D40")
root.title("Currency conversion")
root.iconbitmap("icons/icon.ico")
customtkinter.set_appearance_mode("dark")


# currency convert function
def convert_currency():
    notification_label.configure(text="")
    result_label.configure(text="0")
    try:
        currency_from = drop_down_from.get()
        currency_to = drop_down_to.get()
        amount = float(user_input.get().replace(",", "."))
        apikey = os.getenv("FREE_CURRENCY_API_KEY")
        url = (f"https://api.freecurrencyapi.com/v1/latest?apikey={apikey}&"
               f"currencies={currency_to}&base_currency={currency_from}")
        response = requests.request("GET", url)
        data_result = response.json()
        final_result = amount*data_result["data"][currency_to]
        result_label.configure(text=round(final_result, 2))
    except ValueError:
        notification_label.configure(text="Insert valid amount to convert")
    except requests.exceptions.RequestException:
        notification_label.configure(text="Error communicating, try again.")


# frames
input_frame = customtkinter.CTkFrame(root, fg_color="#202D40")
input_frame.pack(padx=5, pady=5)
buttons_frame = customtkinter.CTkFrame(root, fg_color="#202D40")
buttons_frame.pack(padx=5, pady=5)

# user input
user_input = customtkinter.CTkEntry(input_frame, width=200, font=main_font,
                                    placeholder_text="Insert amount", justify=CENTER)
user_input.grid(row=0, column=0, pady=10)

# drop down menu - from currency
drop_down_from = customtkinter.StringVar(value="CZK")
drop_down_from_option = customtkinter.CTkOptionMenu(input_frame,
                                                    values=["CZK", "USD", "EUR", "CAD",
                                                            "CHF", "GBP", "PLN", "NZD", "JPY"],
                                                    variable=drop_down_from)
drop_down_from_option.grid(row=0, column=1, padx=(0, 10), pady=10)

# drop down menu - to currency
drop_down_to = customtkinter.StringVar(value="CZK")
drop_down_to_option = customtkinter.CTkOptionMenu(input_frame,
                                                  values=["CZK", "USD", "EUR",
                                                          "CAD", "CHF", "GBP", "PLN", "NZD", "JPY"],
                                                  variable=drop_down_to)
drop_down_to_option.grid(row=1, column=1, padx=(0, 10), pady=10)

# result label
result_label = customtkinter.CTkLabel(input_frame, text="0", font=main_font)
result_label.grid(row=1, column=0, padx=10, pady=10)

# note label
notification_label = customtkinter.CTkLabel(input_frame, text="", font=main_font, width=200,
                                            fg_color="transparent")
notification_label.grid(row=2, column=0, padx=10, pady=10)

# convert button
convert_button = customtkinter.CTkButton(buttons_frame, text="Convert", width=100, height=30, border_width=1,
                                         font=main_font, command=convert_currency)
convert_button.grid(row=0, column=0, padx=10, pady=10)

# quit button
quit_button = customtkinter.CTkButton(buttons_frame, text="Quit", width=100, height=30, border_width=1,
                                      font=main_font, command=root.destroy)
quit_button.grid(row=0, column=1, padx=10, pady=10)

# main loop
root.mainloop()
