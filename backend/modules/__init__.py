"""
Sistema de Módulos para CapivaraFlow
Cada módulo é um submódulo plugável do sistema principal
"""

class Module:
    """Classe base para todos os módulos"""
    
    def __init__(self, module_id, name, icon, description):
        self.id = module_id
        self.name = name
        self.icon = icon
        self.description = description
        self.is_active = True
    
    def get_info(self):
        """Retorna informações do módulo"""
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'description': self.description,
            'active': self.is_active
        }
    
    def get_data(self):
        """Retorna dados específicos do módulo - deve ser implementado"""
        raise NotImplementedError("Subclasses devem implementar get_data()")
    
    def process_data(self, data):
        """Processa dados do módulo - pode ser sobrescrito"""
        return data
