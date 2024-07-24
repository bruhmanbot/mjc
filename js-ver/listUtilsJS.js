export function split_list(list, chunk) {
    // splits a list(array) into chunks size specified by the chunk size
    let output_chunks = [];
    let chunk_to_add = [];
    let input_list_dupe = list;
    while (input_list_dupe.length > 0) {
        // while the input list still has items
        // adds items until chunk to add is "full"
        while (chunk_to_add.length < chunk) {
            // adds the new item (first remaining item in input list) to the chunk
            chunk_to_add[chunk_to_add.length] = input_list_dupe[0];
            input_list_dupe.shift();
        }

        // when chunk to add is the length required
        output_chunks[output_chunks.length] = chunk_to_add;
        chunk_to_add = [];
    }
    return output_chunks;
}

export function same_suit(item1, item2) {
    return (Math.floor(item1/10) == Math.floor(item2/10));
}

export function set_containslists(list, set_search){
    // considers all the items in a list and see if ALL of them are in set_search
    for (const item of list) {
        if (!(set_search.includes(item))) {
            return false;
        }
    }
    return true
}

export function count(item, list){
    // returns the number of occurences of an item in a said list
    const count = list.filter((ele) => ele == item)
    return count.length
}

export function unique_occurence_count(list){
    // returns the occurence of each item in the list inside a dictionary
    let occ_dict = {};

    for (let item of list){
        if (occ_dict[item] == undefined){
            // Initialises the count if not inside dictionary
            occ_dict[item] = 1;
        }
        else{
            // adds one to count if already present
            occ_dict[item] ++;
        }
        
    }

    return occ_dict
}

export function find_occurence(occurence, list_search){
    // finds items inside a list which has appeared (occurence) amount of times
    let count_dict = unique_occurence_count(list_search);
    let uitem_list = Object.keys(count_dict);
    let output_list = [];
    for (uitem of uitem_list){
        if (count_dict[uitem] == occurence){
            output_list[output_list.length] = uitem;
        }
    }
    return output_list;
}

export function find_index_duplicate_item(item, list_search){
    // finds the index (indices) of an item in a list
    // outputs the indices to an array
    let indices_array = [];
    let begin_index = 0;
    while (true){
        const item_index = list_search.indexOf(item, begin_index);
        if (item_index == -1){
            // case for no more occurences
            return indices_array;
            // break and return the array
        }
        // else
        indices_array[indices_array.length] = item_index;
        begin_index = item_index + 1;
    }
}

export function find_arithmetic_seq(start, list_search, interval){
    // finds an arithemetic sequence (the longet one) of a bunch of numbers in a list
    // returns said arithmetic sequence in a list
    let aseq_list = [start];
    let next_term = start+interval;
    let next_term_exists = list_search.includes(next_term);


    while (next_term_exists){
        aseq_list[aseq_list.length] = next_term;
        next_term += interval;
        // See if another term exists afterwards
        next_term_exists = list_search.includes(next_term);
    }

    return aseq_list

}

export function list_type_check(list1, type1){
    // sees if all of the items in the list1 is of type type1
    let item;
    for (item of list1){
        if (typeof(item) != type1){
            return false
        }
    }
    return true
}

export function straight_split(list2) {
    // identifies the straights in list2
    // outputs the identified straights in output_list[0]
    // spits the remaining numbers in output_list[1]
    let kan = [];
    let list_operation = list2.slice();
    list_operation.sort()
    let k = 0
    let straight_start = null;
    while (k < list_operation.length){
        // find if a straight exists
        if (list_operation.includes(list_operation[k]+1) && 
        list_operation.includes(list_operation[k]+2))  {
            // straight exists, adds the terms to kan and removes from list_op.
            straight_start = list_operation[k];
            
            for (let i=0; i<3; i++){
                kan[kan.length] = straight_start + i;
                // finds the index of the added item to kan
                let index_removal = list_operation.indexOf(straight_start + i);
                list_operation.splice(index_removal,1); 
                // removes the item from list_op
            }
            k = 0;
        }
        else {
            k++
        }
    }

    let output = new Array(kan, list_operation)
    return output
}

export function triplet_split(list2){
    let triplets = [];
    let list_op = list2.slice();
    list_op.sort();
    let k = 0;
    while (k < list2.length) {
        if (count(list_op[k], list_op) > 2){
            // identifies the triplets
            let add_arr = new Array(3)
            add_arr.fill(list_op[k])
            // list of len 3 with the correct value of list_op[k]
            triplets = triplets.concat(add_arr)
            // appends add_arr to the end of the existing triplets

            // removing the triplet from list_op
            list_op.splice(k, 3) 
        }
        else{
            k++
        }
    }
    const output = new Array(triplets, list_op);
    return output
}

export function element_appear_more_than_n_times_find(list, n){
    // finds the item in a list appearing equal or more than n_times and puts them into a list
    let ini_output = [];
    let item;
    for (item of list) {

        if (ini_output.includes(item)){
            continue
        }

        if (count(item, list) >= n) {
            ini_output[ini_output.length] = item;
        }
    }

    return ini_output
}

export function list_unpack(list){
    // unpacks nested list
    let unpacked = [];
    let nested;
    for (nested of list){
        for (ele of nested){
            unpacked[unpacked.length] = ele;
        }
    }
    return unpacked;
}


export function matrix_diag(matrix) {
    // calculate sum of diag of a 3*3 matrix
    // bottom right
    let sum_diag = 0;
    // main diagonal
    for (let i=0; i<3; i++){
        let d = matrix[0][i] * matrix[1][(i+1)%3] * matrix[2][(i+2)%3]
        if (d>=2){
            d = Math.floor(d/2);
        }
        sum_diag = sum_diag + d
    }

    // upper left
    for (let i=0; i<3; i++){
        let d = matrix[2][i] * matrix[1][(i+1)%3] * matrix[0][(i+2)%3]
        if (d>=2){
            d = Math.floor(d/2);
        }
        sum_diag = sum_diag + d
    }

    return sum_diag
}
