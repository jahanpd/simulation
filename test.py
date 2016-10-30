from random import uniform, randint

Rate = 1000000

Gene = bin(Rate)

Genome = Gene[2:].zfill(100) + ('0'*100)

while int(Genome[0:100], 2) == Rate:
    Prob = 1./int(Genome[0:100], 2)
    _ = ""
    for n in Genome:
        if Prob >= uniform(0, 1):
            _ += str(randint(0, 1))
        else:
            _ += n
    Genome = _
    print Genome
