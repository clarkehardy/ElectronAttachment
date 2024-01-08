import numpy as np
import csv
import os
import argparse
dir_path = os.path.dirname(os.path.realpath(__file__))

def RateConstant(Efield):
    k = []
    field = []
    with open(dir_path + '/data/Bakale_digitized.csv','r') as infile:
        reader = csv.reader(infile)
        for line in reader:
            field.append(float(line[0]))
            k.append(float(line[1]))
    return np.interp(Efield,field,k)

def LXeDensity(pressure):
    # returns density in mol/L
    rho = []
    pres = []
    with open(dir_path + '/data/lxe_density_sat.csv','r') as infile:
        reader = csv.reader(infile)
        for line in reader:
            pres.append(float(line[0]))
            rho.append(float(line[1]))
    return np.interp(pressure,pres,rho)

def GXeDensity(pressure):
    # returns density in mol/L given pressure in torr
    rho = []
    pres = []
    with open(dir_path + '/data/gxe_density.csv','r') as infile:
        reader = csv.reader(infile)
        for line in reader:
            pres.append(float(line[0]))
            rho.append(float(line[1]))
    return np.interp(pressure,pres,rho)

def EL(conc,Efield,pressure=760):
    # takes concentration in ppb
    # returns electron lifetime in us
    # k in L/mol/s, concentration unitless, density in mol/L, pressure in torr
    return 1e6/(LXeDensity(pressure)*RateConstant(Efield)*conc*1e-9)

def Concentration(EL,Efield,pressure=760):
    # takes electron lifetime in us
    # returns concentration in ppb
    # k in L/mol/s, concentration unitless, density in mol/L, pressure in torr
    return 1e9/(RateConstant(Efield)*LXeDensity(pressure)*EL*1e-6)

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-Efield',type=float,default=400)
    parser.add_argument('-conc',type=float,default=1.)
    args = parser.parse_args()
    efield = args.Efield
    conc = args.conc

    print('At {} V/cm, {} ppb equates to {:.1f} us.'.format(efield,conc,EL(1,400)))
