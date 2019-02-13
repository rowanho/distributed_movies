class vector_clock():
    vector = {}
    specific_id = ''
    #sets the vector clock to 0 for the list of ids given
    #input - a list of the uuids of the replicas
    def __init__(self,id_list,specific_id):#
        for id in id_list:
            self.vector[id] = 0
        self.specific_id = specific_id
    #given a second clock, brings us up to date
    def updateToMax(self,v2):
        for id, val in v2.items():
            if val > self.vector[id]:
                self.vector[id] = val
    def increment(self):
        self.vector[self.specific_id] += 1
