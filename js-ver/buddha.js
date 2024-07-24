import * as lu from './listUtilsJS.js';
import { load_acc_dict, sum_accolades, flower_count } from './acc_class.js';

export function buddhaCheck(wh_Inner, wh_Outer, w_Tile){
    // Does the checking thing for buddha and 13 orphans
    // returns the validity result (1/0) as well as the remaining tiles outside of the lucky tiles
    // first thing to check is outer tiles (which should not exist)

    if (wh_Outer.length) {
        return new Array(0, [], [])
    }

    const wh_total = wh_Inner.concat(w_Tile);
    wh_total.sort();

    // extract by suit and check

    let suit_1 = [];
    let suit_2 = [];
    let suit_3 = [];
    let lt = [];
    for (let t of wh_total) {
        switch (Math.floor(Number(t) / 10)) {
            case 1:
                suit_1[suit_1.length] = t;
                break

            case 2:
                suit_2[suit_2.length] = t;
                break

            case 3:
                suit_3[suit_3.length] = t;
                break

            case 4:
                lt[lt.length] = t;
                break
        }
    }
    
    let suitTiles = new Array(suit_1, suit_2, suit_3, lt)

    let suitTilesNum = [];
    for (const list of suitTiles) {
        suitTilesNum[suitTilesNum.length] = list.length;
    }
    // create a sorted copy
    let suitTilesNum_sort = suitTilesNum.slice()
    suitTilesNum_sort.sort()

    let do_OrphansCheck = false;
    let do_BuddhaCheck = false;
    // decide if we are in the case of 13 orphans or 16 buddhas
    if (suitTilesNum_sort[0] == 2) {
        // 13 orphans
        do_OrphansCheck = true;
    }
    else if (suitTilesNum_sort[0] == 3) {
        do_BuddhaCheck = true;
    }
    else {
        // no valid case
        return new Array(0, [], [])
        // end the function here
    }

    if (do_BuddhaCheck) {
        const wh_total_set = new Set(wh_total);
        if (wh_total_set.size != 16) {
            // should be size 16 if valid
            return new Array(0, [], [])
            // end function here
        }

        // define function to see if the list items are related or not
        // e.g. 2 5 8 --> false (not related) | 1 3 7 --> true (is related)
        // related: diff between any 2 successive items <=2
        function isRelated(list) {
            let working_list = list.slice()
            // dupe the list so the function is non-destructive
            working_list.sort()
            // sort the list and extract unique items
            const working_set = new Set(working_list);

            for (let i = 0; i<(working_set.size-1); i++) {
                const diff = working_set[i+1] - working_set[i];
                if (diff < 3) {
                    // items are related!!
                    return true
                    // ends the function here
                }
            }

            // code executed if it survives for loop (i.e. not related)
            return false;
        }

        // check if our 3 suit lists are related
        let i = 0;
        do {
            if (isRelated(suitTiles[i])) {
                // executes if they are related
                return new Array(0, [], [])
                // ends the entire function here
            }

            // else i goes to the next list
            i++;
        } while (i <= 2)

        // if we get here then the hand survives the above loop so we only have to check lucky tiles (one of each)
        const lt_set = new Set (suitTiles[3].slice())
        // lt_set represents all unique items of the luckytiles section
        if (lt_set.size == 7) {
            // all 7 seven tiles
            const numTiles = suitTiles[0].concat(suitTiles[1], suitTiles[2]);
            // combine the number tiles
            const numTiles_set = new Set(numTiles);

            // find the eye
            let eye = [];
            for (const t of wh_total_set){
                if (lu.count(t, wh_total) == 2){
                    // appeared twice
                    eye[0] = t
                    break
                }
            }

            return new Array(1, numTiles_set, eye)
        }
        else {
            return 0, [], []
        }
    }
    else if(do_OrphansCheck) {
        // plan: find the orphans remove it
        // check the remaining tiles and see if there is a straight + 1 orphan left

        let wh_working = wh_total.slice();

        // here remTiles should leave behind the 13 orphans + 1 duplicate tile (eye)
        const orphans = [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]
        if (lu.set_containslists(orphans, wh_working)) {
            // continue
        }
        else {
            return new Array (0, [], [])
            // ends the function here
        }

        for (k of orphans) {
            const pop_index = wh_working.indexOf(Number(k));
            wh_working.splice(pop_index,1);
            // removes the orphans from working set
        }

        const straight_split_res = lu.straight_split(wh_working)
        const straight = straight_split_res[0];
        let remTiles = straight_split_res[1];

        // triplet checking
        const triplet_split_res = lu.triplet_split(remTiles);
        const triplet = triplet_split_res[0];
        remTiles = triplet_split_res[1];

        // check if only 1 tile should remain in remTiles
        const kan = straight.concat(triplet);
        if (remTiles.length != 1) {
            return new Array (0, [], [])
        }
        // check if last tile is orphan
        if (orphans.includes(remTiles[0])) {
            return new Array(2, kan, remTiles)
        }
        else {
            return new Array (0, [], [])
        }
        

    }

    // failsafe if we somehow got here (we shouldn't)
    return new Array(0, [], [])

}

