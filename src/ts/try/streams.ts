// stream.ts - try out ideas for data streams
// a sort of 'lightweight filing system'

// an API that allows you to index into any instance of static read only data
// i.e. an open file pointer

//TODO: we really want this API interchangeable with reading chars from serial
//so that our input stream could be stdin or from stored file.
//that might be too 'big' a design for this tiny system?
//but it means that most of the API is about streaming

//TODO: need to work out how to do error handling.
//null is the same as zero, and there are no exceptions!

interface InputStream {
    isEnd(): boolean;
    readLine(): string;
    readChar(): string;
    putBack(data: string): void;
}


class ReadOnlyFile
    implements InputStream {
    data: string
    pos: number
    eof: boolean

    //file
    constructor(data: string) {
        this.data = data // is this a reference or a copy?
        this.pos = 0 // start of file
        this.eof = false
    }

    //file
    length(): number {
        // get the filesize
        return this.data.length()
    }

    //file
    getPos(): number {
        // get the current file pos
        return this.pos
    }

    //file
    setPos(pos: number) {
        // set the current file pos
        if (pos < 0 || pos > this.data.length) {
            // raise error
        } else {
            this.pos = pos
        }
    }

    //file
    reset(): void {
        this.eof = false
        this.pos = 0
    }

    //stream?
    isEnd(): boolean {
        // work out if hit end of file or not
        return this.eof
    }

    //stream
    readLine(): string {
        // read characters until EOLN or EOF
        // if already eof, raise an error?
        // maintain eof flag if now hit end of file
        // return what we just read as a copy, to the caller
        return ""
    }

    //stream
    readChar(): string {
        // read a single char
        // if already EOF, raise an error
        // advance pointer by one, maintain eof flag
        // return string with single char in it
        if (this.pos < this.data.length) {
            let ch = this.data[this.pos]
            this.pos += 1
            return ch
        }
        this.eof = true
        return "" //TODO: read past eof
    }

    //stream
    putBack(data: string): void {
        // putback 1 or more characters, useful for lookahead parsers
        // validate that what is being put back is correct
        // validate we are not putting back beyond start of string
        // if bad, raise an error
        // wind back pos by the length of this string
    }
}




// some static readonly data
// i.e. the raw file data
// this is probably in flash and RAM, not much we can do about that.

let file1:string = "10\n20\n30\n"


// reading and processing data from a stream
// i.e. the app

let f = new ReadOnlyFile(file1)

while (! f.isEof()) {
    s = f.readLine()
    basic.showString(s)
    basic.pause(250)
}
