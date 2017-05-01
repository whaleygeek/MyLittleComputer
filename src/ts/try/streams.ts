// stream.ts - try out ideas for data streams a sort
// of 'lightweight filing system' an API that allows
// you to index into any instance of static read only
// data i.e. an open file pointer TODO: need to work
// out how to do error handling. null is the same as
// zero, and there are no exceptions!

interface InputStream {
    isEnd(): boolean;
    readLine(): string;
    readChar(): string;
    putBack(data: string): void;
}
interface OutputStream {
    write(s: string): void;
    writeLine(s: string): void
}
class IOStream implements InputStream, OutputStream {
    inp: InputStream
    out: OutputStream

    constructor(inp: InputStream, out: OutputStream) {
        this.inp = inp
        this.out = out
    }
    isEnd(): boolean {
        return this.inp.isEnd()
    }
    readLine(): string {
        return this.inp.readLine()
    }
    readChar(): string {
        return this.inp.readChar()
    }
    putBack(data: string): void {
        this.inp.putBack(data)
    }
    write(s: string) {
        this.out.write(s)
    }
    writeLine(s: string) {
        this.out.writeLine(s)
    }
}
class ScreenOutputStream implements OutputStream {
    constructor() { }

    write(s: string) {
        basic.showString(s)
    }
    writeLine(s: string) {
        basic.showString(s)
        basic.pause(200)
        basic.clearScreen()
    }
}
class SerialOutputStream implements OutputStream {
    constructor() { }

    write(s: string) {
        serial.writeString(s)
    }

    writeLine(s: string) {
        serial.writeLine(s)
    }
}
interface File {
    length(): number;
    getPos(): number;
    setPos(pos: number): void;
    reset(): void;
}
class ReadOnlyFile
    implements InputStream, File {
    data: string
    pos: number
    eof: boolean

    constructor(data: string) {
        this.data = data // is this a reference or a copy?
        this.pos = 0 // start of file
        this.eof = false
    }

    length(): number {
        // get the filesize
        return this.data.length()
    }

    getPos(): number {
        // get the current file pos
        return this.pos
    }

    setPos(pos: number) {
        // set the current file pos
        if (pos < 0 || pos > this.data.length) {
            // raise error
        } else {
            this.pos = pos
        }
    }

    reset(): void {
        this.eof = false
        this.pos = 0
    }

    isEnd(): boolean {
        // work out if hit end of file or not
        return this.eof
    }

    readLine(): string {
        // read characters until EOLN or EOF
        // if already eof, raise an error?
        if (this.eof) {
            // raise error
            return ""
        } else {
            let line = ""
            let c = ""
            while (c != '\n' && !this.eof) {
                c = this.readChar()
                if (!this.eof) {
                    line += c
                }
            }
            return line
        }
    }

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

    putBack(data: string): void {
        // putback 1 or more characters, useful for lookahead parsers
        // validate that what is being put back is correct
        // validate we are not putting back beyond start of string
        // if bad, raise an error
        // wind back pos by the length of this string
    }
}
class SerialInputStream implements InputStream {
    line: string
    lpos: number

    constructor() {
        this.line = ""
        this.lpos = 0
    }

    isEnd(): boolean {
        // Serial never generates EOF
        return false
    }

    readLine(): string {
        //blocking
        return serial.readLine()
    }

    readChar(): string {
        //blocking
        if (this.lpos >= this.line.length) {
            this.line = this.readLine()
            this.lpos = 0
        }
        let d = this.line[this.lpos]
        this.lpos += 1
        return d
    }

    putBack(data: string): void {
        //TODO: unimplemented
    }
}

// TESTER
let i = new SerialInputStream()
let o = new SerialOutputStream()
let terminal = new IOStream(i, o)
while (true) {
    terminal.write("command>")
    let cmd = terminal.readLine()
    basic.showString(cmd)
}
