from tevol import Connector, Nand, IO, creates_loop
import unittest

class TestCircuits(unittest.TestCase):
    def test_not(self):
        io = IO(1,1)
        a = Nand()

        io.i[0].connect(a.i[0])
        io.i[0].connect(a.i[1])
        a.o[0].connect(io.o[0])
        results = io.calc()
        self.assertEqual(results, {'0': '1',
                                   '1': '0'})

    def test_or(self):
        io = IO(2,1)
        a = Nand()
        b = Nand()
        c = Nand()

        io.i[0].connect(a.i[0])
        io.i[0].connect(a.i[1])

        io.i[1].connect(b.i[0])
        io.i[1].connect(b.i[1])

        a.o[0].connect(c.i[0])
        b.o[0].connect(c.i[1])

        c.o[0].connect(io.o[0])

        results = io.calc()
        self.assertEqual(results, {'00': '0',
                                   '01': '1',
                                   '10': '1',
                                   '11': '1'})

    def test_and(self):
        io = IO(2,1)
        a = Nand()
        b = Nand()

        io.i[0].connect(a.i[0])
        io.i[1].connect(a.i[1])

        a.o[0].connect(b.i[0])
        a.o[0].connect(b.i[1])

        b.o[0].connect(io.o[0])

        results = io.calc()
        self.assertEqual(results, {'00': '0',
                                   '01': '0',
                                   '10': '0',
                                   '11': '1'})

    def test_xor(self):
        io = IO(2,1)
        a = Nand()
        b = Nand()
        c = Nand()
        d = Nand()

        io.i[0].connect(a.i[0])
        io.i[0].connect(b.i[0])

        io.i[1].connect(a.i[1])
        io.i[1].connect(c.i[1])

        a.o[0].connect(b.i[1])
        a.o[0].connect(c.i[0])

        b.o[0].connect(d.i[0])
        c.o[0].connect(d.i[1])

        d.o[0].connect(io.o[0])

        results = io.calc()
        self.assertEqual(results, {'00': '0',
                                   '01': '1',
                                   '10': '1',
                                   '11': '0'})

    def test_half_adder(self):
        io = IO(2,2)
        a = Nand()
        b = Nand()
        c = Nand()
        d = Nand()
        e = Nand()
        f = Nand()
        g = Nand()
        h = Nand()
        i = Nand()

        io.i[0].connect(a.i[0])
        io.i[0].connect(b.i[0])

        io.i[1].connect(a.i[1])
        io.i[1].connect(c.i[1])

        a.o[0].connect(b.i[1])
        a.o[0].connect(c.i[0])

        b.o[0].connect(d.i[0])
        c.o[0].connect(d.i[1])

        d.o[0].connect(io.o[0])

        a.o[0].connect(e.i[0])
        a.o[0].connect(e.i[1])



        results = io.calc()
        self.assertEqual(results, {'00': '00',
                                   '01': '10',
                                   '10': '10',
                                   '11': '01'})

if __name__ == '__main__':
    unittest.main()
