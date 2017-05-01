//NOTE: This was an experiment
//The latest code is now in ../custom.ts

//TESTING: input and output format parsing

function print(m:string) {
    basic.showString(m)
}


function format10(n:number, width=3, zeroPad=true, signed=true):string {
    // if zero padding, work out how many zeros to add first
    let result = ""
    let neg:boolean = n<0
    n = Math.abs(n) // strip any sign
    let err:boolean = false

    if (! signed && neg) {
        err = true
    }

    // SIGN
    if (neg) {
        result = "-"
    }

    let value = n.toString()

    // ZEROPAD
    if (zeroPad) {
        let len = value.length + result.length
        if (len < width) {
            let numz = width - len
            for (;numz > 0; numz--) {
                result += "0"
            }
        }
    }
    // VALUE
    result += n.toString()

    // LENGTH CHECK
    if (result.length > width) {
        err = true
    }

    // ERROR HANDLING
    if (err) {
        result = ""
        for (let i=0; i<width; i++) {
            result += '*'
        }
    }

    return result
}

function parse10(s:string):number {
    return parseInt(s)
}

// decimal output with zeropad
let i = 123
let s = format10(i)
print(s)



// do these last

// hex output with zeropad

// hex input with zeropadstrip

// binary output with zeropad

// binary input with zeropadstrip