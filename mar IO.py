import math
inputs_count = 1
output_count = 4# ButtonNames

Population = 300
DeltaDisjoint = 2.0
DeltaWeights = 0.4
DeltaThreshold = 1.0

StaleSpecies = 15

MutateConnectionsChance = 0.25
PerturbChance = 0.90
CrossoverChance = 0.75
LinkMutationChance = 2.0
NodeMutationChance = 0.50
BiasMutationChance = 0.40
StepSize = 0.1
DisableMutationChance = 0.4
EnableMutationChance = 0.2

TimeoutConstant = 20

MaxNodes = 1000000

def getInputs():
    """

    :return:  A list of length input_count stating if each input is possible at the current time
    """

    return [1,1,1,1]

def sigmoid(x):
    return 2 / (1 + math.exp(-4.9, x)) - 1

def newInnovation():
    pool.innovation += 1
    return pool.innovation

class Pool:
    def __init__(self):
        pool = {}
        pool.species = {}
        pool.generation = 0
        pool.innovation = output_count
        pool.currentSpecies = 1
        pool.currentGenome = 1
        pool.currentFrame = 0
        pool.maxFitness = 0


def newPool():
    pool = {}
    pool.species = {}
    pool.generation = 0
    pool.innovation = output_count
    pool.currentSpecies = 1
    pool.currentGenome = 1
    pool.currentFrame = 0
    pool.maxFitness = 0

    return pool


pool = newPool()

def newSpecies():
    species = {}
    species.topFitness = 0
    species.staleness = 0
    species.genomes = {}
    species.averageFitness = 0

    return species

class Genome:
    def __init__(self):
        self.genes = []
        self.fitness = 0
        self.adjustedFitness = 0
        self.network = []
        self.maxneuron = 0
        self.globalRank = 0
        self.mutationRates = {}

def newGenome():
    genome = Genome()
    genome.genes = []
    genome.fitness = 0
    genome.adjustedFitness = 0
    genome.network = []
    genome.maxneuron = 0
    genome.globalRank = 0
    genome.mutationRates = {}
    genome.mutationRates["connections"] = MutateConnectionsChance
    genome.mutationRates["link"] = LinkMutationChance
    genome.mutationRates["bias"] = BiasMutationChance
    genome.mutationRates["node"] = NodeMutationChance
    genome.mutationRates["enable"] = EnableMutationChance
    genome.mutationRates["disable"] = DisableMutationChance
    genome.mutationRates["step"] = StepSize

    return genome

def copyGenome(genome):
    genome2 = newGenome()
    genome2.genes = genome.genes.copy()
    # for genome in genome.genes:
        # table.insert(genome2.genes, copyGene(genome.genes[g]))

    genome2.maxneuron = genome.maxneuron
    genome2.mutationRates["connections"] = genome.mutationRates["connections"]
    genome2.mutationRates["link"] = genome.mutationRates["link"]
    genome2.mutationRates["bias"] = genome.mutationRates["bias"]
    genome2.mutationRates["node"] = genome.mutationRates["node"]
    genome2.mutationRates["enable"] = genome.mutationRates["enable"]
    genome2.mutationRates["disable"] = genome.mutationRates["disable"]

    return genome2

def basicGenome():
    genome = newGenome()
    innovation = 1

    genome.maxneuron = inputs_count
    mutate(genome)

    return genome

def newGene():
    gene = {}
    gene.into = 0
    gene.out = 0
    gene.weight = 0.0
    gene.enabled = True
    gene.innovation = 0

    return gene

def copyGene(gene):
    gene2 = newGene()
    gene2.into = gene.into
    gene2.out = gene.out
    gene2.weight = gene.weight
    gene2.enabled = gene.enabled
    gene2.innovation = gene.innovation

    return gene2

class Neuron:
    def __init__(self):
        self.incoming = []
        self.value = 0.0

def comp(item1, item2):
    return item1 - item2

def generateNetwork(genome):
    network = []
    network.neurons = []

    for i in range(inputs_count):
        network.neurons[i] = Neuron()

    for i in range(output_count):
        network.neurons[MaxNodes + i] = Neuron()


    genome.genes.sort(cmp=comp)
    """
    table.sort(genome.genes, function(a, b)
        return (a.out < b.out)
    """

    # for i=1,  # genome.genes do
        # local gene = genome.genes[i]
    for gene in genome.genes:
        if gene.enabled:
            if network.neurons[gene.out] == None :
                network.neurons[gene.out] = Neuron()

            neuron = network.neurons[gene.out]
            neuron.incoming.append(gene)
            # table.insert(neuron.incoming, gene)

            if network.neurons[gene.into] == None:
                network.neurons[gene.into] = Neuron()

    genome.network = network

