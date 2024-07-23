class acc {
    constructor(name, pts, double_on_conceal) {
        this.name = name;
        this.pts = pts;
        this.double_on_conceal = double_on_conceal;
    }
}

// initialising the class

export async function load_acc_dict() {
    const table = await fetch('./tw_accolades_info.json');
    const tableJ = await table.json();
    
    const keys = Object.keys(tableJ);
    
    // priming the output vector
    let acc_vector = [];
    
    for (const k of keys) {
        const ac_name = tableJ[k]["acco_name"]
        const ac_pts = tableJ[k]["points"]
        const ac_double = tableJ[k]["double_on_conceal"]
        acc_vector[acc_vector.length] = new acc(ac_name, ac_pts, ac_double)
    }
    
    return acc_vector
}

export async function flower_count(seat, flower) {
    // make sure to load accolades before executing this function
    const accolade = await load_acc_dict();
    // flowers
    let flower_working = flower.slice();
    let fl_acc = [];

    if (flower_working.length == 0) {
        // no flowers (non-destructive to the list!!)
        fl_acc[fl_acc.length] = 0;
    }

    // sort the flowers (destructive to the list!)
    flower_working.sort();
    if (flower_working.length >= 4){
        // check for collections
        if (flower_working.length == 8) {
            // all 8 flowers
            fl_acc[fl_acc.length] = 4;
        }
        else if (flower_working.slice(0,4).toString() == [1, 2, 3, 4]) {
            // check first 4 flowers
            fl_acc[fl_acc.length] = 3;
            // delete the flowers from the below counting
            flower_working.splice(0,4)
        }
        else if (flower_working.slice(fl.length-4, fl.length).toString() == [5, 6, 7, 8]) {
            // check last 4 flowers
            fl_acc[fl_acc.length] = 3;
            // delete the flowers from the below counting
            flower_working.splice(flower_working.length-4, flower_working.length)
        }
        
    }

    // eval for remaining flowers
    let fl_score = 0;
    if (flower_working.length) {
        fl_acc[fl_acc.length] = 1;
        // add temp bad flower accolade to the list for final text output
    }
    for (const fl of flower_working) {
        if ((fl%4) == (seat%4)) {
            fl_score = fl_score + accolade[2].pts;
        }
        else{
            fl_score = fl_score + accolade[1].pts;
        }
    }

    return new Array(fl_score, fl_acc)
}


export async function sum_accolades(acc_list, fs=0, ws=0, ss=0) {
    const accolade = await load_acc_dict();
    // sums up all the accolades in the list
    // adds the base in this function as well
    let Score = 0;
    let Acc_txt = '';
    for (const id of acc_list) {
        switch (id) {
            case 1:
                Score = Score + fs
                Acc_txt = Acc_txt + ('Flowers' + ' - ' + fs) + '<br>';
                continue
            case 5:
                Score = Score + ws;
                Acc_txt = Acc_txt + ('Wind Tiles' + ' - ' + ws) + '<br>';
                continue
            case 14:
                Score = Score + ss;
                Acc_txt = Acc_txt + ('Scholar Tiles' + ' - ' + ss) + '<br>';
                continue
            default:
                Score = Score + Number(accolade[id].pts);
                Acc_txt = Acc_txt + (accolade[id].name + ' - ' + accolade[id].pts) + '<br>';
                continue
        } 
    }

    if (Score <= 1) {
    // chicken
        const accumulated_acc = [73,75];
        for (id of accumulated_acc) {
            Score = Score + Number(accolade[Number(id)].pts);
            Acc_txt = Acc_txt + accolade[id].name + '<br>';
        }
    }

    else {
        // add base
        Score = Score + Number(accolade[75].pts);
        Acc_txt = Acc_txt + accolade[75].name + ' - ' + accolade[75].pts;
    }

    return new Array(Score, Acc_txt)
}