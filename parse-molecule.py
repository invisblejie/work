def getnumber(a, number):
    result = ismelecule(a)
    for j in range(len(result)):
        switch = True
        for k in range(len(result[j])):
            if ord(result[j][k]) >=49 and ord(result[j][k]) <= 57:
                switch = False
                result[j] = [result[j][0:k], (int(result[j][k:]) * number)]
                break
        if switch:
            result[j] = [result[j], number]
    return result

def change(a, number):
    last = ''
    result = getnumber(a, number)
    for i in result:
        last += (i[0] + str(i[1]))
    return last

def ismelecule(a):
    result = []
    temple = 0
    for i in range(1,len(a)):
        if ord(a[i]) >= 65 and ord(a[i]) <= 90:
            result.append(a[temple: i])
            temple = i
    result.append(a[temple:])
    return result
    



def findnumber(formula, stop):
    number = ''
    while stop + 1 < len(formula) and ord(formula[stop + 1]) >= 49 and ord(formula[stop + 1])<= 57:
        number += formula[stop + 1]
        stop += 1
    if number == '':
        return 1,stop + 1
    else:
        return int(number), stop + 1

def removenotion(formula, a, b):
    while formula.find(a) != -1:
        start = formula.find(a)
        stop = formula.find(b)
        number, position = findnumber(formula, stop)
        formula = formula[0:start] + change(formula[start + 1:stop], number) +formula[position:]
    return formula

def parse_molecule(formula):
    result = {}
    formula = removenotion(formula, '(', ')')
    formula = removenotion(formula, '[', ']')
    formula = removenotion(formula, '{', '}')
    last = getnumber(formula, 1)
    for i in last:
        try: result[i[0]] += i[1]
        except: result[i[0]] = i[1]
    return result

if __name__ == "__main__":
    print(parse_molecule('{[Co(NH3)4(OH)2]3Co}(SO4)3'))

