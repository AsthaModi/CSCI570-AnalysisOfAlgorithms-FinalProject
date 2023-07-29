import sys
import sys
# from resource import *
import time
import psutil

inputPath = sys.argv[1]
# outputPath = sys.argv[1]

# Initializing alpha (mismatch cost)
alphaMatrix = [[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]
dict = {"A":0, "C":1, "G":2, "T":3}

# Initializing delta (gap penalty)
delta = 30

# Initializations for strings s1 and s2
s1, s2 = "",""
listJ, listK = [],[]
inputString1, inputString2 = "",""
ans = []

# Creating function to read from input files 
def readFile(inputPath):
    file = open(inputPath, "r")
    stream = file.readlines()
    
    s1, s2 = "",""
    listJ, listK = [],[]
    
    s1 = stream[0].strip()
    
    for i in stream[1:]:
        i = i.strip()
        if i and i.isdigit():
            if not s2:
                listJ.append(int(i))
            else:
                listK.append(int(i))
        else:
            s2 = i
        
    return (s1, s2, listJ, listK)

# def __main__():
#     print('HI')
s1, s2, listJ, listK = readFile(inputPath)
# print(s1, s2, listJ, listK)
def inputStringGenerator(s, li):
    tmp = s
    for j in li:
        tmp = tmp[:j+1]+tmp+tmp[j+1:]
    if (len(tmp)!=2**len(li)*len(s)):
        print("There was an error in string generation.")
        return -1
    else:
        return tmp
    

inputString1 = inputStringGenerator(s1,listJ)
inputString2 = inputStringGenerator(s2,listK)

def dpApproach(inpS1,inpS2,delta,alphaMatrix):
    len1, len2 = len(inpS1), len(inpS2)
    dp =  [[float('inf') for j in range(len2+1)] for i in range(len1+1)]

    for j in range(len2+1):
        dp[0][j] = j*delta
        
    for i in range(len1+1):
        dp[i][0] = i*delta

    for i in range(1,len1+1):
        for j in range(1, len2+1):
            if inpS1[i-1] == inpS2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j]+delta, dp[i][j-1]+delta,dp[i-1][j-1]+alphaMatrix[dict[inpS1[i-1]]][dict[inpS2[j-1]]])
    # print(len(dp), len(dp[0]))
    print(dp[-1][-1])

    # m, n = len(inpS1), len(inpS2)
    outS1, outS2 = "",""
    # print(dp)
    while not (len1 == 0 or len2 == 0):
        if dp[len1][len2] == dp[len1-1][len2-1] + alphaMatrix[dict[inpS1[len1-1]]][dict[inpS2[len2-1]]]:
            outS1 = inpS1[len1-1] + outS1
            outS2 = inpS2[len2-1] + outS2
            len1,len2 = len1-1, len2-1
        elif dp[len1][len2] == dp[len1-1][len2] + delta:
            outS1 = inpS1[len1-1] + outS1
            outS2 = "_" + outS2
            len1 = len1-1
        elif dp[len1][len2] == dp[len1][len2-1] + delta:
            outS1 = "_" + outS1
            outS2 = inpS2[len2-1] + outS2
            len2 = len2-1
    while len1 != 0:
        outS1 = inpS1[len1-1] + outS1
        outS2 = "_" + outS2
        len1 = len1-1
    while len2 != 0:
        outS2 = inpS2[len2-1] + outS2
        outS1 = "_" + outS1
        len2 = len2-1
    return (outS1, outS2)

def main():
    process = psutil.Process()
    memory_info = process.memory_info()
    start_time = time.time()
    dpApproach(inputString1, inputString2, delta, alphaMatrix)
    end_time = time.time()
    memory_consumed = int(memory_info.rss/1024)
    time_taken = (end_time - start_time)*1000
    print(time_taken)
    print(memory_consumed)

# def time_wrapper():
#     start_time = time.time()
#     dpApproach(inputString1, inputString2, delta, alphaMatrix)
#     end_time = time.time()
#     time_taken = (end_time - start_time)*1000
#     return time_taken
# print(time_wrapper())
# print(process_memory())
main()