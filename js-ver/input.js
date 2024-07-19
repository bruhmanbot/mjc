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
                document.getElementById('inner_dest').innerHTML = inner_arr;
            }
            break

        case 2:
            if (outer_arr.length == 16) {
                alert('Too many tiles!!!')
            }
            else{
                outer_arr[outer_arr.length] = value;
                document.getElementById('outer_dest').innerHTML = outer_arr;
            }
            break

        case 3:
            if (winner_arr.length == 1) {
                alert('Too many tiles!!!')
            }
            else {
                winner_arr[winner_arr.length] = value;
            document.getElementById('winner_dest').innerHTML = winner_arr;
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
            document.getElementById('inner_dest').innerHTML = inner_arr;
            break
        case 2:
            outer_arr.pop();
            document.getElementById('outer_dest').innerHTML = outer_arr;
            break
        case 3:
            winner_arr.pop();
            document.getElementById('winner_dest').innerHTML = winner_arr;
            break
    }

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

let inner_arr = [];
let outer_arr = [];
let winner_arr = [];

let selection = 1;

document.getElementById().src


