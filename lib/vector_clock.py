class vector_clock():
    vector = {}
    specific_id = ''
    #sets the vector clock to 0 for the list of ids given
    #id_list - a list of the uuids of the replicas
    #specific_id - optional, the replicas need to use this when incrementing
    def __init__(self,id_list,specific_id=''):
        for id in id_list:
            self.vector[id] = 0
        self.specific_id = specific_id
    #given a second clock, brings us up to date
    def updateToMax(self,v2):
        for id, val in v2.items():
            if id not in self.vector or val > self.vector[id]:
                self.vector[id] = val
    def increment(self):
        self.vector[self.specific_id] += 1
    #returns True iff our time stamp is greater than or equal to our given timestammp
    def is_geq(self,v2):
        for id,val in v2.items():
            if id not in self.vector:
                self.vector[id] = 0
            if val > self.vector[id]:
                return False
        return True
    #returns True or False given another vector clock
    def is_concurrent(self,v2):
        found_less_than = False
        found_more_than = False
        for id,val in v2.items():
            #there may be ids we haven't seen before, set these to 0
            if id not in self.vector:
                self.vector[id] = 0
            if val < self.vector[id]:
                found_less_than = True
            elif val > self.vector[id]:
                found_more_than = True
            if found_less_than and found_more_than:
                return True
        if (not found_less_than) and (not found_more_than):
            return True
        else:
            return False
