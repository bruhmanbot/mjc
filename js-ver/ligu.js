import * as lu from "./listUtilsJS.js";
import { flower_count, load_acc_dict, sum_accolades } from "./acc_class.js";

export function liguCheck(wh_Inner, wh_Outer, wh_tile) {
    // checks if there is a ligu hand
    // no outer tiles can exist
    // returning in format:
    // (1/0) , [pairs], [triplet]
    if (wh_Outer.length > 0) {
        return 0, [], []
    }

    // count up the occurences of each inner tile
    const wh_Total = wh_Inner.concat(wh_tile);
    const uniqCount = lu.unique_occurence_count(wh_Total)
    // uniqCount: dictionary/obj

    let pairs = 0;
    let triplets = 0;

    let pairsList = [];
    let tripletList = [];

    for (let tile of Object.keys(uniqCount)) {
        switch (uniqCount[tile]) {
            case 2:
                pairs ++ // add 1 to the amount of pairs
                pairsList[pairsList.length] = Number(tile);
                break
            case 3:
                triplets ++ // add 1 to the amount of triplets
                tripletList[tripletList.length] = Number(tile);
                break
            case 4:
                pairs = pairs + 2 // add 2 to the amount of pairs (quads = 2 pairs)
                // append tile twice to the end of pairsList
                pairsList[pairsList.length] = Number(tile);
                pairsList[pairsList.length] = Number(tile);
                break
            case (uniqCount[tile] >= 5):
                return 0, [], [] // obviously cheating
            default:
                continue // skips to next tile
        }
    }

    if (pairs != 7 || triplets != 1) {
        // not 7 pairs + 1 triplet!
        return 0, [], []
    }

    // valid case
    return new Array(1, pairsList, tripletList)
}


export async function score_count_L(pairs, triplets, winningTile, wind, seat, sd, flower) {
    // initialise accolade table
    const accolade = await load_acc_dict();

    // preload ligu
    let acc_accolade = [82];

    // flowers
    const fl_res = await flower_count(seat, flower);
    const fl_score = fl_res[0];
    // add the flower accolades!!
    acc_accolade = acc_accolade.concat(fl_res[1]);
    acc_accolade.sort() 
    // put flowers in front

    // evaluate score for lucky tile triplet (here triplet should be list of len 1 e.g. [41])
    let windScore = 0;
    let scholarScore = 0;

    // suitsPresence
    const suitsPresence = new Array(5)
    suitsPresence.fill(0)

    if (triplets[0] >= 45) {
        acc_accolade[acc_accolade.length] = 14; // scholar tile
        scholarScore = accolade[14].pts;
        suitsPresence[4] = 1;
    }
    else if (triplets[0] > 40) {
        // wind tiles xx bonus

        if (triplets[0] % 4 == wind) {
            windScore = windScore + accolade[6].pts;
        }
        if (triplets[0] % 4 == seat) {
            windScore = windScore + accolade[7].pts;
        }

        // base for wind tiles
        windScore = windScore + accolade[5].pts;
        acc_accolade[acc_accolade.length] = 5; // wind tile
        suitsPresence[3] = 1;
    }

    // check winning tile
    if (winningTile[0] == triplets[0]) {
        // winning on the triplet --> 1 in 8
        acc_accolade[acc_accolade.length] = 83;
    }
    else if (lu.count(winningTile[0], pairs) == 1) {
        // only appearing as ONE pair --> dudu
        acc_accolade[acc_accolade.length] = 20;
    }
    else {
        // two triplets waiting --> 1 in 2
        acc_accolade[acc_accolade.length] = 21;
    }

    // check suits present
    for (let tile of pairs) {
        const suit_index = Number(Math.floor(tile / 10) - 1)
        suitsPresence[suit_index] = 1;
    }


    // consec pairs
    let pairs_working = pairs.slice();
    pairs_working = pairs_working.concat(triplets);
    pairs_working.sort();

    // extract only the number tiles
    pairs_working = pairs_working.filter((tile) => tile < 40);

    var pairs_working_u = [];

    for (let tile of pairs_working) {
        pairs_working_u[pairs_working_u] = Number(tile%10);
    }

    pairs_working_u.sort();



    let consecPairs = []; // stores the number of consec pairs in an arithmetic sequence

    while (pairs_working.length > 0) {
        let Aseq = lu.find_arithmetic_seq(pairs_working[0], pairs_working, 1);
        consecPairs[consecPairs.length] = Aseq.length; // append the length of each Aseq to the end of the consec pairs

        // remove the items of the Aseq from pairs_working
        for (const tile of Aseq) {
            pairs_working.splice(pairs_working.indexOf(tile), 1)
        }
    }

    // sum up accolades for the consec pairs
    for (const consecNum of consecPairs) {
        if (consecNum < 3) {
            continue
        }
        // executes if consecNum > 3
        const accID = Number(consecNum + 81);
        acc_accolade[acc_accolade.length] = accID;
    }

    // mixed dragon?
    const Aseq = lu.find_arithmetic_seq(pairs_working_u[0], pairs_working_u, 1);

    if (Aseq.length == 8) {
        acc_accolade[acc_accolade.length] = 90;
    }


    // check for suit related accolades
    // mixed/full flushes
    const normalSuits = suitsPresence.slice(0,3) // first 3 elements

    const luckySuits = suitsPresence.slice(3,5) // last 2 elements
    
    const normalSuitsSum = normalSuits.reduce((accumulator, currentvalue) => accumulator + currentvalue, 0,);


    const luckySuitsSum = luckySuits.reduce((accumulator2, currentvalue2) => accumulator2 + currentvalue2, 0,);

    switch(normalSuitsSum) {
        case 0:
            // all lucky tiles
            acc_accolade[acc_accolade.length] = 62;
            break
        case 1:
            // mixed flush / full flush
            if (luckySuitsSum) {
                acc_accolade[acc_accolade.length] = 60;
            }
            else {
                acc_accolade[acc_accolade.length] = 61;
            }
        case 2:
            // 2 non lucky suits
            if (luckySuitsSum == 0) {
                acc_accolade[acc_accolade.length] = 59;
            }
        case 3:
            // 5 suits?
            if (luckySuitsSum == 2) {
                acc_accolade[acc_accolade.length] = 57;
            }
    }

    if (sd) {
        acc_accolade[acc_accolade.length] = 74;
    }

    // final results
    const finalRes = await sum_accolades(acc_accolade, fl_score, windScore, scholarScore);

    return finalRes 
}