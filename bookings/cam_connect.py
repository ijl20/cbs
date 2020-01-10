from ibisclient import *

class CamConnect:
    def __init__(self):
        conn = createConnection()
        #conn = createTestConnection()
        self.pm = PersonMethods(conn)
        self.im = InstitutionMethods(conn)

    # returns the string displayName of userid
    def display_name(self, userid):
        p = self.pm.getPerson('crsid',userid)
        return p.displayName
      
    # returns the IBIS person object for userid
    def person(self, userid):
        p = self.pm.getPerson('crsid',userid, 'email,all_insts')
        return p
    
    # returns the list of IBIS inst objects for user
    def user_insts(self, userid):
        insts = self.pm.getInsts('crsid',userid)
        return insts

    # returns the IBIS inst object for instid
    def inst(self, instid):
        i = self.im.getInst(instid, 'parent_insts')
        return i
    
    # returns the list of IBIS inst objects from list of instid's
    def insts(self, instid_list):
        r = []
        for instid in instid_list:
            r.append(self.im.getInst(instid))
        return r
    
    def in_group(self, userid, groupid):
        return self.pm.isMemberOfGroup('crsid',userid,groupid)
                