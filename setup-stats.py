####################################################################################
print('Creating Noun Types')

from bookings.models import NounType

NounType(id="crate",
    description="Info regarding a bookable resource, e.g. room, equipment etc.",
    ).save()
    
NounType(id="person",
    description="Info regarding a person, i.e. some user has just looked at a person-page",
    ).save()
    
NounType(id="inst",
    description="Info regarding an institution, i.e. some user has just looked at an inst page",
    ).save()
    
NounType(id="general",
    description="A general page accessible by any user, e.g. index, help, about",
    ).save()
    
NounType(id="admin",
    description="Page on the system used for local or enterprise administration",
    ).save()
    
print('Noun types crate,person,inst,general,admin created')
