import customtkinter as ctk
import tkinter as tk


def ask_string(query):
    def ret(event=None):  # The parameter is needed for bind.
        result[0] = query_input.get()
        popup.destroy()

    result = [None]  # Use a mutable object to store the result.
    popup = ctk.CTk()
    popup.title(query)
    popup.geometry("300x150")
    query_label = ctk.CTkLabel(master=popup, text=f"Enter {query}:")
    query_label.pack(pady=5, side="top")

    query_input = ctk.CTkEntry(master=popup, placeholder_text=query)
    query_input.pack(pady=5, side="top")
    query_input.bind("<Return>", ret)  # Bind the Enter key.

    query_return = ctk.CTkButton(master=popup, text="Enter", command=ret)
    query_return.pack(pady=5, side="top")

    popup.mainloop()
    return result[0]  # Return the result.


def check_case_insensitive(variable, my_list):
    variable_lower = variable.lower()
    list_lower = [item.lower() for item in my_list]
    return variable_lower in list_lower


def ask_strings(queries, title):
    def ret(event=None):  # The parameter is needed for bind.
        print(f"Return event called with {event}")
        for i, query in enumerate(queries):
            results[i] = inputs[i].get()
        popup.destroy()

    results = [None] * len(queries)  # Use a mutable object to store the results.
    inputs = []
    popup = ctk.CTk()
    popup.title(title)
    popup.geometry("300x150")

    query_label = ctk.CTkLabel(master=popup, text="Enter info:")
    query_label.pack(pady=5, side="top")

    for query in queries:
        query_input = ctk.CTkEntry(master=popup, placeholder_text=query)
        query_input.pack(pady=5, side="top")
        query_input.bind("<Return>", ret)  # Bind the Enter key.
        inputs.append(query_input)

    query_return = ctk.CTkButton(master=popup, text="Enter", command=ret)
    query_return.pack(pady=5, side="top")

    popup.mainloop()
    return results


def info_popup(popup_type: str, title="CTKDialogue Popup", text="CTKDialogue Error Text", code=1, do_exit=False,
               close="Exit", width=300, height=100, font_family="Arial"):
    if not check_case_insensitive(popup_type, ["textOnly", "imageOnly", "textAndImage"]):
        raise ValueError(f"Argument {popup_type} is not a valid type, expected 'textOnly', 'imageOnly',"
                         f" 'textAndImage'. (Not case sensitive)")

    popup_root = ctk.CTk()
    popup_root.geometry(f"{width}x{height}")
    popup_root.title(title)

    # Make the window not resizable
    popup_root.resizable(False, True)

    def leave(event=None):
        popup_root.destroy()
        if do_exit:
            exit(code)

    popup_root.bind("<Return>", leave)

    # Configure the label to display text on the left and wrap around
    error_text = ctk.CTkLabel(master=popup_root, text=text, text_color="#ffffff", anchor="w", justify="left",
                              wraplength=int(width*0.9333333333333333), font=(font_family, 12))
    error_text.pack(pady=40, side="top")

    exit_button = ctk.CTkButton(master=popup_root, text=close, command=leave)
    exit_button.pack(pady=0, side="top")

    popup_root.mainloop()

    return popup_root


def create_popup(title, placeholders):
    def on_submit():
        # Retrieve the input data and set it to the StringVar
        for i, entry_var in enumerate(entry_vars):
            input_data[i] = entry_var.get()

        # Close the popup window
        root.destroy()

    # Create the main window
    root = tk.Tk()
    root.title(title)

    # Create entry fields with placeholder text
    entry_vars = []
    input_data = [None] * len(placeholders)
    for i, placeholder in enumerate(placeholders):
        entry_var = tk.StringVar()
        entry_var.set(placeholder)
        entry = tk.Entry(root, textvariable=entry_var)
        entry.pack(pady=5)
        entry_vars.append(entry_var)

    # Create a button to submit the inputs
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    # Run the main loop to display the window
    root.mainloop()

    # Return the input data after the window is closed
    return input_data
