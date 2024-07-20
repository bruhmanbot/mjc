import { score_count_A } from './counterA.js';
import { validityCheck } from './validityCheckJS.js';


async function eval_hand(){
    const validityResults = validityCheck(inner_arr, outer_arr, winner_arr);

    if (validityResults[0] == 0) {
        document.getElementById('accolades').innerHTML = 'Cheating!! - -300'
        document.getElementById('score').innerHTML = '-300'
        return 
        // end the function if not valid
    }

    console.log(validityResults.slice())

    // runs only if hand is valid
    // assign vars for score_count_A
    const is = validityResults[1];
    const it = validityResults[2];
    const os = validityResults[3];
    const ot = validityResults[4];
    const eye = validityResults[5];

    const fsd = 1;
    const fwind = 1;
    const fseat = 1;
    const fflower = [];

    const scoreA_results= await score_count_A(is, it, os, ot, eye, winner_arr, 
        fsd, fwind, fseat, fflower);
    
    // outputs

    const sc = scoreA_results[0];

    const accolade_output_txt = scoreA_results[1];


    // set txt
    document.getElementById('accolades').innerHTML = accolade_output_txt;
    document.getElementById('score').innerHTML = sc;

    
}



// binding the function to the eval_button
document.getElementById('eval_button').addEventListener('click', eval_hand);
