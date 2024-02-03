from helpers.serealizer import BaseSerializer

from tracker.models import LegalPerson, NaturalPerson, PackageContainer, Person, State, City


class StateSerializer(BaseSerializer):
    
    _model = State

    @classmethod
    def encode(self, instance):
        
        result = super().encode(instance)

        result.update(
            {
                "Name": str(instance.name),
                "Sigla": str(instance.abbreviation),
            }
        )

        return result
    

class CitySerializer(BaseSerializer):
    
    _model = City

    @classmethod
    def encode(self, instance):
        
        result = super().encode(instance)

        result.update(
            name=instance.name,
            state=[StateSerializer.encode(instance.state)]

        )

        return result


class PersonSerializer(BaseSerializer):
    
    _model = Person
    
   


class NaturalPersonSerializer(BaseSerializer):
    
    _model = NaturalPerson
    
    @classmethod
    def encode(self, instance):
        
        result = super().encode(instance)

        result.update(
            {
                "Name": str(instance.name),
                "city": CitySerializer.encode(instance.city)
            }
        )

        return result
    
    
class LegalPersonSerializer(BaseSerializer):
    
    _model = LegalPerson
    
    @classmethod
    def encode(self, instance):
        
        result = super().encode(instance)

        result.update(
            {
                "Fantasy Name": str(instance.fantasy_name),
                "city": CitySerializer.encode(instance.city)
            }
        )

        return result

class PackageContainerSerializer(BaseSerializer):

    _model = PackageContainer

    @classmethod
    def encode(self, instance):
        result = super().encode(instance)

        result.update(
            sender=PersonSerializer.encode(instance.sender),
            destination=PersonSerializer.encode(instance.destination),
            sender_city=CitySerializer.encode(instance.sender_city),
            destination_city=CitySerializer.encode(instance.destination_city),
            weight=float(instance.weight),
            volume=float(instance.volume),
            create_at=str(instance.create_at),
            unique_identify=instance.unique_identify,
            delivery_state=instance.delivery_state,
            delivery_state_display=instance.get_delivery_state_display()
        )

        return result
