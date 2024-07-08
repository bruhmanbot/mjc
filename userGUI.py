import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from MJCounter import mj_scorecount


def enter_tile(tileNo: int):
    global OutsideTileCount, InsideTileCount, WinningTileCount, OutsideTileList, InsideTileList, WinningTile
    # Get column from num of tiles present

    match target_entry:
        case "Outer":
            if OutsideTileCount < 15:
                row = 2
                col = OutsideTileCount
                OutsideTileCount += 1
                OutsideTileList.append(tileNo)
            else:
                tkinter.messagebox.showinfo(title="Too many tiles!", message="Too many tiles!")
                return
        case "Winning":
            if WinningTileCount < 1:
                row = 6
                col = WinningTileCount
                WinningTileCount += 1
                WinningTile.append(tileNo)
            else:
                tkinter.messagebox.showinfo(title="Too many tiles!", message="Too many tiles!")
                return
        case "Inner":
            if InsideTileCount < 16:
                row = 4
                col = InsideTileCount
                InsideTileCount += 1
                InsideTileList.append(tileNo)
            else:
                tkinter.messagebox.showinfo(title="Too many tiles!", message="Too many tiles!")
                return
        case _:
            return
    # Path of image
    path_cmd = f'mahjong_tile_images/{tileNo}.png'
    # display image
    image_temp = Image.open(path_cmd)
    resize_img_temp = image_temp.resize((60, 72))
    image_temp = ImageTk.PhotoImage(resize_img_temp)
    ttk.Label(frame, image=image_temp).grid(column=col, row=row)
    ttk.Label(frame, image=image_temp).image = image_temp


def direction_conversion(direction):
    match direction:
        case "South":
            return 2
        case "West":
            return 3
        case "North":
            return 4
        case _:  # Includes east as well
            return 1


def ResetWinningTile(RowTileCount, RowNo):
    # RowTileCount is the number of tiles in the row
    global OutsideTileCount, OutsideTileList, InsideTileList, InsideTileCount, WinningTileCount, WinningTile
    for k in range(RowTileCount):
        ttk.Label(frame, image=bull).grid(column=k, row=RowNo)
    match RowNo:
        case 2:  # Outer Hand
            OutsideTileCount = 0
            OutsideTileList.clear()
        case 4:  # Inner hand
            InsideTileCount = 0
            InsideTileList.clear()
        case 6:  # Winning Tile
            WinningTileCount = 0
            WinningTile.clear()


def select_flower(flowerNo):
    global selected_flowers
    # Replacing the image of the button
    # Appending to the selected_flowers list
    if flowerNo in selected_flowers:
        # Change to black and white
        path_flower = f'mahjong_tile_images/{flowerNo}_k.png'
        selected_flowers.remove(flowerNo)
    else:
        # Change to colour
        path_flower = f'mahjong_tile_images/{flowerNo}.png'
        selected_flowers.append(flowerNo)
    # Loading the new image
    image_f = Image.open(path_flower)
    resize_f = image_f.resize((60, 72))
    image_f = ImageTk.PhotoImage(resize_f)
    new_flower_button = ttk.Button(frame, image=image_f, command=lambda flowerNo=flowerNo: select_flower(flowerNo))
    new_flower_button.grid(column=flowerNo + 4, row=6)
    ttk.Button(frame, image=image_f).image = image_f


def evaluate_hand():
    global frame_canvas, scrollbar
    eva_wind = direction_conversion(WindDropdown.get())
    eva_seat = direction_conversion(SeatDropdown.get())
    if 'selected' in SelfDrawnBox.state():
        sd = 1
    else:
        sd = 0

    Output = mj_scorecount(WinningTile.copy(), OutsideTileList.copy(), InsideTileList.copy(), sd, eva_wind, eva_seat,
                           selected_flowers)
    Output_formatted = f'Score: {Output[0]} \nAccolades: '
    for accolade in Output[1]:
        Output_formatted += f'\n{accolade}'

    if len(Output) == 4: # 雙吃
        Output_formatted += f'\n\nScore: {Output[2]} \nAccolades: '
        for accolade in Output[3]:
            Output_formatted += f'\n{accolade}'

    OutputLabel['text'] = Output_formatted


