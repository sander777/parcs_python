from Pyro4 import expose

from_char, to_char = 48, 122
range_char = to_char-from_char+1
class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        (key, str) = self.read_input()
        splited = Solver.div_string(str, len(self.workers))
        mapped = []
        for i in xrange(len(splited)):
            (s, ix) = splited[i]
            mapped.append(self.workers[i].mymap(s, key, ix))
        reduced = Solver.myreduce(list(mapped))
        self.write_output(reduced)

    @staticmethod
    @expose
    def mymap(a, key, ix):
        code = Solver.encode(a, key, ix)
        decode = Solver.decode(code, key, ix)
        return (code, decode)

    @staticmethod
    @expose
    def myreduce(mapped):
        code = ''
        decode = ''

        for i in mapped:
            c, d = i.value
            code += c
            decode += d
        return (code, decode)

    def read_input(self):
        f = open(self.input_file_name, 'r')
        key = f.readline().strip()
        lines = f.read().strip()
        f.close()
        return (key, lines)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        code, decode = output
        f.write(code)
        f.write('\n')
        f.write(decode)
        f.close()
        print("output done")

    @staticmethod
    @expose
    def encode(string, key, ix):
        res = ''
        for i in range(len(string)):
            if string[i] == ' ':
                res+=string[i]
            else: 
                c = Solver.echar(ord(string[i]), ord(key[(i + ix) % len(key)]))
                res += chr(c)
        return res

    @staticmethod
    @expose
    def div_string(string, workres):
        res = []
        step = int(len(string) / workres)
        d = len(string) % step
        for i in range(workres-1):
            res.append((string[i*step:i*step+step], i * step))
        res.append((string[(workres - 1)*step:], step*(workres - 1)))
        return res


    @staticmethod
    @expose
    def decode(string, key, ix):
        res = ''
        for i in range(len(string)):
            if string[i] == ' ':
                res+=string[i]
            else: 
                res += chr(Solver.dchar(ord(string[i]), ord(key[(i + ix) % len(key)])))
        return res
    
    @staticmethod
    @expose
    def echar(l, r):
        s = (l-from_char) + (r-from_char)
        return from_char + s % range_char

    @staticmethod
    @expose
    def dchar(l, r):
        s = l - r
        return s + from_char if s >= 0 else to_char + s + 1