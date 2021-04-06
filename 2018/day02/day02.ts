/*
 * Problem 2 of the Advent-of-Code 2018
 */

import * as fs from 'fs';
import * as readline from 'readline';
export {}

const readInterface = readline.createInterface({
    input: fs.createReadStream('input.txt'),
    output: null
});

var input: Array<any> = []

readInterface.on('line', (line: string) => {
    input.push(line)
})

readInterface.on('close', () => {
    console.log("Part A: " + part_a(input).toString());
    console.log("Part B: " + part_b(input).toString());
})

function part_a(input_array: Array<string>): number {
    var num_twins: number = 0;
    var num_triplets: number = 0;

    /* For each input string */
    for (var i = 0; i < input_array.length; i++) {
        var count: Object = {};
        var id: string = input_array[i];
        /* Build up a count of each letter */
        for (var j = 0; j < id.length; j++) {
            var letter: string = id[j];
            if (!(letter in count)) {
                count[letter] = 1;
            } else {
                count[letter] += 1;
            }
        }

        /* Check if there are twins or triplets */
        if (are_there_twins(count)) {
            num_twins += 1;
        }
        if (are_there_triplets(count)) {
            num_triplets += 1;
        }
    }

    return num_twins * num_triplets;
}

/* Returns true if the object has a [key, value] pair where the value == 2 */
function are_there_twins(dict: Object): boolean {
    for (const key in dict) {
        if (dict[key] == 2) {
            return true;
        }
    }
    return false;
}

/* Returns true if the object has a [key, value] pair where the value == 3 */
function are_there_triplets(dict: Object): boolean {
    for (const key in dict) {
        if (dict[key] == 3) {
            return true;
        }
    }
    return false;
}

function part_b(input_array: Array<string>): number {
    return 0;
}
