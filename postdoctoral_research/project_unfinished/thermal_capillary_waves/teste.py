from classAnalysis import Analysis

print("Reading")
teste = Analysis(3375, 50.0, 140, 1, '/home/alebaal/Documents/thermoCapillaryWavesPosGz/*000.pos.gz')

print("Loop")
teste.loop()

print("Plot")
teste.plotPar()

print("Saveing Area and NumMolecules")
teste.savePar()
