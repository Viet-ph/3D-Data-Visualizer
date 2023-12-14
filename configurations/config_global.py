import yaml

#YML configuration
config = {'Variance': 0.02, "FillHole": False}

isModifying = False

def getConfiguration():
    with open('configurations\config.yml', 'r') as file:
        global config
        configuration = yaml.safe_load(file)
        config['Variance'] = configuration['Variance']
        config['FillHole'] = configuration['FillHole']
    
    print("Variance: ", config['Variance'])

def updateNewConfiguration(varianceValue=config['Variance'], fillHoleValue = config['FillHole']):
    global config
    config['Variance'] = varianceValue
    config['FillHole'] = fillHoleValue
    with open('configurations\config.yml', 'w') as file:
        yaml.dump(config, file, sort_keys=False) 