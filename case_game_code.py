import tkinter as tk
import random

# ДАННЫЕ
coins = 500
inventory = []
selected_item = None
spinning = False

CASE_PRICE = 100

# ПРЕДМЕТЫ
items_by_rarity = {
    "Обычный": [
        "Glock-18 | Sand Dune",
        "P250 | Boreal Forest",
        "Nova | Candy Apple"
    ],
    "Редкий": [
        "AK-47 | Elite Build",
        "M4A1-S | Decimator",
        "USP-S | Cortex"
    ],
    "Эпический": [
        "AK-47 | Redline",
        "AWP | Fever Dream",
        "Desert Eagle | Kumicho Dragon"
    ],
    "Легендарный": [
        "AWP | Dragon Lore",
        "Karambit | Fade",
        "M4A4 | Howl"
    ]
}

rarities = list(items_by_rarity.keys())
weights = [60, 25, 10, 5]

def random_item():
    rarity = random.choices(rarities, weights=weights)[0]
    name = random.choice(items_by_rarity[rarity])
    return {"name": name, "rarity": rarity}


current = [random_item() for _ in range(7)]

# ЦЕНЫ
sell_price = {
    "Обычный": 40,
    "Редкий": 90,
    "Эпический": 250,
    "Легендарный": 500
}

# ЦВЕТА
def color(rarity):
    if rarity == "Легендарный":
        return "#FFD700"
    elif rarity == "Эпический":
        return "#a020f0"
    elif rarity == "Редкий":
        return "#3399ff"
    return "#777777"


# ОКНО
root = tk.Tk()
root.title("Case Simulator_text.version")
root.geometry("700x500")
root.configure(bg="#1e1e1e")

# ПАНЕЛЬ
top = tk.Frame(root, bg="#2b2b2b")
top.pack(fill="x")

coins_label = tk.Label(
    top,
    text=f"Монеты: {coins}",
    fg="white",
    bg="#2b2b2b",
    font=("Arial", 14, "bold")
)
coins_label.pack(pady=10)


# СМЕНА ЭКРАНОВ
def show(frame):
    menu.pack_forget()
    case.pack_forget()
    inv.pack_forget()
    frame.pack(fill="both", expand=True)


# МЕНЮ
menu = tk.Frame(root, bg="#1e1e1e")
menu.pack(fill="both", expand=True)

tk.Label(menu, text="CASE SIM",
         fg="white", bg="#1e1e1e",
         font=("Arial", 18, "bold")).pack(pady=20)

tk.Button(menu, text="Кейсы", command=lambda: show(case), width=20).pack(pady=5)
tk.Button(menu, text="Инвентарь", command=lambda: open_inv(), width=20).pack(pady=5)
tk.Button(menu, text="Выход", command=root.destroy, width=20).pack(pady=5)


# КЕЙС
case = tk.Frame(root, bg="#1e1e1e")

wheel = tk.Frame(case, bg="#1e1e1e")
wheel.pack(pady=40)

labels = []

for i in range(7):
    lbl = tk.Label(
        wheel,
        text="?",
        width=18,
        height=3,
        bg="#3c3c3c",
        fg="white",
        font=("Arial", 10, "bold")
    )
    lbl.grid(row=0, column=i, padx=3)
    labels.append(lbl)

result_label = tk.Label(case, text="Кейс", fg="white", bg="#1e1e1e")
result_label.pack()


def spin(step=0):
    global current, spinning

    current = current[1:] + [random_item()]

    for i in range(7):
        item = current[i]
        labels[i].config(
            text=item["name"],
            bg=color(item["rarity"])
        )

    if step < 20:
        delay = 50 + step * 5
        root.after(delay, spin, step + 1)
    else:
        win = current[3]
        inventory.append(win)
        result_label.config(text=f"Выпало: {win['name']}")
        spinning = False


def open_case():
    global coins, current, spinning

    if spinning:
        return

    if coins < CASE_PRICE:
        result_label.config(text="Нет монет")
        return

    coins -= CASE_PRICE
    coins_label.config(text=f"Монеты: {coins}")

    current = [random_item() for _ in range(7)]
    spinning = True
    spin(0)


tk.Button(case, text="Открыть кейс",
          command=open_case,
          width=20).pack(pady=10)

tk.Button(case, text="Назад",
          command=lambda: show(menu)).pack()


# ИНВЕНТАРЬ
inv = tk.Frame(root, bg="#1e1e1e")


def select_item(index):
    global selected_item
    selected_item = index
    item = inventory[index]
    inv_status.config(text=f"Выбрано: {item['name']}")


def sell_item():
    global coins, selected_item

    if selected_item is None:
        return

    item = inventory.pop(selected_item)
    coins += sell_price[item["rarity"]]

    coins_label.config(text=f"Монеты: {coins}")
    selected_item = None
    open_inv()


def sell_all():
    global coins

    coins += sum(sell_price[i["rarity"]] for i in inventory)
    inventory.clear()

    coins_label.config(text=f"Монеты: {coins}")
    open_inv()


def open_inv():
    global inv_status, selected_item

    selected_item = None
    show(inv)

    for w in inv.winfo_children():
        w.destroy()

    tk.Label(inv, text="ИНВЕНТАРЬ",
             fg="white", bg="#1e1e1e",
             font=("Arial", 14, "bold")).pack(pady=10)

    inv_status = tk.Label(inv, text="Ничего не выбрано",
                          fg="white", bg="#1e1e1e")
    inv_status.pack()

    grid = tk.Frame(inv, bg="#1e1e1e")
    grid.pack()

    cols = 4

    for i, item in enumerate(inventory):
        card = tk.Frame(
            grid,
            bg=color(item["rarity"]),
            width=160,
            height=60
        )
        card.grid(row=i // cols, column=i % cols, padx=5, pady=5)
        card.pack_propagate(False)

        tk.Button(
            card,
            text=item["name"],
            bg=color(item["rarity"]),
            fg="black",
            wraplength=140,
            command=lambda i=i: select_item(i)
        ).pack(expand=True, fill="both")

    # КНОПКИ
    tk.Button(inv, text="💰 Продать выбранное",
              command=sell_item).pack(pady=5)

    tk.Button(inv, text="💥 Продать всё",
              command=sell_all).pack(pady=5)

    tk.Button(inv, text="⬅ Выйти в меню",
              command=lambda: show(menu),
              bg="#222222",
              fg="white").pack(pady=10)


root.mainloop()
