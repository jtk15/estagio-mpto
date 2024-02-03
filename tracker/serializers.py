from helpers.serealizer import BaseSerializer

from tracker.models import LegalPerson, NaturalPerson, Person, State, City


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
