# Here we test for the rules requested by any page

# Rules are stored in 'Rule' objects, indexed with crate_id

from .cam_connect import CamConnect

from .models import Permission, Rule, Crate

CBS_ADMIN_GROUP = "100995"

class CamRules:

    # cam_connect - a connection to the IBIS api
    # userid - id of logged-on user
    # user - IbisPerson of logged on user
    # user_insts - list of instids for logged on user
    # rules - list of Rules for current crate
    
    def __init__(self, userid, target_crate=None, target_userid=None):
        self.cam_connect = CamConnect()
        
        self.userid = userid
        
        self.user = self.cam_connect.person(self.userid)
        
        self.user_insts = []
        for inst in self.user.institutions:
            self.user_insts.append(inst.instid)
        
        if target_crate:
            self.rules = self.get_rules(target_crate)
        else:
            self.rules = []
            
        if target_userid:
            self.target_userid = target_userid
    
    # return the ordered list of rules for a crate and its parents
    def get_rules(self, target_crate):
        rules =  []
        crate = target_crate
        while crate:
            crate_rules = Rule.objects.filter(crate_id=crate.id)
            for rule in crate_rules:
                rules.append(rule)
            crate = crate.parent_crate
        rules.sort(key=lambda r: r.permission.index)
        return rules
    
    # test permission for current user/crate and return tuple (Permission, reason) or None 
    def test(self, permission_name):

        permission = Permission.objects.get(name=permission_name)

        if self.test_superuser():
            return permission, "Requested "+permission_name+", actual CBS System Administrator"
        
        if permission_name == 'Self':
            if self.test_self(self.target_userid):
                return permission, "Self rule matched"
            else:
                return None, "Self rule failed"
            
        
        # test each of the permission rules associated with current crate
        for rule in self.rules:
            # rules are sorted by index so fail & quit if we're past required rule type
            if rule.permission.index > permission.index:
                return None, "Requested "+permission_name+", no successful rule found."
            # test simplest rule: 'cbs.ALL'
            if rule.userid and rule.userid == 'cbs.ALL':
                return rule.permission, "Requested "+permission_name+", All authenticated users are permitted to see resource "+rule.crate.id
            # now test just the current user's userid in rule
            if rule.userid and rule.userid == self.userid:
                return rule.permission, "Requested "+permission_name+", success based on userid " + self.userid + " for resource "+rule.crate.id
            # now test for group membership
            if rule.groupid and self.cam_connect.in_group(self.userid,rule.groupid):
                return rule.permission, "Requested "+permission_name+", success based on membership of group " + rule.groupid + " for resource "+rule.crate.id
            # finally test for inst membership
            if rule.instid:
                for instid in self.user_insts:
                    if instid == rule.instid:
                        return rule.permission, "Requested "+permission_name+", success based on membership of inst " + rule.instid + " for resource "+rule.crate.id
            
        return None, "No access rules were passed for " + permission_name

    def test_superuser(self):
        return self.cam_connect.in_group(self.userid,CBS_ADMIN_GROUP)

    def test_self(self, target_userid):
        return self.userid == target_userid or self.test_superuser()
       
    # return true if permission_name is a higher or equal index to 'permission'
    def passes(self, permission, permission_name):
        return Permission.objects.get(name=permission_name).index >= permission.index