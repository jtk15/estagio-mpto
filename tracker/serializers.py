from helpers.serealizer import BaseSerializer

from tracker.models import State, City


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
