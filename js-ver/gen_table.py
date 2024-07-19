# suit 1
f = open("./js-ver/tileTable.txt", "w")
for i in range(9):
    id = 11 + i
    path = f'../mahjong_tile_images/{id}.png'
    cl = 'tile'
    html_ele = f"<td><button onclick='append({id}, selection)'><img src='{path}' class='{cl}' ></button>
    </td>00\n"
    f.write(html_ele)

f.close()