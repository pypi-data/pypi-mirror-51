'''
Created on Nov 9, 2016

@author: rli
'''
def cqs2nasdaq(s):
    s = s.replace( 'p' ,     '-' )  # preferred
    s = s.replace( '/WS' ,   '+' )  # warrants
    s = s.replace( '/WD' ,   '$' )  # when distributed
    s = s.replace( '/CL' ,   '*' )  # called
    s = s.replace( '/EC' ,   '!' )  # emerging company marketplace
    s = s.replace( '/PP' ,   '@' )  # partial paid
    s = s.replace( '/CV' ,   '%' )  # convertible
    s = s.replace( 'r' ,     '^' )  # rights
    s = s.replace( '/U' ,    '=' )  # units
    s = s.replace( 'w' ,     '#' )  # when issued
    s = s.replace( '/TEST' , '~' )  # test
    s = s.replace( '/' ,     '.' )  # class A, B, ...
    return s

def nasdaq2cqs(s):
    s       =       s.replace(      '-'     ,       'p'     )       #       preferred
    s       =       s.replace(      '+'     ,       '/WS'   )       #       warrants
    s       =       s.replace(      '$'     ,       '/WD'   )       #       when    distributed
    s       =       s.replace(      '*'     ,       '/CL'   )       #       called
    s       =       s.replace(      '!'     ,       '/EC'   )       #       emerging        company marketplace
    s       =       s.replace(      '@'     ,       '/PP'   )       #       partial paid
    s       =       s.replace(      '%'     ,       '/CV'   )       #       convertible
    s       =       s.replace(      '^'     ,       'r'     )       #       rights
    s       =       s.replace(      '='     ,       '/U'    )       #       units
    s       =       s.replace(      '#'     ,       'w'     )       #       when    issued
    s       =       s.replace(      '~'     ,       '/TEST' )       #       test
    s       =       s.replace(      '.'     ,       '/'     )       #       class   A,      B,      ...
    return s

def nasdaq2bbg(s):
    s = s.replace('.CL', ' CL') #hack for GEB.CL and GEH.CL
    s = s.replace('-' , '/P' ) #prefered
    s = s.replace('p' , '/P' ) #prefered
    s = s.replace('+', '/WS') #warrants
    s = s.replace('$', '/WD') #When distributed
    s = s.replace('=', '/U') #unit
    s = s.replace('^', '-R') #right
    s = s.replace('.', '/') #class 
    s = s.replace('#', '-W') #when issue
    return s

def bbg2nasdaq(s):
    s = s.replace( '.CL' , '*' ) #called
    s = s.replace( '/WS' , '+' ) #warrants
    s = s.replace( '/WD' , '$' ) #When distributed
    s = s.replace( '/U' ,   '=' ) #unit
    s = s.replace( '-R' ,   '^' ) #right
    s = s.replace( '/P' , '-' ) #prefered
    s = s.replace( 'p' , '-' ) #prefered
    s = s.replace( ' ' , '-' ) #prefered
    s = s.replace( '/',     '.') #class 
    s = s.replace( '-W' ,   '#' ) #when issue
    return s
    
def qaam2nasdaq(s):
    symbol = s['SYMBOL']
    base = s['SYMBAS']
    if(symbol!=base):
        if(len(symbol)<=len(base)):            return symbol
        else:
            suffix = symbol[len(base):]
            return base+'.'+suffix
    return symbol


if __name__ == '__main__':
    print(nasdaq2cqs('BRK.A' ))
    print(nasdaq2cqs('WFCpJ' ))
