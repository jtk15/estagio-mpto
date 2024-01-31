from tracker.models import State


class BaseSerialization:

    _model = None

    @classmethod
    def serealizer(self, instance):

        return {
            'pk': instance.pk,
            'description': str(instance)
        }
    
    @classmethod
    def deserealizer(self, data):

        return self._model(**data)


class StateSerialiazer(BaseSerialization):
    
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
