import * as lu from './listUtilsJS.js';

export function validityCheck(wh_Inner, wh_Outer, w_Tile){
    // step 0: check length
    const wh_Total = wh_Inner.concat(wh_Outer, w_Tile);
    let validityOutput = new Array(5);
    // first slot: hand valid?
    validityOutput[0] = 0;
    // check for number of tiles and type of all items
    if (wh_Total.length != 17) {
        return validityOutput
    }
    if (!(lu.list_type_check(wh_Total, 'number'))){
        validityOutput[0] = 'Error: Wrong type in lists';
        return validityOutput
    }

    // prodcedure: find eye --> triplet split --> straight split
    // (if needed) find eye --> straight split --> triplet split

    // finding eyes
    
    const potentialEyes = lu.element_appear_more_than_n_times_find(wh_Inner.concat(w_Tile), 2);
    
    wh_Inner.sort();

    let ey;
    let insideValid = false;

    for (ey of potentialEyes){
        let wh_Inner_working = wh_Inner.slice();
        
        wh_Inner_working = wh_Inner_working.concat(w_Tile);

        wh_Inner_working.sort();

        // removing the 2 eyes from wh_inner
        // triplet split
        wh_Inner_working.splice(wh_Inner_working.indexOf(ey), 2);
        

        let result = lu.triplet_split(wh_Inner_working);
        let innerTriplets = result[0];
        let remInnerTiles = result[1];

        // straight split (if complete hand should return 0 remaining tiles)
        let max_tile = remInnerTiles.reduce((a,b) => Math.max(a,b), -Infinity)
        // skip evaluation if lucky tiles remain
        if (max_tile > 40) {
            continue
        }

        result = lu.straight_split(remInnerTiles);
        let innerStraights = result[0];
        remInnerTiles = result[1];

        if (remInnerTiles.length == 0){
            // found valid hand (inner bit)
            validityOutput[1] = innerStraights;
            validityOutput[2] = innerTriplets;
            validityOutput[5] = new Array(2);
            validityOutput[5].fill(ey)
            insideValid = true;
            break
        }

    }

    if (!insideValid) {
        // inner hand no valid combination
        return validityOutput
        // end function
    }

    // outside?!
    let result = lu.triplet_split(wh_Outer);
    let outerTriplets = result[0];
    let remOuterTiles = result[1];

    let max_tile = remOuterTiles.reduce((a,b) => Math.max(a,b), -Infinity);

    if (max_tile > 40) {
        // no outer valid hand
        return validityOutput;
    }

    result = lu.straight_split(remOuterTiles);
    let outerStraights = result[0];
    remOuterTiles = result[1];

    if (remOuterTiles.length > 0) {
        return validityOutput;
        // no valid hand
    }

    validityOutput[3] = outerStraights;
    validityOutput[4] = outerTriplets;
    // valid hand
    validityOutput[0] = 1;

    return validityOutput;
}

let inner = [18, 18, 19, 19, 19, 28, 28, 29, 29, 29, 37, 37, 37];
let outer = [44, 44, 44];
let wt = [28];

console.log(validityCheck(inner, outer, wt));