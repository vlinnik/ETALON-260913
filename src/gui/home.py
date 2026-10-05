from qtpy.QtWidgets import QWidget,qApp
from pysca import app
from concrete6 import concrete6

@app.inject()
def updateTooltip(expenses=[])->str:
    not_zero = [(concrete6.containers[i].component,x) for i,x in enumerate(expenses) if x>0]
    return '<html><head/><body>В смесителе: <table>' + '\n'.join([f'<tr><td>{component}</td><td>{amount:.2f}</td></tr>' for component,amount in not_zero]) + '</table></body></html>'

class Home(QWidget):
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
__all__ = ['updateTooltip']