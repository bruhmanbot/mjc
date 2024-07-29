import * as lu from './listUtilsJS.js';

import  * as acc_class from './acc_class.js';

export async function score_count_A(innerStraights, innerTriplets, outerStraights, outerTriplets, eyePair, winningTile,
    sd, wind, seat, flower) {

        const total_Tiles = innerStraights.concat(innerTriplets, outerStraights, outerTriplets, eyePair);
        const total_Tiles2 = innerStraights.concat(innerTriplets, outerStraights, outerTriplets);
        
        const innerS = lu.split_list(innerStraights, 3);
        const innerT = lu.split_list(innerTriplets, 3);
        const outerS = lu.split_list(outerStraights, 3);
        const outerT = lu.split_list(outerTriplets, 3);
        
        const innerK = innerS.concat(innerT);
        const outerK = outerS.concat(outerT);

        const totalS = innerS.concat(outerS);
        const totalT = innerT.concat(outerT);

        // acc dict
        const accolade = await acc_class.load_acc_dict();

        // store our accolades here empty list!
        let accumulated_acc = [];

        // flowers
        const fl_res = await acc_class.flower_count(seat, flower);
        const fl_score = fl_res[0];
        // add the flower accolades!!
        accumulated_acc = accumulated_acc.concat(fl_res[1]);


        // unit digis
        const totalS_u = [];
        for (let s of totalS) {
            // append unit digit of middle tile to totalS
            totalS_u[totalS_u.length] = s[1] % 10;
        }

        const totalT_u = [];
        const totalT_numTiles = [];
        for (let t of totalT) {
            // append tile number to total T
            totalT_numTiles[totalT_numTiles.length] = t[1];
            // append unit digit of triplet tile (only for non lucky tiles!) to totalS
            totalT_u[totalT_u.length] = t[1] % 10;
        }

        // wind tiles
        let windTileCount = 0;
        let windScore = 0;
        let kan;
        for (kan of totalT){
            if (40 < kan[1] && kan[1]< 45) {
                windTileCount ++;
                if (kan[1] % 10 == seat){
                    windScore = windScore + accolade[7].pts; // seat bonus
                }
                if (kan[1] % 10 == wind){
                    windScore = windScore + accolade[6].pts; // wind bonus
                }
            }
        }
      
        // scholar tiles
        let scholarCount = 0;
        let scholarScore = 0;

        for (kan of totalT){
            // 45 - 47
            if (45 <= kan[1] && kan[1] < 48) {
                scholarCount ++;
            }
        }
        
        // eye
        if (45 <= eyePair[1] && eyePair[1] < 48) {
            scholarCount = scholarCount + 0.5;
        } 
        else if (40 < eyePair[1] && eyePair[1] < 45) {
            windTileCount = windTileCount + 0.5;
        }


        // winds & scholar bonuses
        if (windTileCount + scholarCount == 0){
            // no characters
            accumulated_acc[accumulated_acc.length] = 16
        }
        else {
            switch (windTileCount){
                case 4:
                    // 4 big winds
                    accumulated_acc[accumulated_acc.length] = 11;
                    break
                case 3.5:
                    // 4 smol winds
                    accumulated_acc[accumulated_acc.length] = 10;
                    break
                case 3:
                    // 3 big winds
                    accumulated_acc[accumulated_acc.length] = 9;
                    break
                case 2.5:
                    // 3 smol winds
                    accumulated_acc[accumulated_acc.length] = 8;
                    break 
                    
                default:
                    // add windscore
                    windScore = windScore + Math.floor(windTileCount) * accolade[5].pts;
                    accumulated_acc[accumulated_acc.length] = 5;
                           
            }
    
            // scholar
            switch (scholarCount){
            
                case 3:
                    // 3 big scholar
                    accumulated_acc[accumulated_acc.length] = 13;
                    break
                case 2.5:
                    // 3 smol scholar
                    accumulated_acc[accumulated_acc.length] = 12;
                    break
                default:
                    // add scholarscore
                    scholarScore = Math.floor(scholarCount) * accolade[14].pts;
                    if (scholarScore) {
                        // only add acc if >0
                        accumulated_acc[accumulated_acc.length] = 14;  
                    }
                         
            }
        }

        // windScores and other scores are added at the end

        // 1 in 2
        let checkdudu = true;
        for (kan of innerT) {
            if (winningTile == kan[1]){
                // winning on the triplet e.g. 22 55 get 2/5
                accumulated_acc[accumulated_acc.length] = 21;
                checkdudu = false;
            }
        }
        
        // dudu
        let dudu = 0;
        let fakedudu = 0;
        if (checkdudu) {
            for (kan of innerK) {
                // in the middle
                if (winningTile[0] == kan[1]){
                    accumulated_acc[accumulated_acc.length] = 18;
                    dudu = 1;
                    break
                }
    
                // 3 or 7 edge tile
                else if (winningTile[0] < 40 && (winningTile[0] % 10 == 3)){
                    if (winningTile[0] == kan[2]){
                        accumulated_acc[accumulated_acc.length] = 17;
                        dudu = 1;
                        break
                    }                
                }
                else if (winningTile[0] < 40 && (winningTile[0] % 10 == 7)){
                    if (winningTile[0] == kan[0]){
                        accumulated_acc[accumulated_acc.length] = 17;
                        dudu = 1;
                        break
                    }                
                }
                // eye 
                else if (eyePair.includes(winningTile[0])){
                    dudu = 1;
                    if (kan.includes(winningTile[0])) {
                        fakedudu = 1;
                    }
                    else if (Math.abs(winningTile[0] - kan[1]) == 2 && lu.same_suit(kan[1], winningTile[0])) {
                        fakedudu = 1;
                    }
                }
            }
        }

        if (fakedudu) {
            accumulated_acc[accumulated_acc.length] = 19;
        }
        else if (dudu) {
            if (!(accumulated_acc.includes(17) || accumulated_acc.includes(18))) {
                accumulated_acc[accumulated_acc.length] = 20;
            }
        }
        
        // general eye
        if ([2,5,8].includes(eyePair[0] % 10) && eyePair[0] < 40) {
            accumulated_acc[accumulated_acc.length] = 22;
        }

        // all straight
        if (innerT.length + outerT.length == 0) {
            accumulated_acc[accumulated_acc.length] = 24;
        }

        // dragon + smol old (straight ver)
        let matrix_row;
        let matrix_col;
        let dragon_matrix = [[0,0,0] , [0,0,0] , [0,0,0]];
        

        // initialise 3*3 zero matrix
        for (kan of totalS) {
            let mod = 0;
            switch(kan[0] % 10){

                case 1: //123
                    matrix_row = Math.floor(kan[0] / 10) -1 // selecting row based on suit
                    matrix_col = 0; // first col
                    mod = 1;
                    break;
                case 4: //456
                    matrix_row = Math.floor(kan[0] / 10) -1 // selecting row based on suit
                    matrix_col = 1; // 2nd col
                    mod = 1;
                    break;
                case 7: //789
                    matrix_row = Math.floor(kan[0] / 10) -1 // selecting row based on suit
                    matrix_col = 2; // 3rd col
                    mod = 1;
                    break;
                    
                default:
                    // skip to next kan directly
                    continue;    
            }
            // Modify the matrix if required (add one to count)
            dragon_matrix[matrix_row][matrix_col] ++
        }

        

        let suit;
        
        for (suit of dragon_matrix){
            // considering PURE dragons! / small old
            const suit_sorted = suit.splice().sort();
            if (suit_sorted[0] > 0) {
                // at least 1 dragon
                if (suit_sorted.toString() == [1, 2, 2].toString()){
                    // DOUBLE dragon
                    accumulated_acc[accumulated_acc.length] = 25;
                    accumulated_acc[accumulated_acc.length] = 25;
                    continue
                }
                
                // else one dragon
                accumulated_acc[accumulated_acc.length] = 25;
                continue

            }
            else {
                // find if smol old exists
                let smol_old_list = new Array(suit[0], suit[2]);
                switch (smol_old_list.sort()[0]) {
                    // consider the smallest element here
                    case 1:
                        // 1 smol old
                        accumulated_acc[accumulated_acc.length] = 26;
                        continue
                    case 2:
                        // 2 smol old
                        accumulated_acc[accumulated_acc.length] = 26;
                        accumulated_acc[accumulated_acc.length] = 26;
                        continue
                    case 0:
                        // nothing
                        continue

                }
            }

            
        }
        
        // mixed dragon
        const m_dragons = lu.matrix_diag(dragon_matrix);
        for (let i=0; i<m_dragons; i++) {
            accumulated_acc[accumulated_acc.length] = 27;
        }

        // concealed triplets
        const concealed_triplet_num = innerT.length;
        if (concealed_triplet_num >= 5) {
            if (sd) {
                accumulated_acc[accumulated_acc.length] = 32;
            }
            else {
                accumulated_acc[accumulated_acc.length] = 31;
            }
        }
        else if (concealed_triplet_num >= 2) {
            accumulated_acc[accumulated_acc.length] = 26+concealed_triplet_num;
        }

        // Offsuit repeated straights / suited as well 
        // change if same suit straights should not be counted again
        let offsuit_rs_dict = lu.unique_occurence_count(totalS_u);
        
        for (const s in offsuit_rs_dict) {
            if (offsuit_rs_dict[s] == 1) {
                continue
            }
            
            // skips to next iteration of the loop if count == 1

            let rs = [];
            let rs_set;
            switch (offsuit_rs_dict[s]) {

                case 2:
                    const looping = lu.find_index_duplicate_item(Number(s), totalS_u);
                    // rs here should store 2 indices in a list ;; rs = [4, 5]
                    for (let i = 0; i<looping.length;i++){
                        rs[i] = totalS[looping[i]][0];
                        // changing rs into the actual straights
                    }

                    rs_set = new Set(rs);
                    if (rs_set.size == 2) {
                        // indicate that the 2 sets are of different suits
                        accumulated_acc[accumulated_acc.length] = 33;
                    }
                    else {
                        // same suit!
                        accumulated_acc[accumulated_acc.length] = 37;
                    }
                    break

                case 3:
                    rs = lu.find_index_duplicate_item(Number(s), totalS_u);
                    let rsk = [];
                    // rs here should store 3 indices in a list ;; rs = [2, 4, 5]
                    for (let i = 0; i<rs.length;i++){
                        rsk[rsk.length] = totalS[rs[i]].toString();
                        // changing rs into the actual straights
                    }
                    rs_set = new Set(rsk);
                    
                    if (rs_set.size == 3) {
                        // indicate that the 3 sets are of different suits
                        accumulated_acc[accumulated_acc.length] = 34;
                    }
                    else if (rs_set.size == 2) {
                        // same suit * 2 + 1 os
                        accumulated_acc[accumulated_acc.length] = 33;
                        accumulated_acc[accumulated_acc.length] = 37;
                    }
                    else {
                        // 3 of the same suit
                        accumulated_acc[accumulated_acc.length] = 38;
                    }
                    break

                case 4:
                    rs = lu.find_index_duplicate_item(s, totalS_u);
                    // rs here should store 4 indices in a list ;; rs = [0, 1, 2, 4]
                    for (let i = 0; i<rs.length;i++){
                        rs[i] = totalS[i];
                        // changing rs into the actual straights
                    }
                    rs_set = new Set(rs);

                    if (rs_set.length >= 2) {
                        // indicate that the 4 sets are of >=2 different suits
                        accumulated_acc[accumulated_acc.length] = 35;
                    }
                    else {
                        // QUADS
                        accumulated_acc[accumulated_acc.length] = 39;
                    }
                    break

                case 5:
                    accumulated_acc[accumulated_acc.length] = 36;
                    break

                default:
                    continue
            }
        }
        
        // bbg
        for (let i_str of totalS_u) {
            if (totalS_u.includes(i_str + 1) && totalS_u.includes(i_str + 2)){
                // found 2 straights with bbg nums
                // index of the 3 straights in totalS
                let str_suits = [];
                for (let j = 0; j < 3; j++){
                    const j_ind = totalS_u.indexOf(i_str + j);
                    const j_suit = Math.floor(totalS[j_ind][1] / 10);

                    // adding the suit to str_suits
                    str_suits[str_suits.length] = j_suit;
                }

                // no of unique items in str_suits
                const str_suits_set = new Set(str_suits);
                switch (str_suits_set.size) {
                    case 1:
                        accumulated_acc[accumulated_acc.length] = 41;
                        break
                    case 2:
                        // nothing!!
                        continue
                    case 3:
                        accumulated_acc[accumulated_acc.length] = 40;
                        break
                    default:
                        continue
                }
            }
        }

        // ladder
        if (totalS_u.length == 5){
            // run only if all straights!
            let totalS_u_sorted = totalS_u.slice(); // dupe the list
            totalS_u_sorted.sort();
            const aseq = lu.find_arithmetic_seq(totalS_u_sorted[0], totalS_u_sorted, 1);
            if (aseq.length == 5){
                accumulated_acc[accumulated_acc.length] = 42;
            }
        }
        
        // Repeated triplets (Offsuit)
        // find repeated occurences of the trips
        let offsuit_rt_dict = lu.unique_occurence_count(totalT_u);
        // add eye
        const eyeU = eyePair[0] % 10
        if (offsuit_rt_dict[eyeU] == undefined) {
            offsuit_rt_dict[eyeU] = 0.5;
        }
        else {
            offsuit_rt_dict[eyeU] = offsuit_rt_dict[eyeU] + 0.5;
        }

        for (const t of Object.keys(offsuit_rt_dict)){
            switch (offsuit_rt_dict[t]){
                case 2:
                    accumulated_acc[accumulated_acc.length] = 43;
                    break
                case 2.5:
                    accumulated_acc[accumulated_acc.length] = 44;
                    break
                case 3:
                    accumulated_acc[accumulated_acc.length] = 45;
                    break
                default:
                    continue
            }
        }

        // consec trips
        let totalT_numTiles_c = totalT_numTiles.slice();
        // sort the list
        totalT_numTiles_c.sort();
        while (totalT_numTiles_c.length > 0) {
            const aseq = lu.find_arithmetic_seq(totalT_numTiles_c[0], totalT_numTiles_c, 1);
            // returns the aseq of consec tiles starting at the smallest one
            // adds the eYe!
            let numConsec;
            if (eyePair[0] + 1 == aseq[0] || eyePair[0] - 1 == aseq[aseq.length - 1]) {
                numConsec = aseq.length + 0.5;
            }
            else {
                numConsec = aseq.length;
            }

            if (numConsec >=2 ) {
                accumulated_acc[accumulated_acc.length] = 2 * numConsec + 42;
            }

            // remove the items in aseq from the original list.
            totalT_numTiles_c.splice(0, aseq.length)
        }

        // smol old (triplet)
        for (let i = 1; i<4; i++) {
            if (totalT_numTiles.includes(Number(10*i+1)) && totalT_numTiles.includes(Number(10*i+9))){
                // has both the 1/9 triplet of the same sedo
                accumulated_acc[accumulated_acc.length] = 26;
            }
        }


        // 4 in X
        // reconstruct total tiles
        // total_Tiles = innerStraights.concat(innerTriplets, outerStraights, outerTriplets, eyePair);
        
        const tileCount = lu.unique_occurence_count(total_Tiles);

        for (const k of Object.keys(tileCount)) {
            if (!(tileCount[k] == 4)) {
                
                continue
                // skip to next k
                
            }
            // runs if tile count is 4 (4 in X) 
            // lucky tiles cannot have 4 in X so we should be fine

            if (eyePair.includes(Number(k))) {
                accumulated_acc[accumulated_acc.length] = 55;
            }
            else if ( totalT_numTiles.includes(Number(k)) ) {
                // a triplet exists
                accumulated_acc[accumulated_acc.length] = 54;
            }
            else {
                // no triplet, not in eye, only straights
                accumulated_acc[accumulated_acc.length] = 56;
            }
        }

        // suits: finding suits_present
        const set_total_Tiles = new Set(total_Tiles2);
        let suits_present = new Array(5);
        suits_present.fill(0);
        // suits_present is a array of length 5 and full of zeroes

        // eye!
        if (eyePair[0] < 40) {
            const suit_index = Math.floor(eyePair[0] / 10) - 1;
            suits_present[suit_index] = 0.5;
        }
        else if (40 < eyePair[0] && eyePair[0] < 45) {
            // wind tiles
            suits_present[3] = 0.5;
        }
        else {
            // scholar tiles
            suits_present[4] = 0.5;
        }

        // other normal kans! 

        for (const i of set_total_Tiles) {
            if (i < 40) {
                const suit_index = Math.floor(i / 10) - 1;
                suits_present[suit_index] = 1;
            }
            else if (40 < i && i < 45) {
                // wind tiles
                suits_present[3] = 1;
            }
            else {
                // scholar tiles
                suits_present[4] = 1;
            }
        }

        const num_suits = suits_present.slice(0, 3);
        const lt_suits = suits_present.slice(3,5);
        
        let sum_num_suits = 0;
        let sum_suits = 0;
        // sum of num suits
        for (let i of num_suits){
            sum_num_suits = sum_num_suits + Number(i);
            sum_suits = sum_suits + Number(i);
        }
        // sum of lt suits
        for (let i of lt_suits){
            sum_suits = sum_suits + Number(i);
        }

        // small big 5 suits
        if (sum_suits >= 4.5) {
            if (sum_suits == 5) {
                // big 5 suits
                accumulated_acc[accumulated_acc.length] = 58;
            }
            else {
                // small 5 suits
                accumulated_acc[accumulated_acc.length] = 57;
            }
        }

        if (sum_num_suits == 0) {
            accumulated_acc[accumulated_acc.length] = 62;
        }
        else if (sum_num_suits == 0.5 || sum_num_suits == 1) {
            // 1 suit only
            if (lt_suits.toString() == [0,0].toString()) {
                // no lucky tiles
                accumulated_acc[accumulated_acc.length] = 61;
            }
            else {
                accumulated_acc[accumulated_acc.length] = 60;
            }
        }
        else if (sum_num_suits == 2) {
            if (lt_suits.toString() == [0,0].toString()) {
                // no lucky tiles
                accumulated_acc[accumulated_acc.length] = 59
            }
        }

        // all triplets
        if (totalS.length == 0) {
            // runs if no straights
            if (innerT.length == 5) {
                if (sd == 0) {
                    // kan kan do not double count!
                    accumulated_acc[accumulated_acc.length] = 63;
                    // if sd = 1, then kan kan is counted already!
                }
            }
            else {
                accumulated_acc[accumulated_acc.length] = 63;
            }
        }

        // independence
        if (outerK.length == 0) {
            // no outer
            if (sd == 1) {
                accumulated_acc[accumulated_acc.length] = 66;
            }
            else {
                accumulated_acc[accumulated_acc.length] = 67;
            }
        }
        
        // all from others

        if (outerK.length == 5) {
            if (sd == 1) {
                accumulated_acc[accumulated_acc.length] = 64;
            }
            else {
                accumulated_acc[accumulated_acc.length] = 65;
            }
        }

        // yaojiu

        let yj_present = 0;
        const yj_list = [11, 19, 21, 29, 31, 39];

        for (const k of total_Tiles) {
            if (yj_list.includes(k)) {
                yj_present = 2;
                break
            }
            else if (k > 40) {
                yj_present = 2;
                break
            }
        }

        if (yj_present == 0) {
            accumulated_acc[accumulated_acc.length] = 68;
        }
        

        // if no yj + lucky tiles, yj_present = 0, otherwise = 2
        if (yj_present == 2){
            let all_yj = true;

            let is_yj;
            for (kan of totalS.concat(totalT)) {
                is_yj = false;
                for (const tile of kan) {
                    if (yj_list.includes(tile) || tile > 40) {
                        is_yj = true;
                        break
                    } 
                } // is_yj stays false if none of the tiles in kan are yj/lucky tiles
            
                if (is_yj == false) {
                    // not yj
                    all_yj = false;
                    break
                    // sets all yj to false and breaks the loop
                }
            }

            if (!yj_list.includes(eyePair[0]) && eyePair[0] < 40) {
                all_yj = false;
            }

            if (all_yj) {
                // 連/純連/花/清
                if (totalS.length == 0) {
                    if (windTileCount+scholarCount == 0) {
                    // no lucky tiles!! + all triplets
                        accumulated_acc[accumulated_acc.length] = 72;
                    } else {
                        accumulated_acc[accumulated_acc.length] = 71;
                    }
                }
                else if (windTileCount+scholarCount == 0){
                    // no lucky tiles! + some straights w/ 1/9 in all of them and some 1/9 triplets
                    accumulated_acc[accumulated_acc.length] = 70;
                }
                else{
                    accumulated_acc[accumulated_acc.length] = 69;
                }

                }
            
        }

        if (sd) {
            accumulated_acc[accumulated_acc.length] = 74;
        }

        // counting up the final scores
        const finalResult = await acc_class.sum_accolades(accumulated_acc, fl_score, windScore, scholarScore)

        return finalResult;
        
    }




