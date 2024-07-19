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

