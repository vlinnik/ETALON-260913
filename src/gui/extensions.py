from qtpy.QtWidgets import QWidget,qApp

class Extensions(QWidget):
    def __init__(self, /, parent: QWidget = None ) -> None:
        super().__init__(parent)

# пример настройки обработчика события элемента (автоматически)
#    def on_<control name>_<signal name>(self,<signal arguments>):
#        pass

# пример добавления свойства text
#    def getText(self)->str:
#        return self._text
#    
#    def setText(self,text:str):
#        self._text = text
#
#    text = Property(str,fget=getText,fset=setText)  

#все что должно быть доступно глобально в событиях окна
#__all__ = []