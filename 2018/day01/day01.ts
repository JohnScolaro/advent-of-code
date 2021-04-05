const fs = require('fs')
const readline = require('readline');

const readInterface = readline.createInterface({
    input: fs.createReadStream('input.txt'),
    output: null,
    console: false
});

var input = []

readInterface.on('line', (line) => {
    input.push(parseInt(line, 10))
})

const reducer = (a, current_value) => a + current_value;

readInterface.on('close', () => {
    console.log(input.reduce(reducer, 0))
})
