import time


def solve_lin(m):                                                                               # The main function, determines the answers to given in form of koefficient-matrix system of linear equations                                                       
    zeile = 0                                                                                   # Prompts the user if something goes wrong (but not everything)
    fehlt = False
    vals = {}
    diff = len(m) - len(m[0]) + 1

    m = checkIfComplete(m, diff)
    m = checkTypo(m)
    print(m)
    
    
    while zeile < len(m):
        
        if m[zeile][zeile] != 0:   
            pivot = pivoteer(m[zeile], zeile)
            m = eliminate(m, pivot, zeile)
       
        else:
            if zeile == len(m)-1:
                f = fehler(m)
                if f == 0:
                    time.sleep(0.8)
                    return "Unloesbar"
                else:
                    
                    for elem in f:
                        time.sleep(0.8)
                        vals[elem] = input(f"Please, enter the value of x{elem+1}: ")
            
            else:
                found = seek(m, zeile)
                
                if found:
                    for i in range(zeile, found+1):
                        m.append(m.pop(i))
                    
                    zeile -= 1
                
                else:
                    fehlt = True

        zeile+=1
    
    if fehlt and vals == {}:
        f = fehler(m)
        if not f:
            time.sleep(0.8)
            return "Unloesbar"
        else:
            vals = []
            for elem in f:
                time.sleep(0.8)
                vals[elem] = input(f"Please, enter the value of x{elem+1}: ")                   #
    
    out = "Answers are: "
    arr = []
    
    if vals == {}:
        for elem in m:
            arr.append(str(round(elem[-1], 3)))
    else:
        for elem in range(len(m)):
            if elem in vals:
                arr.append(vals[elem])
            else:
                arr.append(str(round(get_val(elem, vals, m),3)))
    
    out += ", ".join(arr)
    time.sleep(0.8)
    return out

def get_val(elem, vals, m):                                                                     # This function calculates the value of parameters according to set-by-user values in infinite systems
    out = m[elem][-1]
    for ind in range(len(m)):
        if ind in vals:
            out -= float(vals[ind])*m[elem][ind]
    return out

def pivoteer(z, num):                                                                           # This function brings the defined equation to the pivot state
    haupt = z[num]
    
    for ind in range(len(z)):
        z[ind] *= 1/haupt
    
    return z

def eliminate(m, p, num):                                                                       # This function eliminates the defined parameter from all non-pivot equations
    for z in range(len(m)):
    
        if z != num:
            factor = m[z][num]
            
            for i in range(len(m[z])):
                m[z][i] -= factor*p[i]
    
    return m

def fehler(m):                                                                                  # This function determines the type of error, returns 0 if the system cannot be solved
    inf = []                                                                                    # And the list of missing values othervise
    for zeile in range(len(m)):
        zero = True
        for elem in range(len(m)):
            if elem != zeile and m[zeile][elem] != 0:
                zero = False     
        if zero:    
            if m[zeile][-1] != 0: 
                return 0
            else:
                inf.append(zeile)
    return inf            
    
def seek(m, zeile):                                                                             # This function searchs for equations where the defined (zeile) parameter does not equal zero, if there are such
    for ind in range(zeile, len(m)):
        
        if m[ind][zeile] != 0:
            return ind
   
    return False

def checkIfComplete(m, diff):                                                                   # The function checks if the matrix is complete (n equations and n parameters)
    if diff > 0:                                                                                # And prompts the user to make it complete via deleting or adding equations
        time.sleep(0.8)
        print("This matrix seems to be overdefined...")
        
        for count in range(diff):
            time.sleep(0.8)
            toDel = int(input("Which equation do you want to delete? "))
            m.pop(toDel-1)
    
    if diff < 0:
        time.sleep(0.8)
        print("This matrix seems to be underdefined...")
        
        for count in range(-diff):
            time.sleep(0.8)
            m.append(list(map(int, input("Which equation do you want to add? ").split())))
    
    return m

def checkTypo(m):
    
    lens = fillInLens(m)
    
    if len(lens) > 1:
        keys = list(lens.keys())
        lowest = keys[0]
        biggest = keys[1]
        
        for ind in keys:
            
            if len(lens[ind]) < len(lens[lowest]):
                lowest = ind
            if len(lens[ind]) > len(lens[biggest]):
                biggest = ind
        lenBigger = max(lowest, biggest)
        lenSmaller = min(lowest, biggest)

        answer = input(f"Do you want to delete from line {lens[lenBigger][1] + 1} or add to line {lens[lenSmaller][1] + 1}? (Del/Ins(Add)/Auto) ").lower()                                  # TODO: auto    
        if answer == "auto":
            answer = choose(lens, biggest, lowest)
        
        if answer == "del":    
            for ind in range(1, len(lens[lenBigger])):    
                
                time.sleep(0.5)
                toDel = int( input(f"Seems like you've got too much elements in line {lens[lenBigger][ind] + 1}, which one do you want to delete? ") ) - 1
                m[ lens[lenBigger][ind] ].pop(toDel)
        else:    
            for ind in range(1, len(lens[lenSmaller])):

                time.sleep(0.5)
                toAdd, pos = map(int, input(f"Seems like you've got not enough of elements in line {lens[lenSmaller][ind] + 1}, which one and where do you want to insert? ").split())
                pos -= 1
                m[ lens[lenSmaller][ind] ].insert(pos, toAdd)
        
        checkTypo(m)
    return m
    
    
def choose(lens, biggest, lowest):
    return "del"                                                                                                                                                                        #TODO

def fillInLens(m):
    lens = {}
    
    for ind in range(len(m)):
        curr_len = len(m[ind])
        
        if curr_len in lens:
            lens[curr_len][0] += 1
            lens[curr_len].append(ind)
        else:
            lens[curr_len] = [1, ind]
    
    return lens
    



matrix = [[2,3,-3,-3,5],[0,0,2,-1,2],[1,2,-1,-2,3],[0,-1,2,0,1]]
matrixUn = [[2,3,-1,12],[4,-3,7,6],[6,9,-3,18]]
matrixInf = [[2,-1,6,10],[1,1,-2,4],[1,-2,8,6]]
matrixOver = [[1,1,2,2],[3,4,6,7],[2,2,5,3], [2,2,5,3]]
matrixUnder = [[2,3,-1,12],[4,-3,7,6]]
matrixTypo1 = [[2,3,-3,-3,5],[0,0,2,-1,2],[1,2,-1,-2,3,3],[0,-1,2,0,1]]
matrixTypo2 = [[2,3,-3,-3,5],[2,-1,2],[1,2,-2,3],[0,-1,2,0,1]]

print(solve_lin(matrix))
print("")
print(solve_lin(matrixUn))
print("")
print(solve_lin(matrixInf))
print("")
print(solve_lin(matrixOver))
print("")
print(solve_lin(matrixUnder))
print("")
print(solve_lin(matrixTypo1))
print("")
print(solve_lin(matrixTypo2))