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
                Score = Score + Number(accolade[Number(id)].pts);
                Acc_txt = Acc_txt + (accolade[id].name + ' - ' + accolade[id].pts) + '<br>';
                continue
        } 
    }

    if (Score <= 1) {
    // chicken
        accumulated_acc = [73,75];
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