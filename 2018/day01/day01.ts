/*
 * Problem 1 of the Advent-of-Code 2018
 */

import * as fs from 'fs';
import * as readline from 'readline';
export {}

const readInterface = readline.createInterface({
    input: fs.createReadStream('input.txt'),
    output: null
});

var input = []

readInterface.on('line', (line: string) => {
    input.push(parseInt(line, 10))
})

const reduce_function = (a: number, current_value: number) => a + current_value;

readInterface.on('close', () => {
    console.log("Part A: " + part_a(input).toString());
    console.log("Part B: " + part_b(input).toString());
})

function part_a(input_array: Array<number>): number {
    return input_array.reduce(reduce_function, 0);
}

function part_b(input_array: Array<number>): number {
    var hist: Set<number> = new Set();
    var current_value: number = 0;
    while (true) {
        for (var i = 0; i < input_array.length; i++) {
            current_value += input_array[i];
            if (hist.has(current_value)) {
                return current_value
            }
            hist.add(current_value)
        }
    }
}