def evaluateNetwork(network, inputs):
    # table.insert(inputs, 1)
    if  len(inputs) != len(inputs):
        raise Exception("Incorrect number of neural network inputs." + str(inputs))

    for i in range(len(inputs)):
        network.neurons[i].value = inputs[i]

    for neuron in network.neurons:
        sum = 0
        for incoming in neuron.incoming:
            other = network.neurons[incoming.into]
            sum = sum + incoming.weight * other.value

        if  len(neuron.incoming) > 0:
            neuron.value = sigmoid(sum)

    # TODO: This probably needs to set just one final output
    outputs = []
    for i in range(output_count):
        # TODO: This is most likely wrong...
        activate = network.neurons[MaxNodes + i].value > 0
        outputs.apped(activate)

        print("Button {} : {}".format(i, activate ))

    return outputs

def crossover(g1, g2):
    # Make sure g1 is the highest fitness genome
    if g2.fitness > g1.fitness:
        tempg = g1
        g1 = g2
        g2 = tempg
    child = newGenome()

    innovations2 = {}
    # for gene in g2.genes:
    for i in range(len(g2.genes)):
        gene = g2.genes[i]
        innovations2[gene.innovation] = gene

    for i in range(len(g1.genes)):
        gene1 = g1.genes[i]
        gene2 = innovations2[gene1.innovation]

        if gene2 != None and math.random(2) == 1 and gene2.enabled:
            # table.insert(child.genes, copyGene(gene2))
            child.genes.append(copyGene(gene2))
        else:
            # table.insert(child.genes, copyGene(gene1))
            child.genes.append(copyGene(gene1))

    child.maxneuron = math.max(g1.maxneuron, g2.maxneuron)

    child.mutationRates = g1.mutationRates.copy()
    """
    for mutation, rate in pairs(g1.mutationRates) do
        child.mutationRates[mutation] = rate
    """
    return child

def randomNeuron(genes, nonInput):
    neurons = [False] * len(inputs_count)
    if not nonInput:
        for i in range(inputs_count):
            neurons[i] = True

    for i in range(inputs_count):
        neurons[MaxNodes + i] = True

    for i in range(len(genes)):
        if not nonInput or genes[i].into > inputs_count:
            neurons[genes[i].into] = True

        if not nonInput or genes[i].out > inputs_count:
            neurons[genes[i].out] = True

    count = inputs_count
    """
    count = 0
    for _, _ in pairs(neurons) do
        count = count + 1
    """

    n = math.random(1, count)

    for k, v in neurons:
        n = n - 1
        if n == 0:
            return k

    """
    for k, v in pairs(neurons) do
        n = n - 1
        if n == 0 then
            return k
    """
    return 0

def containsLink(genes, link):
    for i in range(len(genes)):
        gene = genes[i]
        if gene.into == link.into and gene.out == link.out:
            return True

def pointMutate(genome):
    step = genome.mutationRates["step"]

    for i in range(genome.genes):
        gene = genome.genes[i]
        if math.random() < PerturbChance:
            gene.weight = gene.weight + math.random() * step * 2 - step
        else:
            gene.weight = math.random() * 4 - 2

def linkMutate(genome, forceBias):
    neuron1 = randomNeuron(genome.genes, False)
    neuron2 = randomNeuron(genome.genes, True)

    newLink = newGene()
    if neuron1 <= inputs_count and neuron2 <= inputs_count:
        return

    if neuron2 <= inputs_count:
        # Swap output and input
        temp = neuron1
        neuron1 = neuron2
        neuron2 = temp

    newLink.into = neuron1
    newLink.out = neuron2

    if forceBias:
        newLink.into = inputs_count

    if containsLink(genome.genes, newLink):
        return

    newLink.innovation = newInnovation()
    newLink.weight = math.random() * 4 - 2

    genome.genes.append(newLink)

def nodeMutate(genome):
    if  len(genome.genes) == 0:
        return

    genome.maxneuron = genome.maxneuron + 1

    gene = genome.genes[math.random(1,  len(genome.genes) )]
    if not gene.enabled:
        return
    gene.enabled = False

    gene1 = copyGene(gene)
    gene1.out = genome.maxneuron
    gene1.weight = 1.0
    gene1.innovation = newInnovation()
    gene1.enabled = True
    genome.genes.append(gene1)

    gene2 = copyGene(gene)
    gene2.into = genome.maxneuron
    gene2.innovation = newInnovation()
    gene2.enabled = True
    genome.genes.append(gene2)

