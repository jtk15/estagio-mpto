class BaseSerializer:

    _model = None

    @classmethod
    def Model(self):

        return self._model

    @classmethod
    def encode(self, instance):

        return {
            'pk': instance.pk,
            'description': str(instance)
        }
    
    @classmethod
    def decode(self, data):

        return self._model(**data)
