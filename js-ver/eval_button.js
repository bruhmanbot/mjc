import { score_count_A } from './counterA.js';
import { validityCheck } from './validityCheckJS.js';
import * as bd from './buddha.js';


async function eval_hand(){

    // running the 3 validity checks
    const validityResultsA = validityCheck(inner_arr, outer_arr, winner_arr);
    const validityResultsB = bd.buddhaCheck(inner_arr, outer_arr, winner_arr);
    

    if (validityResultsA[0] + validityResultsB[0] == 0) {
        document.getElementById('accolades').innerHTML = 'Cheating!! - -300'
        document.getElementById('score').innerHTML = '-300'
        return 
        // end the function if not valid
    }

    // load params for score counting
    const fsd = 1; // self drawn
    const fwind = 1; // wind
    const fseat = 1; // seat
    const fflower = fl; // flowers
    // later link to website input!!
    
    if (validityResultsA[0]) {
        // runs only if hand is valid
        // assign vars for score_count_A

        const is = validityResultsA[1];
        const it = validityResultsA[2];
        const os = validityResultsA[3];
        const ot = validityResultsA[4];
        const eye = validityResultsA[5];

        

        const scoreA_results= await score_count_A(is, it, os, ot, eye, winner_arr, 
            fsd, fwind, fseat, fflower);
        
        // outputs
    
        const sc = scoreA_results[0];
    
        const accolade_output_txt = scoreA_results[1];
    
    
        // set txt
        document.getElementById('accolades').innerHTML = accolade_output_txt;
        document.getElementById('score').innerHTML = sc;
    }

    if (validityResultsB[0] == 1) {
        // buddha
        const numTiles = Array.from(validityResultsB[1]);
        const eye = validityResultsB[2];

        // run score count
        const scoreB_results = await bd.score_count_b(numTiles, eye, winner_arr, fsd, fwind, fseat, fflower);

        // allocate the results
        const sc_b = scoreB_results[0];
        const accolade_output_txt_b = scoreB_results[1];

        // set txt
        document.getElementById('accolades').innerHTML = accolade_output_txt_b;
        document.getElementById('score').innerHTML = sc_b;
    }
    else if (validityResultsB[0] == 2) {
        // 13 orphans
        const remKan = validityResultsB[1];
        const eye = validityResultsB[2];

        // run score count
        const score13_results = await bd.score_count_13(remKan, eye, winner_arr, fsd, fwind, fseat, fflower);

        // allocate results
        const sc_13 = score13_results[0];
        const accolade_output_txt_13 = score13_results[1];

        // output txt
        document.getElementById('accolades').innerHTML = accolade_output_txt_13;
        document.getElementById('score').innerHTML = sc_13;
    }
    
    

    
    

    

    
}



// binding the function to the eval_button
document.getElementById('eval_button').addEventListener('click', eval_hand);