export async function score_count_b(numTiles, eye, wTile, sd, wind, seat, flower){
    // initialise the accolade table first
    const accolade = await load_acc_dict();

    // preload 16 buddhas
    let acc_accolade = [76];

    // flowers
    const fl_res = await flower_count(seat, flower);
    const fl_score = fl_res[0];
    // add the flower accolades!!
    acc_accolade = acc_accolade.concat(fl_res[1]);
    acc_accolade.sort() 
    // put flowers in front
    
    // check for 1 in 16 & dudu
    if (eye[0] == wTile[0]) {
        // 1 in 16
        acc_accolade[acc_accolade.length] = 77;
    }
    else if (wTile[0] > 40){
        // dudu
        acc_accolade[acc_accolade.length] = 20;
    }
    else if (wTile[0] % 10 <= 3) {
        if (numTiles.includes(wTile[0] + 3)) {
            // dudu
            acc_accolade[acc_accolade.length] = 20;
        }
    }
    else if (wTile[0] % 10 <= 6) {
        if (numTiles.includes(wTile[0] - 3) && numTiles.includes(wTile[0] + 3)) {
            // dudu
            acc_accolade[acc_accolade.length] = 20;
        }
    }
    else {
        if (numTiles.includes(wTile[0]-3)) {
            // dudu
            acc_accolade[acc_accolade.length] = 20;
        }
    }

    // create a new dupe list for numTiles and sort it
    let working_numTiles = Array.from(numTiles);

    working_numTiles.sort();
    // here numTiles is a set of length (size) 9
    let working_numTilesU = [];

    for (let t of working_numTiles) {
        working_numTilesU[working_numTilesU.length] = (t % 10)
        // extracting the unit digis
    }

    const set_numTiles = new Set (working_numTilesU);

    switch (set_numTiles.size) {
        case 3:
            acc_accolade[acc_accolade.length] = 79;
            break
        case 9:
            acc_accolade[acc_accolade.length] = 78;
            break
        default:
            // pass
            break
    }

    // counting up the final scores (and add base here)
    const finalResult = sum_accolades(acc_accolade, fl_score, 0, 0); // 0 for wind and scholarscore

    return finalResult

}

export async function score_count_13(kan, eye, w_Tile, sd, wind, seat, flower) {
    // initialise the accolade table first
    const accolade = await load_acc_dict();

    // preload 13 orphans
    let acc_accolade = [80];

    // flowers
    const fl_res = await flower_count(seat, flower);
    const fl_score = fl_res[0];
    // add the flower accolades!!
    acc_accolade = acc_accolade.concat(fl_res[1]);
    acc_accolade.sort() 
    // put flowers in front


    // need to check kan to evaluate
    let doTripletCheck = false;
    let doStraightCheck = false;
    if (kan[0] == kan[1]) {
        // check for triplet
        doTripletCheck = true;
    }
    else {
        doStraightCheck = true;
    }

    // otherwise, the winning tile is not a lucky tile, but may still be dudu!!
    // check for 1 in 13 / dudu
    if (w_Tile[0] == eye[0]) {
        acc_accolade[acc_accolade.length] = 81;
    }

    else if (w_Tile[0] > 40) {
        acc_accolade[acc_accolade.length] = 20;
    }
    else if (w_Tile[0] % 10 == 1 || w_Tile[0] % 10 == 9) {
        if (doStraightCheck) {
            if (Math.abs(kan[1]-w_Tile) == 2) {
                // fake dudu
                acc_accolade[acc_accolade.length] = 19;
            }
        }
        else {
            // dudu for triplet and winning on orphan
            acc_accolade[acc_accolade.length] = 20;
        }
    }

    else {
        // winning on non orphan
        if (w_Tile[0] == kan[1]) {
            if (doStraightCheck) {
                acc_accolade[acc_accolade.length] = 18;
            }
            else {
                acc_accolade[acc_accolade.length] = 20;
            }
        }
        else if (w_Tile[0] % 10 == 3 && w_Tile[0] == kan[2]) {
            // edge tile
            acc_accolade[acc_accolade.length] = 20;
        }
        else if (w_Tile[0] % 10 == 7 && w_Tile[0] == kan[0]) {
            // edge tile
            acc_accolade[acc_accolade.length] = 20;
        }
    }


    // scoring for the last kan
    let windScore = 0;
    let scholarScore = 0;

    if (doStraightCheck) {
        if (kan[0] % 10 == 1 || kan[kan.length-1] % 10 == 9) {
            // contain an orphan
            acc_accolade[acc_accolade.length] = 69;
        }
    }
    else if (doTripletCheck) {
        if (kan[1] < 40) {
            // non lt
            if (kan[1] % 10 == 1 || kan[kan.length-1] % 10 == 9) {
                // triplet is an orphan + (4 in 1)
                acc_accolade[acc_accolade.length] = 71;
                acc_accolade[acc_accolade.length] = 54;
            }
        }
        else {
            // 4 in 1 and all lt+1/9
            acc_accolade[acc_accolade.length] = 71;
            acc_accolade[acc_accolade.length] = 54;
            // LT
            if (kan[1] < 45) {
                acc_accolade[acc_accolade.length] = 5;
                // wind tile
                if (kan[1] % 10 == wind) {
                    windScore = windScore + accolade[6].pts
                }

                if (kan[1] % 10 == seat) {
                    windScore = windScore + accolade[7].pts
                }

                // wind tile base
                windScore = windScore + accolade[8].pts
            }
            else {
                acc_accolade[acc_accolade.length] = 14;
                scholarScore = accolade[14].pts
            }
        }
        
    }

    // self drawn
    if (sd) {
        acc_accolade[acc_accolade.length] = 74;
    }

    // calculating score and output txt
    // counting up the final scores and add base
    const finalResult = sum_accolades(acc_accolade, fl_score, windScore, scholarScore)

    return finalResult

}

// function eval_hand_b_test(){
//     const rez = buddhaCheck(inner_arr, outer_arr, winner_arr);

//     console.log(rez);

// }

// // binding the function to the eval_button
// document.getElementById('eval_button_b').addEventListener('click', eval_hand_b_test);