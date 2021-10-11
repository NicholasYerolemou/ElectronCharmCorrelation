
import sys
import math
lib = "/opt/exp_soft/cern/pythia/lib"
sys.path.insert(0,lib)


import pythia8
pythia = pythia8.Pythia()
pythia.readString("Beams:idA = 2212")#p-p collision
pythia.readString("Beams:idB = 2212")

#pythia.readString("Beams:frameType = 1")
pythia.readString("Beams:eCM = 13500.")

pythia.readString("HardQCD:hardccbar = on")
pythia.readString("PhaseSpace:pTHatMin = 20.")
pythia.readString("MultipartonInteractions:processLevel = 1");#doesnt effect cross section
pythia.init()




def isCharm(event,prt):#checks if it is the first charm quark produced
    if(abs(prt.id()) == 4):
        return True
    else:return False

def isInitialCharm(event,prt):#checks if it is the first charm quark produced
    if(abs(prt.id()) == 4):
        if(abs(event[prt.mother1()].id()) == 4 or abs(event[prt.mother2()].id()) == 4):
            return False
        else:
            return True
    else:return False


def isInitialBeam(event,arr):#checks if it is the intial proton beam
    for i in range(len(arr)):
        if(arr[i]!=event[1] or arr[i]!=event[2]):
            return False
            
    return True




def findParticles(event,arr):
    particles = []
    for i in range(len(arr)):
        particles.append(event[arr[i]])
    return particles


def parentIsCharm(event,arr,num):
    for i in range(len(arr)):
        if(isCharm(event,arr[i])):
            if(num == 0):
                setElectronCharmStats(arr[i])
            if(num == 1):
                setMuonCharmStats(arr[i])
            return True
    return False


def motherOfMothers(event,arr):
    particles = []
    
    for i in range(len(arr)):
        temp = arr[i].motherList()
        for p in range(len(temp)):
            particles.append(temp[p])
    return particles




def isCharmDaughter(event,prt,num):
    row = findParticles(event,prt.motherList())#list of mothers of initial particle
    run = True
    while(run):# runs until either the particle is a charm or one of the initial protons
        if(isInitialBeam(event,row)):#the particle is one of the original protons 
            #This happends when there are no parents of any of the particles
            return False
        elif(parentIsCharm(event,row,num)): return True
        else:
            parentsIndexes = motherOfMothers(event,row)#returns an array of the current particles parents indexes
            row = findParticles(event,parentsIndexes)#returns an array of the particle objects of the parents indexes




def isFinalElectron(prt):#checks if the particle is a final electron/positron
    if(abs(prt.id()) == 11 and prt.isFinal()):
        return True
    else:return False

def isFinalMuon(prt):
    if(abs(prt.id()) == 13 and prt.isFinal()):
        return True
    else:return False

def getdPhi(phi,phiC):
    dPhi = phi-phiC
    return dPhi
    """
    if(dPhi < 0): 
        return dPhi + 2*math.pi
    elif(dPhi>2*math.pi):
        return dPhi - 2*math.pi
    else:
        return dPhi
    """

def createTxtFile():
    f = open("ParticleStatisticsElectron.txt","w")
    g = open("ParticleStatisticsMuon.txt","w")

    for i in range(len(eStats)):
        #etaE,etaC,ptE,ptC,phiE,phiC,dPhi
        line =  str(eStats[i][0]) + "," + str(ceStats[i][0]) + "," + str(eStats[i][1]) + "," + str(ceStats[i][1]) + "," + str(eStats[i][2]) + "," + str(ceStats[i][2]) + "," + str(getdPhi(eStats[i][2],ceStats[i][2]))+"\n";f.write(line)
    for i in range(len(mStats)):
        line =  str(mStats[i][0]) + "," + str(cmStats[i][0]) + "," + str(mStats[i][1]) + "," + str(cmStats[i][1]) + "," + str(mStats[i][2]) + "," + str(cmStats[i][2]) + "," + str(getdPhi(mStats[i][2],cmStats[i][2]))+"\n";g.write(line)


electrons = []
def addElectron(e):
    electrons.append(e)

charms = []
def addCharm(c):
    charms.append(c)

ceStats = []
def setElectronCharmStats(prt):
    temp = []
    temp.append(prt.eta())
    temp.append(prt.pT())
    temp.append(prt.phi())
    temp.append(prt.id())
    ceStats.append(temp) 

cmStats = []
def setMuonCharmStats(prt):
    temp = []
    temp.append(prt.eta())
    temp.append(prt.pT())
    temp.append(prt.phi())
    temp.append(prt.id())
    cmStats.append(temp) 

eStats = []
def setElectronStats(prt):
    temp = []
    temp.append(prt.eta())
    temp.append(prt.pT())
    temp.append(prt.phi())
    temp.append(prt.id())
    eStats.append(temp) 


mStats = []
def setMuonStats(prt):
    temp = []
    temp.append(prt.eta())
    temp.append(prt.pT())
    temp.append(prt.phi())
    temp.append(prt.id())
    mStats.append(temp) 


nElectrons = 0
nMuons = 0
nCharms = 0

temp =[]#holds the charm who are parents of an electron which is then added to the allElectronsCharms array, then deleted

initialCharms = []
numberOfEvents = 3500000
for iEvent in range(numberOfEvents):#loop through number of collisions
    
    if not pythia.next(): continue #if there is no issue continue
        
    for prt in pythia.event:#loop through each particle in the event
        
        if(isFinalElectron(prt)):
            nElectrons +=1
            if(isCharmDaughter(pythia.event,prt,0)):
                setElectronStats(prt)
        
        if(isFinalMuon(prt)):
            nMuons +=1
            if(isCharmDaughter(pythia.event,prt,1)):
                setMuonStats(prt)


        if(isInitialCharm(pythia.event,prt)):
            nCharms +=1

createTxtFile()
print("Electrons",nElectrons)
print("Muon",nMuons)
print("charms", nCharms)
print("Electrons with charm parents",len(eStats))
print("Muons with charm parents",len(mStats))

pythia.stat();
