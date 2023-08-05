'''
Created on Nov 17, 2016

@author: rli
'''
def get_check_digit(cusip):
    sum = 0
    if(not len(cusip)==8):
        raise ValueError('cusip must be 8 digit') 
    i = 0
    while(i<8):
        c = cusip[i]
        if(c.isdigit()):
            v = int(c)
        elif(c.isalpha()):
            p = ord(c)-ord('A')+1
            v = p + 9
        elif(c=='*'):
            v = 36
        elif(c=='@'):
            v = 37
        elif(c=='#'):
            v = 38
        else:
            raise ValueError('invalid cusip') 
        if(i%2==1):
            v = v*2
        sum += v/10 + v%10
        i += 1
    return (10 - (sum % 10)) % 10

def get_cusip9(cusip):
    return cusip+str(get_check_digit(cusip))
"""
097751BB6
1248EPBE2
147446AR9
29977HAB6
404119BN8
458204AP9
45824TAC9
45824TAM7
45824TAP0
526057BA1

if __name__ == '__main__':
    print get_check_digit("097751BB")
    print get_check_digit("1248EPBE")
    print get_check_digit("147446AR")
    print get_check_digit("29977HAB")
    print get_check_digit("404119BN")
    print get_check_digit("458204AP")
    print get_check_digit("45824TAC")
    print get_check_digit("45824TAM")
    print get_check_digit("45824TAP")
    print get_check_digit("526057BA")
"""