def enableDisableMutate(genome, enable):
    candidates = []
    for gene in genome.genes:
        if not gene.enabled == enable:
            candidates.append(gene)

    if  len(candidates) == 0:
        return

    gene = candidates[math.random(1,  len(candidates))]
    gene.enabled = not gene.enabled

def mutate(genome):
    for mutation, rate in genome.mutationRates.items():
        if math.random(1, 2) == 1:
            genome.mutationRates[mutation] = 0.95 * rate
        else:
         genome.mutationRates[mutation] = 1.05263 * rate

    if math.random() < genome.mutationRates["connections"]:
        pointMutate(genome)

    p = genome.mutationRates["link"]

    while p > 0:
        if math.random() < p :
            linkMutate(genome, False)
        p = p - 1

    p = genome.mutationRates["bias"]

    while p > 0:
        if math.random() < p:
            linkMutate(genome, True)
        p = p - 1

    p = genome.mutationRates["node"]

    while p > 0 :
        if math.random() < p:
            nodeMutate(genome)
        p = p - 1

    p = genome.mutationRates["enable"]

    while p > 0:
        if math.random() < p:
            enableDisableMutate(genome, True)
        p = p - 1

    p = genome.mutationRates["disable"]

    while p > 0:
        if math.random() < p:
            enableDisableMutate(genome, False)
        p = p - 1

def disjoint(genes1, genes2):
    i1 = []
    for i in range(len(genes1)):
        gene = genes1[i]
        i1[gene.innovation] = True

    i2 = []
    for i in range(len(genes2)):
        gene = genes2[i]
        i2[gene.innovation] = True

    disjointGenes = 0
    for i in range(len(genes1)):
        gene = genes1[i]
        if not i2[gene.innovation]:
            disjointGenes = disjointGenes + 1

    for i in range(len(genes2)):
        gene = genes2[i]
        if not i1[gene.innovation]:
            disjointGenes = disjointGenes + 1

    n = math.max(len(genes1), len(genes2))

    return disjointGenes / n

def weights(genes1, genes2):
    i2 = []
    for i in range(len(genes2)):
        gene = genes2[i]
        i2[gene.innovation] = gene
    sum = 0
    coincident = 0

    for i in range(len(genes1)):
        gene = genes1[i]
        if i2[gene.innovation] != None :
            gene2 = i2[gene.innovation]
            sum = sum + math.abs(gene.weight - gene2.weight)
            coincident = coincident + 1

    return sum / coincident

def sameSpecies(genome1, genome2):
    dd = DeltaDisjoint * disjoint(genome1.genes, genome2.genes)
    dw = DeltaWeights * weights(genome1.genes, genome2.genes)

    return dd + dw < DeltaThreshold

