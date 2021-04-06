/*
 * Problem 1 of the Advent-of-Code 2018
 */

import * as fs from 'fs';
import * as readline from 'readline';
export {}

const readInterface = readline.createInterface({
    input: fs.createReadStream('input.txt'),
    output: null,
    console: false
});

var input: Array<any> = []

readInterface.on('line', (line: string) => {
    input.push(parseInt(line, 10))
})

readInterface.on('close', () => {
    console.log("Part A: " + part_a(input).toString());
    console.log("Part B: " + part_b(input).toString());
})

function part_a(input_array: Array<number>): number {
    return 0;
}

function part_b(input_array: Array<number>): number {
    return 0;
}
