import * as lu from './listUtilsJS.js';

function score_count_A(innerStraights, innerTriplets, outerStraights, outerTriplets, eyePair, winningTile,
    sd, wind, seat, flower) {
        const innerS = lu.split_list(innerStraights, 3);
        const innerT = lu.split_list(innerTriplets, 3);
        const outerS = lu.split_list(outerStraights, 3);
        const outerT = lu.split_list(outerTriplets, 3);
        
        const innerK = innerS.concat(innerT);
        const outerK = outerS.concat(outerT);

        // other vars
        let Score = 0

        // wind tiles
        let windTileCount = 0;
        let windScore = 0;
        for (kan of innerT.concat(outerT)){
            if (40 < kan[1] < 45) {
                windTileCount ++;
                if (kan[1] % 10 == seat){
                    windScore ++; // seat bonus
                }
                if (kan[1] % 10 == wind){
                    windScore ++; // wind bonus
                }
            }
        }
        
        // eye
        if (40 < eyePair[1] < 45) {
            windTileCount = windTileCount + 0.5;
        }

        // scholar tiles
        let scholarCount = 0;
        let scholarScore = 0;

        for (kan of innerT.concat(outerT)){
            if (45 <= kan[1] < 48) {
                scholarCount ++;
            }
        }
        
        // eye
        if (45 <= eyePair[1] < 48) {
            scholarCount = scholarCount + 0.5;
        }

        // winds & scholar bonuses
        if (windTileCount + scholarCount == 0){
            // no characters
            console.log('no chars')
        }
        else {
            switch (windTileCount){
                case 4:
                    // 4 big winds
                    windScore = 150;
                    console.log("4 big winds");
                case 3.5:
                    // 4 smol winds
                    windScore = 120;
                    console.log("4 big winds");
                case 3:
                    // 3 big winds
                    windScore = 40;
                    console.log("3 big winds"); 
                case 2.5:
                    // 4 big winds
                    windScore = 20;
                    console.log("3 smol winds") 
                default:
                    // add windscore
                    windScore = Math.floor(windTileCount)       
            }
    
            // scholar
            switch (scholarCount){
                case 3:
                    // 3 big scholar
                    scholarScore = 80;
                    console.log("3 big scholars");
                case 2.5:
                    // 3 smol scholar
                    scholarScore = 40;
                    console.log("3 smol scholars");
                default:
                    // add windscore
                    scholarScore = Math.floor(scholarCount) * 2;       
            }
        }
        // accumulation of scores
        Score = Score + windScore + scholarScore;

        // 1 in 2
        let checkdudu = true;
        for (triplet of innerT) {
            if (winningTile == triplet[1]){
                // winning on the triplet e.g. 22 55 get 2/5
                console.log('1 in 2');
                checkdudu = false;
            }
        }
        
        // dudu
        let dudu = 0;
        let fakedudu = 0;
        if (checkdudu) {
            for (kan of innerK) {
                // in the middle
                if (winningTile == kan[1]){
                    dudu = 1;
                    break
                }
    
                // 3 or 7 edge tile
                else if (winningTile < 40 && (winningTile % 10 == 3)){
                    if (winningTile == kan[2]){
                        fakedudu = 1;
                        break
                    }                
                }
                else if (winningTile < 40 && (winningTile % 10 == 7)){
                    if (winningTile == kan[0]){
                        fakedudu = 1;
                        break
                    }                
                }
                // eye 
                else if (eyePair.include(winningTile)){
                    dudu = 1;
                    if (kan.include(winningTile)) {
                        fakedudu = 1;
                    }
                    else if (Math.abs(winningTile - kan[1]) == 2 && lu.same_suit(kan[1], winningTile)) {
                        fakedudu = 1;
                    }
                }
            }
        }

        if (fakedudu) {
            console.log('fakedudu')
        }
        else if (dudu) {
            console.log('dudu')
        }
        
        // general eye
        if ([2,5,8].includes(eyePair[0] % 10) && eyePair[0] < 40) {
            console.log('general eye')
        }

        // all straight
        if (innerT.length + outerT.length == 0) {
            console.log('all straight!')
        }

        

        
    }