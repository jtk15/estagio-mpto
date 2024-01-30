class BaseSerialization:

    _model = None

    def serealizer(self, instance):

        raise NotImplemented('abstract class serealize not implemented')
    
     def deserealizer(self, instance):

        raise NotImplemented('abstract class serealize not implemented')

    