from django.db import models


class State(models.Model):
    
    name = models.CharField('Nome', max_length=30, unique=True)
    abbreviation = models.CharField('Sigla', max_length=2, unique=True)

    def __str__(self):

        return  f'{self.name}/{self.abbreviation}'
    

class City(models.Model):
    
    name = models.CharField('Nome', max_length=30, unique=True)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.PROTECT)

    
    def __str__(self):

        return  f'{self.name}/{self.state.abbreviation}'


class Person(models.Model):

    name = models.CharField('Nome', max_length=200)
    city = models.ForeignKey(City, related_name='+', on_delete=models.PROTECT)
    
    class Meta:

        abstract = True
        
    def __str__(self):
        
        return f'{self.name}'


class NaturalPerson(Person):
    
    cpf = models.CharField('Cadastro de pessoa fisica', max_length=11, unique=True)
    
    def __str__(self):
        
        return f'{self.name} ({self.cpf})'

class LegalPerson(Person):
    
    fantasy_name = models.CharField('Nome Fatasia', max_length=200)
    cnpj = models.CharField('Cadastro Nacional de Pessoa Juridica', max_length=30, unique=True)
    
    def __str__(self) -> str:
        
        return f'{self.fantasy_name} ({self.cnpj})'


        