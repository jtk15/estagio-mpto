class BaseSerialization:

    _model = None

    @classmethod
    def Model(self):

        return self._model

    @classmethod
    def serealizer(self, instance):

        return {
            'pk': instance.pk,
            'description': str(instance)
        }
    
    @classmethod
    def deserealizer(self, data):

        return self._model(**data)