def switch_input(switch_to: str):
    global target_entry
    # switch_to is the hand we are switching to
    # Reset all buttons
    OutsideTilesTitle = Button(frame, text="Outside Tiles", command=lambda: switch_input("Outer"))
    OutsideTilesTitle.grid(column=0, row=1, columnspan=2, sticky=W)
    InsideTilesTitle = Button(frame, text="Inside Tiles", command=lambda: switch_input("Inner"))
    InsideTilesTitle.grid(column=0, row=3, columnspan=2, sticky=W)
    WinningTileTitle = Button(frame, text="Winning Tile", command=lambda: switch_input("Winning"))
    WinningTileTitle.grid(column=0, row=5, columnspan=2, sticky=W)

    # Change the state of the one we are targetting
    match switch_to:
        case "Outer":
            # Change colour to red
            OutsideTilesTitle = Button(frame, text="Outside Tiles", bg='RED', fg='WHITE',
                                       command=lambda: switch_input("Outer"))
            OutsideTilesTitle.grid(column=0, row=1, columnspan=2, sticky=W)
            target_entry = "Outer"
        case "Inner":
            InsideTilesTitle = Button(frame, text="Inside Tiles", bg='RED', fg='WHITE',
                                      command=lambda: switch_input("Inner"))
            InsideTilesTitle.grid(column=0, row=3, columnspan=2, sticky=W)
            target_entry = "Inner"
        case "Winning":
            WinningTileTitle = Button(frame, text="Winning Tile", bg='RED', fg='WHITE',
                                      command=lambda: switch_input("Winning"))
            WinningTileTitle.grid(column=0, row=5, columnspan=2, sticky=W)
            target_entry = "Winning"


# Initialising the window
root = Tk()
root.title("PC MJ COUNTER")
root.geometry("1280x720")
root.tk.call('tk', 'scaling', 2)

# Outer frame for scrolling
outer_frame = ttk.Frame(root)
outer_frame.pack(fill=BOTH, expand=1)

