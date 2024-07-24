function append(value, select) {
    // check length ++
    // adds some value to the list arr
    switch(select) {
        case 1:
            if (inner_arr.length == 16) {
                alert('Too many tiles!!!')
            }
            else {
                inner_arr[inner_arr.length] = value;
                // change img
                const id_chg = '1-' + inner_arr.length
                const path = '../mahjong_tile_images/' + value +'.png';
                document.getElementById(id_chg).src = path;
            }
            break

        case 2:
            if (outer_arr.length == 16) {
                alert('Too many tiles!!!')
            }
            else{
                outer_arr[outer_arr.length] = value;
                // change img
                const id_chg = '2-' + outer_arr.length
                const path = '../mahjong_tile_images/' + value +'.png';
                document.getElementById(id_chg).src = path;
            }
            break

        case 3:
            if (winner_arr.length == 1) {
                alert('Too many tiles!!!')
            }
            else {
                winner_arr[winner_arr.length] = value;
                // change img
                const id_chg = '3-1'
                const path = '../mahjong_tile_images/' + value +'.png';
                document.getElementById(id_chg).src = path;
            }
            break
        default:
            // pass
    }
}

function removeEle(arrID) {
    // delete value from arrID 
    // 1: inner, 2: outer, 3: winner
    switch(arrID) {
        case 1:
            inner_arr.pop();
            break
        case 2:
            outer_arr.pop();
            break
        case 3:
            winner_arr.pop();
            break
    }
    redraw()

}

function changeSel(sel) {
    let i = 1;
    do {
        if (i != sel) {
            const id_name = ('selButton' + i);

            document.getElementById(id_name).className = 'selButton'
        }
        else {
            const id_name = ('selButton' + i);

            document.getElementById(id_name).className = 'selButton_selected'
        }

        i ++ 
    }
    while (i <= 3);
}

function redraw() {
    // redraws the tiles shown according to the tiles in inner_arr, outer_arr, winner_arr
    // redraw the winning tile
    const img_null = '../mahjong_tile_images/bull.png';
    document.getElementById('3-1').src = img_null;
    for (let i=1; i<=16; i++) {
        const id_1 = '1-' + i;
        const id_2 = '2-' + i;
        document.getElementById(id_1).src = img_null;
        document.getElementById(id_2).src = img_null;
    }

    // redraw inner row 
    for (k=0; k<inner_arr.length;k++) {
        // index k
        const id_inner = '1-' + (k+1);
        const path = '../mahjong_tile_images/' + inner_arr[k] + '.png';
        document.getElementById(id_inner).src = path;
    }

    // redraw outer row

    for (k=0; k<outer_arr.length;k++) {
        // index k
        const id_outer = '2-' + (k+1);
        const path = '../mahjong_tile_images/' + outer_arr[k] + '.png';
        document.getElementById(id_outer).src = path;
    }

    // redraw winning tile if applicable

    if (winner_arr.length) {
        const path = '../mahjong_tile_images/' + winner_arr[0] + '.png';
        document.getElementById('3-1').src = path;
    }

}

function debug(type=null) {
    switch (type) {
        
        case 'b':
            inner_arr = [11, 14, 17, 22, 25, 28, 33, 36, 39, 41, 42, 43, 44, 45, 46, 47];
            outer_arr = [];
            winner_arr = [47];
            break

        case 't':
            inner_arr = [11, 19, 21, 29, 31, 39, 33, 34, 35, 41, 42, 43, 44, 45, 46, 47];
            outer_arr = [];
            winner_arr = [46];
            break
        default:
            inner_arr = [18, 18, 19, 19, 19, 28, 28, 29, 29, 29, 37, 37, 37];
            outer_arr = [44, 44, 44];
            winner_arr = [28];
            break
    }
    redraw()
}

function cls() {
    inner_arr = [];
    outer_arr = [];
    winner_arr = [];
    redraw();

    document.getElementById('accolades').innerHTML = '~';
    document.getElementById('score').innerHTML = '~';
}

function fl_toggle(id) {
    const img_id = 'fl_' + id;
    if (fl.includes(id)) {
        fl.splice(fl.indexOf(id), 1);
        document.getElementById(img_id).className = 'tile_gray';
        return
    }
    // else 
    fl[fl.length] = id;
    document.getElementById(img_id).className = 'tile';

}



let inner_arr = [];
let outer_arr = [];
let winner_arr = [];
let fl = [];

let selection = 1;



