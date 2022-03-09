from classAnalysis import Analysis

teste = Analysis(3375, 50.0, 140, 1, '/home/alebaal/Documents/thermoCapillaryWavesPosGz/*00000.pos.gz')

teste.loop()

#teste.plotPar()

slab = 10
pos = len(teste.filesPos)
for i in range(slab):
    count = 0
    for j in range(pos):
    	if (count/100):
	   print('slab: %d\t pos: %d', i, j)	
        teste.plotSlab(i,j, path = '/home/alebaal/Documents/resultsThermoCapWaves/')
        count+=1