# Canvas
frame_canvas = Canvas(outer_frame)
frame_canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Scrollbar
scrollbar = ttk.Scrollbar(outer_frame, orient=VERTICAL, command=frame_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# configure the canvas
frame_canvas.configure(yscrollcommand=scrollbar.set)
frame_canvas.bind(
    '<Configure>', lambda e: frame_canvas.configure(scrollregion=frame_canvas.bbox("all"))
)

# Inner frame
frame = ttk.Frame(frame_canvas, padding=20)
frame.grid()
ttk.Label(frame, text="Mahjong Score Counter", font=("", 18)).grid(row=0, columnspan=20, sticky=W)

# Outside Tiles
OutsideTileCount = 0
OutsideTileList = []
OutsideTilesTitle = Button(frame, text="Outside Tiles", fg='WHITE', bg='RED', command=lambda: switch_input("Outer"))
target_entry = "Outer"
OutsideTilesTitle.grid(column=0, row=1, columnspan=2, sticky=W)
## Clear button
OutsideTileReset = ttk.Button(frame, text="Reset Outer Hand", command=lambda: ResetWinningTile(16, 2))
OutsideTileReset.grid(column=2, row=1, columnspan=3)
# Diplay image (Outerhand)
bull_img = Image.open("mahjong_tile_images/bull.png")
bull_resize = bull_img.resize((60, 72))
bull = ImageTk.PhotoImage(bull_resize)
for i in range(16):
    ttk.Label(frame, image=bull).grid(column=i, row=2)

# Inner Hand
InsideTileCount = 0
InsideTileList = []
InsideTilesTitle = Button(frame, text="Inside Tiles", command=lambda: switch_input("Inner"))
InsideTilesTitle.grid(column=0, row=3, columnspan=2, sticky=W)
## Clear button
InsideTileReset = ttk.Button(frame, text="Reset Inner Hand", command=lambda: ResetWinningTile(16, 4))
InsideTileReset.grid(column=2, row=3, columnspan=3)
# Diplay image (InnerHand)
for i in range(16):
    ttk.Label(frame, image=bull).grid(column=i, row=4)

# Winning Tile
WinningTileCount = 0
WinningTile = []
WinningTileTitle = Button(frame, text="Winning Tile", command=lambda: switch_input("Winning"))
WinningTileTitle.grid(column=0, row=5, columnspan=2, sticky=W)
## Clear button
WinningTileReset = ttk.Button(frame, text="Reset Winning Tile", command=lambda: ResetWinningTile(1, 6))
WinningTileReset.grid(column=2, row=5, columnspan=3)

# Diplay image (InnerHand)
ttk.Label(frame, image=bull).grid(column=0, columnspan=8, row=6, sticky=W)

# Flowers
flowerTitle = ttk.Label(frame, text="Flowers")
flowerTitle.grid(column=5, row=5, columnspan=10, sticky=W)
selected_flowers = []
for flower in range(8):
    path = f'mahjong_tile_images/{flower + 1}_k.png'
    image01 = Image.open(path)
    resize_img = image01.resize((60, 72))
    imageO1 = ImageTk.PhotoImage(resize_img)
    test1 = ttk.Button(frame, image=imageO1, command=lambda flower=flower: select_flower(flower + 1))
    test1.grid(column=flower + 5, row=6)
    ttk.Button(frame, image=imageO1).image = imageO1

# 3 main suits

for suit in range(3):
    for tileNum in range(9):
        # Path of image
        target = (suit + 1) * 10 + (tileNum + 1)
        path = f"mahjong_tile_images/{target}.png"
        # display image
        image01 = Image.open(path)
        resize_img = image01.resize((60, 72))
        imageO1 = ImageTk.PhotoImage(resize_img)
        test1 = ttk.Button(frame, image=imageO1, command=lambda target=target: enter_tile(target))
        test1.grid(column=tileNum, row=(suit + 7))
        ttk.Button(frame, image=imageO1).image = imageO1

# LuckyTiles
for tileNum in range(7):
    # Path of image
    target = 40 + (tileNum + 1)
    path = f"mahjong_tile_images/{target}.png"
    # display image
    image01 = Image.open(path)
    resize_img = image01.resize((60, 72))
    imageO1 = ImageTk.PhotoImage(resize_img)
    test1 = ttk.Button(frame, image=imageO1, command=lambda target=target: enter_tile(target))
    test1.grid(column=tileNum, row=10)
    ttk.Button(frame, image=imageO1).image = imageO1

# Wind
WindList = ['East', 'South', 'West', "North"]
WindTitle = ttk.Label(frame, text="Wind")
WindTitle.grid(column=0, row=11, columnspan=2, sticky=W)

WindDropdown = ttk.Combobox(frame, state="readonly", values=WindList, width=6)
WindDropdown.grid(column=0, row=12, columnspan=2, sticky=W)

# Seat
SeatTitle = ttk.Label(frame, text="Seat")
SeatTitle.grid(column=2, row=11, columnspan=2, sticky=W)

SeatDropdown = ttk.Combobox(frame, state="readonly", values=WindList, width=6)
SeatDropdown.grid(column=2, row=12, columnspan=2, sticky=W)

# SelfDrawn
SelfDrawnTitle = ttk.Label(frame, text="Self Drawn")
SelfDrawnTitle.grid(column=4, row=11, columnspan=2, sticky=W)

SelfDrawnBox = ttk.Checkbutton(frame)
SelfDrawnBox.grid(column=4, row=12, columnspan=2, sticky=W)

# Evaluate button
EvaluateButton = ttk.Button(frame, text="Evaluate Score", command=evaluate_hand)
EvaluateButton.grid(column=6, row=12, columnspan=4, sticky=W)

OutputLabel = ttk.Label(frame)
OutputLabel.grid(column=0, row=13, columnspan=1000, sticky=W)

ttk.Button(frame, text="Quit", command=root.destroy).grid(column=0, row=1000, columnspan=4, sticky=W)

# Add inner frame to canvas
frame_canvas.create_window((0, 0), window=frame, anchor="nw")
root.mainloop()
