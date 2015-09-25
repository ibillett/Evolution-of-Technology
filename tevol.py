from logic_gates import not_, and_, or_, xor_, half_
import itertools
import unittest
import random
import string
import sys
import pdb

gates = [half_]

class Connector:
    """
      Connectors are inputs and outputs. Only outputs should connect
      to inputs. Be careful NOT to have circular references
      As an output is changed it propagates the change to its connected inputs
    """
    def __init__(self, owner, name):
        self.id = id(self)
        self.value = None
        self.owner = owner
        self.name = name
        self.connects = []

    def connect(self, inputs):
        if type(inputs) != type([]):
            inputs = [inputs]
        for input in inputs:
            self.connects.append(input)

    def set(self, value):
        #print("setting value of {} {} to {}".format(type(self.owner).__name__, self.name, value))
        if self.value == value:
            return                    # Ignore if no change
        self.value = value
        self.owner.evaluate()
        for con in self.connects:
            con.set(value)
            con.owner.evaluate()

class Input(Connector):
    def __init__(self, owner, name):
        Connector.__init__(self, owner, name)

    def __repr__(self):
        return "{} {} {}".format(self.owner.name, self.__class__.__name__, self.name)

class Output(Connector):
    def __init__(self, owner, name):
        Connector.__init__(self, owner, name)

    def __repr__(self):
        return "{} {} {}".format(self.owner.name, self.__class__.__name__, self.name)

class Nand:
    def __init__(self):
        self.id = id(self)
        self.name = "{} {}".format(self.__class__.__name__, self.id % 100)
        self.i = [Input(self, string.ascii_uppercase[i]) for i in range(0,2)]
        self.o = [Output(self, 'A')]

    def __repr__(self):
        return "{} {}".format(self.__class__.__name__, self.id % 100)

    def evaluate(self):
        self.o[0].set(not(self.i[0].value and self.i[1].value))

class IO:
    def __init__(self, input_length, output_length):
        self.id = id(self)
        self.name = "IO"
        self.ilen = input_length
        self.olen = output_length
        self.table = ["".join(seq) for seq in itertools.product("01", repeat=self.ilen)]
        self.i = [Input(self, string.ascii_uppercase[i]) for i in range(0,self.ilen)]
        self.o = [Output(self, string.ascii_uppercase[i]) for i in range(0,self.olen)]

    def calc(self):
        """ Calculate the output values generated from the input """
        results = {}
        for row in self.table:
            #print("Setting inputs to {}".format(row))
            self.set(row)
            #print("{} : {}".format(row,self.out()))
            results[row] = self.out()
        return results

    def set(self, inp):
        """ Set the values of the input array """
        assert len(inp) == self.ilen
        for i in range(len(inp)):
            self.i[i].set(int(inp[i]))

    def out(self):
        """ Return the output(o) array """
        return "".join([str(int(o.value)) for o in self.o])

    def evaluate(self):
        pass

def creates_loop(o,i):
    end = o.owner
    start = i.owner
    if start == end:
        return True

    for out in start.o: #There should only be one output with a Nand gate
        for con in out.connects:
            if con.owner == end or creates_loop(con,i):
                return True
    return False

def match(res):
    for gate in gates:
        if gate == res:
            return True
    return False

if __name__ == '__main__':

    result = []
    results = []
    count = []
    iteration = 0

    while not match(result):

        io = IO(2,2)
        inputs = list(io.i)  # Creates copy of IO inputs
        outputs = list(io.o) # Creates copy of IO outputs
        connections = []
        n = Nand()
        inputs += n.o

        while outputs != []:
            o = outputs.pop(random.randrange(len(outputs)))
            i = random.choice(inputs)

            while creates_loop(o,i):
                i = random.choice(inputs)

            i.connect(o)
            connections.append((i,o))

            if type(i.owner) == Nand:
                outputs += i.owner.i
                n = Nand()
                inputs += n.o

        result = io.calc()

        if result in results:
            index = results.index(result)
            count[index] += 1
        else:
            results.append(result)
            count.append(0)
        # print("Inputs: {}\nOutputs: {}\nConnections: {}".format(inputs,outputs,connections))
        iteration += 1
        if iteration % 100 == 0:
            print("Iteration {}".format(iteration))

    print(result,iteration)
