from helpers.baseSerialization import BaseSerialization

from tracker.models import State, City


class StateSerializer(BaseSerialization):
    
    _model = State

    @classmethod
    def serealizer(self, instance):
        
        result = super().serealizer(instance)

        result.update(
            {
                "Name": str(instance.name),
                "Sigla": str(instance.abbreviation),
            }
        )

        return result
    

class CitySerializer(BaseSerialization):
    
    _model = City

    @classmethod
    def serealizer(self, instance):
        
        result = super().serealizer(instance)

        result.update(
            name=instance.name,
            state=[StateSerializer.serealizer(instance.state)]

        )

        return result