def rankGlobally():
    _global = []
    for s in range(len(pool.species)):
        species = pool.species[s]
        for g in range(len(species.genomes)):
            _global.append(species.genomes[g])

    table.sort(
        _global, function(a, b)
        return (a.fitness < b.fitness)
    end)

    for g in range(len(_global):
        _global[g].globalRank = g

def calculateAverageFitness(species):
    total = 0

    # for g=1,  # species.genomes do
    for g in range(species.genomes):
        genome = species.genomes[g]
        total = total + genome.globalRank

    species.averageFitness = total /  len(species.genomes)

def totalAverageFitness():
    total = 0
    # for s = 1,  # pool.species do
    for s in range(len(pool.species)):
        species = pool.species[s]
        total = total + species.averageFitness

    return total

def cullSpecies(cutToOne):
    # for s = 1,  # pool.species do
    for s in range(pool.species):
        species = pool.species[s]

        table.sort(species.genomes, function(a, b)
            return (a.fitness > b.fitness)
        end)

        remaining = math.ceil(  # species.genomes/2)
        if cutToOne:
            remaining = 1

        while len(species.genomes) > remaining:
            species.genomes.clear()

def breedChild(species):
    child = []
    if math.random() < CrossoverChance:
        g1 = species.genomes[math.random(1, len(species.genomes))]
        g2=species.genomes[math.random(1,  len(species.genomes))]
        child=crossover(g1, g2)
    else:
        g = species.genomes[math.random(1,  # species.genomes)]
        child=copyGenome(g)

    mutate(child)

    return child

def removeStaleSpecies():
    survived = []

    for s in range(pool.species):
        species = pool.species[s]

        """
        table.sort(species.genomes, function(a, b)
            return (a.fitness > b.fitness)
        end)
        """

        if species.genomes[1].fitness > species.topFitness:
            species.topFitness = species.genomes[1].fitness
            species.staleness = 0
        else:
            species.staleness = species.staleness + 1

        if species.staleness < StaleSpecies or species.topFitness >= pool.maxFitness:
            survived.append(species)

    pool.species = survived

def removeWeakSpecies():
    survived = {}

    sum = totalAverageFitness()

    for s in range(len(pool.species)):
        species = pool.species[s]
        breed = math.floor(species.averageFitness / sum * Population)

        if breed >= 1:
            survived.append(species)


    pool.species = survived


def addToSpecies(child):
    foundSpecies = False

    for s in range(pool.species):
        species = pool.species[s]

        if not foundSpecies and sameSpecies(child, species.genomes[1]):
            # table.insert(species.genomes, child)
            species.genomes.append(child)
            foundSpecies = True

    if not foundSpecies:
        childSpecies = newSpecies()
        childSpecies.genomes.append(child)
        pool.species.append(childSpecies)

def newGeneration():
    cullSpecies(False) # Cull the bottom half of each species
    rankGlobally()
    removeStaleSpecies()
    rankGlobally()

    for s in range(pool.species):
        _species = pool.species[s]
        calculateAverageFitness(_species)

    removeWeakSpecies()
    _sum = totalAverageFitness()
    _children = []

    for s in range(pool.species):
        species = pool.species[s]
        breed = math.floor(species.averageFitness / _sum * Population) - 1

        # for i=1, breed do
        for i in range(1, breed):
            _children.append(breedChild())

    cullSpecies(True) # Cull all but the top member of each species

    while  len(_children) + len(pool.species) < Population:
        species = pool.species[math.random(1,  len(pool.species))]
        _children.append(breedChild(species))

    for c in range(len(_children)):
        child = _children[c]
        addToSpecies(child)

    pool.generation += 1

    # writeFile("backup."..pool.generation.."."..forms.gettext(saveLoadFile))

def initializePool():
    pool = newPool()

    for i in range(1, Population):
        basic = basicGenome()
        addToSpecies(basic)

    initializeRun()


def initializeRun():
    rightmost = 0
    pool.currentFrame = 0
    timeout = TimeoutConstant

    species = pool.species[pool.currentSpecies]
    genome = species.genomes[pool.currentGenome]
    generateNetwork(genome)
    evaluateCurrent()

def evaluateCurrent():
    species = pool.species[pool.currentSpecies]
    genome = species.genomes[pool.currentGenome]

    inputs = getInputs()
    controller = evaluateNetwork(genome.network, inputs)


    if pool == None:
        initializePool()

def nextGenome():
    pool.currentGenome = pool.currentGenome + 1
    if pool.currentGenome > len(pool.species[pool.currentSpecies].genomes):
        pool.currentGenome = 1
        pool.currentSpecies = pool.currentSpecies+1
        if pool.currentSpecies >  len(pool.species):
            newGeneration()
            pool.currentSpecies = 1

def fitnessAlreadyMeasured():
    species = pool.species[pool.currentSpecies]
    genome = species.genomes[pool.currentGenome]

    return genome.fitness != 0


while True:
    backgroundColor = 0xD0FFFFFF
    if not forms.ischecked(hideBanner):
        gui.drawBox(0, 0, 300, 26, backgroundColor, backgroundColor)

    species = pool.species[pool.currentSpecies]
    genome = species.genomes[pool.currentGenome]

    if forms.ischecked(showNetwork):
        displayGenome(genome)

    if pool.currentFrame % 5 == 0:
        evaluateCurrent()

    joypad.set(controller)

    getPositions()
    if marioX > rightmost:
        rightmost = marioX
        timeout = TimeoutConstant

    timeout = timeout - 1

    timeoutBonus = pool.currentFrame / 4
    if timeout + timeoutBonus <= 0:
        fitness = rightmost - pool.currentFrame / 2

        if fitness == 0:
            fitness = -1
        genome.fitness = fitness

        if fitness > pool.maxFitness:
            pool.maxFitness = fitness
            # forms.settext(maxFitnessLabel, "Max Fitness: "..math.floor(pool.maxFitness))
            # writeFile("backup."..pool.generation.. "."..forms.gettext(saveLoadFile))

        print("Gen {} species {} genome {} fintess {}".format(
            pool.generation, pool.currentSpecies, pool.currentGenome, fitness))
        pool.currentSpecies = 1
        pool.currentGenome = 1
        while fitnessAlreadyMeasured():
            nextGenome()

        initializeRun()

    measured = 0
    total = 0
    for _, species in pairs(pool.species):
        for _, genome in pairs(species.genomes):
            total += 1

            if math.isclose(genom.fitness, 0):
                measured += 1

# Migh need this one ==========================================================
"""
def playTop():
    maxfitness = 0
    maxs = None
    maxg = None

    for s, species in pairs(pool.species) do
        for g, genome in pairs(species.genomes) do
            if genome.fitness > maxfitness:
                maxfitness = genome.fitness
                maxs = s
                maxg = g

    pool.currentSpecies = maxs
    pool.currentGenome = maxg
    pool.maxFitness = maxfitness
    # forms.settext(maxFitnessLabel, "Max Fitness: "..math.floor(pool.maxFitness))
    initializeRun()
    pool.currentFrame = pool.currentFrame + 1

"""

"""
def displayGenome(genome)
    network = genome.network
    cells = {}

    i = 1
    cell = {}
    for dy=-BoxRadius, BoxRadius do
        for dx=-BoxRadius, BoxRadius do
            cell = {}
            cell.x = 50 + 5 * dx
            cell.y = 70 + 5 * dy
            cell.value = network.neurons[i].value
            cells[i] = cell
            i = i + 1
    biasCell = {}
    biasCell.x = 80
    biasCell.y = 110
    biasCell.value = network.neurons[Inputs].value
    cells[Inputs] = biasCell

    for o = 1, Outputs do
        cell = {}
        cell.x = 220
        cell.y = 30 + 8 * o
        cell.value = network.neurons[MaxNodes + o].value
        cells[MaxNodes + o] = cell
        color = 0xFF0000FF  if cell.value > 0 else 0xFF000000
    gui.drawText(223, 24 + 8 * o, ButtonNames[o], color, 9)

    for n, neuron in pairs(network.neurons) do
        cell = {}
        if n > Inputs and n <= MaxNodes then
            cell.x = 140
            cell.y = 40
            cell.value = neuron.value
            cells[n] = cell

    for n=1, 4 do
        for _, gene in pairs(genome.genes) do
            if gene.enabled:
                c1 = cells[gene.into]
                c2 = cells[gene.out]

                if gene.into > Inputs and gene.into <= MaxNodes:
                    c1.x = 0.75 * c1.x + 0.25 * c2.x
                    if c1.x >= c2.x:
                        c1.x = c1.x - 40
                    if c1.x < 90:
                        c1.x = 90

                    if c1.x > 220:
                        c1.x = 220

                    c1.y = 0.75 * c1.y + 0.25 * c2.y

                if gene.out > Inputs and gene.out <= MaxNodes:
                    c2.x = 0.25 * c1.x + 0.75 * c2.x
                    if c1.x >= c2.x:
                        c2.x = c2.x + 40
                    if c2.x < 90:
                        c2.x = 90
                    if c2.x > 220:
                        c2.x = 220

                    c2.y = 0.25 * c1.y + 0.75 * c2.y

    # gui.drawBox(50 - BoxRadius * 5 - 3, 70 - BoxRadius * 5 - 3, 50 + BoxRadius * 5 + 2, 70 + BoxRadius * 5 + 2, 0xFF000000, 0x80808080)

    for n, cell in pairs(cells) do
        if n > Inputs or cell.value ~= 0 then
            color = math.floor((cell.value + 1) / 2 * 256)

            if color > 255:
                color = 255
            if color < 0:
                color = 0

            opacity = 0xFF000000
            if cell.value == 0:
                opacity = 0x50000000

            color = opacity + color * 0x10000 + color * 0x100 + color
            gui.drawBox(cell.x - 2, cell.y - 2, cell.x + 2, cell.y + 2, opacity, color)
    for _, gene in pairs(genome.genes) do
        if gene.enabled:
            c1 = cells[gene.into]
            c2 = cells[gene.out]
            opacity = 0xA0000000
            if c1.value == 0:
                opacity = 0x20000000

            color = 0x80 - math.floor(math.abs(sigmoid(gene.weight)) * 0x80)
            if gene.weight > 0:
                color = opacity + 0x8000 + 0x10000 * color
            else:
                color = opacity + 0x800000 + 0x100 * color

            gui.drawLine(c1.x + 1, c1.y, c2.x - 3, c2.y, color)

    gui.drawBox(49, 71, 51, 78, 0x00000000, 0x80FF0000)

    if forms.ischecked(showMutationRates) then
        pos = 100
        for mutation, rate in pairs(genome.mutationRates) do
            gui.drawText(100, pos, mutation.. ": "..rate, 0xFF000000, 10) pos = pos + 8

"""

"""
def writeFile(filename):
    with open(filename, "w") as file:
        file.write(pool.generation)
        file.write(pool.maxFitness)
        file.write(pool.species)

        for n, species in pairs(pool.species):
            file.write(species.topFitness)
            file.write(species.staleness)
            file.write(species.genomes)

            for m, genome in pairs(species.genomes):
                file.write(genome.fitness..
                file:write(genome.maxneuron..
                for mutation, rate in pairs(genome.mutationRates) do
                    file:write(mutation..
                    file:write(rate..

                file.write("done\n")

            file.write(genome.genes)
                for l, gene in pairs(genome.genes):
                    file.write(gene.into)
                    file.write(gene.out)
                    file.write(gene.weight)
                    file.write(gene.innovation)

                    if gene.enabled:
                        file.write("1")
                    else:
                        file.write("0")

def savePool():
    filename = "backup.txt"#forms.gettext(saveLoadFile)
    writeFile(filename)

def loadFile(filename)
    with open(filename, "r"):
        pool = newPool()
        pool.generation = file:read("*number")
        pool.maxFitness = file:read("*number")
        forms.settext(maxFitnessLabel, "Max Fitness: "..math.floor(pool.maxFitness))

        numSpecies = file:read("*number")
        for s=1, numSpecies do
            species = newSpecies()
            table.insert(pool.species, species)
            species.topFitness = file:read("*number")
            species.staleness = file:read("*number")
            numGenomes = file:read("*number")


            for g=1, numGenomes do
                genome = newGenome()
                table.insert(species.genomes, genome)
                genome.fitness = file:read("*number")
                genome.maxneuron = file:read("*number")
                line = file:read("*line")

                while line ~= "done" do
                    genome.mutationRates[line] = file:read("*number")
                    line = file:read("*line")

                numGenes = file:read("*number")

                for n=1, numGenes do
                    gene = newGene()
                    table.insert(genome.genes, gene)
                    enabled = None
                    gene.into, gene.out, gene.weight, gene.innovation, enabled = file:read("*number", "*number", "*number", "*number",
                                                                       "*number")
                    if enabled == 0 :
                        gene.enabled = False
                    else:
                        gene.enabled = True

    while fitnessAlreadyMeasured():
        nextGenome()
    initializeRun()
    pool.currentFrame = pool.currentFrame + 1

def loadPool()
    filename = "backup.txt"
    loadFile(filename)
"""

"""
def onExit():
    forms.destroy(form)

writeFile("temp.pool")

event.onexit(onExit)

form = forms.newform(200, 260, "Fitness")
maxFitnessLabel = forms.label(form, "Max Fitness: "..math.floor(pool.maxFitness), 5, 8)
showNetwork = forms.checkbox(form, "Show Map", 5, 30)
showMutationRates = forms.checkbox(form, "Show M-Rates", 5, 52)
restartButton = forms.button(form, "Restart", initializePool, 5, 77)
saveButton = forms.button(form, "Save", savePool, 5, 102)
loadButton = forms.button(form, "Load", loadPool, 80, 102)
saveLoadFile = forms.textbox(form, Filename..
".pool", 170, 25, nil, 5, 148)
saveLoadLabel = forms.label(form, "Save/Load:", 5, 129)
playTopButton = forms.button(form, "Play Top", playTop, 5, 170)
hideBanner = forms.checkbox(form, "Hide Banner", 5, 190)
"""

    """
    if not forms.ischecked(hideBanner):
         gui.drawText(0, 0, "Gen "..pool.generation..
            " species "..pool.currentSpecies..
            " genome "..pool.currentGenome..
            " ("..math.floor(measured / total * 100)..
            "%)", 0xFF000000, 11)
            gui.drawText(0, 12, "Fitness: "..math.floor(rightmost - (pool.currentFrame) / 2 - (timeout + timeoutBonus) * 2 / 3),
                0xFF000000, 11)
            gui.drawText(100, 12, "Max Fitness: "..math.floor(pool.maxFitness), 0xFF000000, 11)
        """
