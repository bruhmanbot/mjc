# suit 1
f = open("./js-ver/tileTable.txt", "w")

f.write('<tr>\n')
for i in range(9):
    id = 11 + i
    path = f'../mahjong_tile_images/{id}.png'
    cl_0 = 'tileButton'
    cl_1 = 'tile'
    html_ele = f"   <td><button class='{cl_0}' onclick='append({id}, selection)'><img src='{path}' class='{cl_1}'></button></td>\n"
    f.write(html_ele)
f.write('</tr>\n\n')


# suit 2
f.write('<tr>\n')
for i in range(9):
    id = 21 + i
    path = f'../mahjong_tile_images/{id}.png'
    cl_0 = 'tileButton'
    cl_1 = 'tile'
    html_ele = f"   <td><button class='{cl_0}' onclick='append({id}, selection)'><img src='{path}' class='{cl_1}'></button></td>\n"
    f.write(html_ele)
f.write('</tr>\n\n')

# suit 3
f.write('<tr>\n')
for i in range(9):
    id = 31 + i
    path = f'../mahjong_tile_images/{id}.png'
    cl_0 = 'tileButton'
    cl_1 = 'tile'
    html_ele = f"   <td><button class='{cl_0}' onclick='append({id}, selection)'><img src='{path}' class='{cl_1}'></button></td>\n"
    f.write(html_ele)
f.write('</tr>\n\n')

# lucky tiles
f.write('<tr>\n')
for i in range(7):
    id = 41 + i
    path = f'../mahjong_tile_images/{id}.png'
    cl_0 = 'tileButton'
    cl_1 = 'tile'
    html_ele = f"   <td><button class='{cl_0}' onclick='append({id}, selection)'><img src='{path}' class='{cl_1}'></button></td>\n"
    f.write(html_ele)
f.write('</tr>\n\n')

f.close()