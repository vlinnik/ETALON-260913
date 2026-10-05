
from sys import platform
from pyplc.platform import plc,hw
from pyplc.utils.logging import logger
from project import name as project_name,version as project_version
from concrete import Factory,Mixer,Motor,Manager,Readiness,Loaded,Weight,Container,Dosator,Lock
from concrete.container import Assembly2
from concrete.vibrator import Vibrator,UnloadHelper
from concrete.elevator import ElevatorGeneric
from concrete.msgate import MPGate

#VSCode autocompleter блок.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from collections import namedtuple
    HW = namedtuple('HW',['CEMENT_M_1','WATER_M_1','ADDITION_M_1','FILLERS_M_1','MIXER_I_1','MIXER_ISON_1','MIXER_CLOSED_1','MIXER_OPENED_1','ELEVATOR_BELOW_1','ELEVATOR_ABOVE_1','DCEMENT_OPEN_1','DWATER_OPEN_1','DADDITIONS_OPEN_1','CONVEYOR_ON_1','AUGER_ON_1','AUGER_ON_2','WPUMP_ON_1','APUMP_ON_1','FEEDER_ON_1','FEEDER_ON_3','FILLER_OPEN_2L','FILLER_OPEN_2R','ELEVATOR_MOVEUP_1','ELEVATOR_MOVEDOWN_1','MIXER_ON_1','MIXER_OPEN_1','MIXER_CLOSE_1','BELL_ON_1','COMPRESSOR_ON_1','S_VIBRATOR_ON_1','S_VIBRATOR_ON_2','VIBRATOR_ON_1','VIBRATOR_ON_2','VIBRATOR_ON_3','DF_VIBRATOR_ON_1','ADDON_OPEN_1'],defaults=[])
    hw = HW()

logger.info(f'Запуск проекта {project_name} {project_version}')

factory_1 = Factory()

cement_m_1 = Weight( raw=hw.CEMENT_M_1, mmax=1500 ) 
water_m_1 = Weight( raw=hw.WATER_M_1, mmax=500 )
addition_m_1 = Weight( raw=hw.ADDITION_M_1, mmax=100 )
fillers_m_1 = Weight( raw=hw.FILLERS_M_1, mmax=8000 )

assembly_1 = Assembly2(outs=(hw.AUGER_ON_1,hw.AUGER_ON_2),sts=(~hw.AUGER_ON_1,~hw.AUGER_ON_2))
auger_1 = Container(m = cement_m_1.get_m, out=hw.AUGER_ON_1,closed=assembly_1.state(0), lock=Lock(key=lambda: hw.DCEMENT_OPEN_1 or not assembly_1.allowed(0)() ), max_sp = 1000 )
auger_2 = Container(m = cement_m_1.get_m, out=hw.AUGER_ON_2,closed=assembly_1.state(1), lock=Lock(key=lambda: hw.DCEMENT_OPEN_1 or not assembly_1.allowed(1)() ), max_sp = 1000 )
assembly_1.link(auger_1)
dcement_1 = Dosator(m = cement_m_1.get_m, containers = (auger_1,auger_2), out = hw.DCEMENT_OPEN_1,lock=Lock(key=lambda: not auger_1.closed or not auger_2.closed or not hw.MIXER_ISON_1) )

water_1 = Container(m = water_m_1.get_m, out=hw.WPUMP_ON_1, lock=Lock(key=hw.DWATER_OPEN_1), max_sp = 300 )
dwater_1 = Dosator(m = water_m_1.get_m, containers = (water_1,), lock=Lock(key=hw.WPUMP_ON_1), out = hw.DWATER_OPEN_1 )

addition_1 = Container(m = addition_m_1.get_m, out=hw.APUMP_ON_1, lock=Lock(key=hw.DADDITIONS_OPEN_1),max_sp = 100 )
daddition_1 = Dosator(m = addition_m_1.get_m, containers = (addition_1,),lock=Lock(key=hw.APUMP_ON_1), out = hw.DADDITIONS_OPEN_1 )

filler_1 = Container( m=fillers_m_1.get_m, out=hw.FEEDER_ON_1, closed=~hw.FEEDER_ON_1,lock=Lock(key=lambda: not filler_3.closed or not filler_2.closed or hw.CONVEYOR_ON_1),max_sp = 4000 )
assembly_2 = Assembly2( outs = (hw.FILLER_OPEN_2L,hw.FILLER_OPEN_2R),sts = (~hw.FILLER_OPEN_2L,~hw.FILLER_OPEN_2R) )
filler_2 = Container( m=fillers_m_1.get_m, out= assembly_2.out, closed=lambda: not (hw.FILLER_OPEN_2L or hw.FILLER_OPEN_2R) ,lock=Lock(key=lambda: not filler_1.closed or not filler_3.closed or hw.CONVEYOR_ON_1), max_sp = 4000 )
assembly_2.link(filler_2)
assembly_2.en = True
filler_3 = Container( m=fillers_m_1.get_m, out=hw.FEEDER_ON_3,lock=Lock(key=lambda: not filler_1.closed or not filler_2.closed or hw.CONVEYOR_ON_1), max_sp = 4000 )

fillers_1 = Dosator(m = fillers_m_1.get_m,containers = (filler_1,filler_2,filler_3), out = hw.CONVEYOR_ON_1,lock=Lock(key=lambda: hw.FILLER_OPEN_2R or hw.FILLER_OPEN_2L or hw.FEEDER_ON_1 or hw.FEEDER_ON_3 or not hw.ELEVATOR_BELOW_1) )
vibrator_1 = Vibrator( q = hw.VIBRATOR_ON_1,containers=(hw.FEEDER_ON_1,),weight = fillers_m_1)
vibrator_2 = Vibrator( q = hw.VIBRATOR_ON_2,containers=(hw.FILLER_OPEN_2R,hw.FILLER_OPEN_2L),weight = fillers_m_1)
vibrator_3 = Vibrator( q = hw.VIBRATOR_ON_3,containers=(hw.FEEDER_ON_3,),weight = fillers_m_1)
df_vibrator_1 = UnloadHelper(q = hw.DF_VIBRATOR_ON_1, dosator=fillers_1, weight=fillers_m_1)

elevator_1 = ElevatorGeneric( up = hw.ELEVATOR_MOVEUP_1, down = hw.ELEVATOR_MOVEDOWN_1, above = hw.ELEVATOR_ABOVE_1, below = hw.ELEVATOR_BELOW_1,containers=(filler_1,filler_2,filler_3),dosator=fillers_1 )

class Mixer7(Mixer):
    expense_0 = Mixer.var(0.0)
    expense_1 = Mixer.var(0.0)
    expense_2 = Mixer.var(0.0)
    expense_3 = Mixer.var(0.0)
    expense_4 = Mixer.var(0.0)
    expense_5 = Mixer.var(0.0)
    expense_6 = Mixer.var(0.0)
    

gate_1 = MPGate( closed = hw.MIXER_CLOSED_1, opened = hw.MIXER_OPENED_1, open = hw.MIXER_OPEN_1,close=hw.MIXER_CLOSE_1)
motor_1 = Motor( powered = hw.MIXER_ON_1, ison = hw.MIXER_ISON_1,bell = hw.BELL_ON_1 ) 
mixer_1 = Mixer7( gate = gate_1 , motor = motor_1,use_ack=False,flows=[x.q for x in [auger_1,auger_2,water_1,addition_1]+elevator_1.expenses] )

ready_1 = Readiness( rails=[dcement_1,dwater_1,daddition_1,fillers_1,elevator_1] )
loaded_1 = Loaded( rails=[dcement_1,dwater_1,daddition_1,fillers_1,elevator_1] )

def load_order():
    elevator_1.unload = True
    daddition_1.unload = True
    yield
    daddition_1.unload = False
    elevator_1.unload = False
    while not elevator_1.above: yield
    dcement_1.unload = True
    dwater_1.unload = True

manager_1 = Manager(collected=ready_1,loaded=loaded_1,mixer = mixer_1,dosators=(dcement_1,dwater_1,daddition_1,elevator_1),loadOrder=load_order)

factory_1.on_emergency = [x.emergency for x in (manager_1,mixer_1,dcement_1,dwater_1,daddition_1,fillers_1,elevator_1,gate_1)]
factory_1.on_mode = [x.switch_mode for x in (dcement_1,dwater_1,daddition_1,fillers_1)]

def imitation()-> tuple:
    from concrete.imitation import iMOTOR,iELEVATOR,iGATE,iWEIGHT
    igate_1 = iGATE(open=hw.MIXER_OPEN_1,close=hw.MIXER_CLOSE_1,opened=hw.MIXER_OPENED_1,closed=hw.MIXER_CLOSED_1,simple=True)
    imotor_1 = iMOTOR(simple=True,on=hw.MIXER_ON_1,ison=hw.MIXER_ISON_1)
    ielevator_1=iELEVATOR(up=hw.ELEVATOR_MOVEUP_1,down=hw.ELEVATOR_MOVEDOWN_1,above=hw.ELEVATOR_ABOVE_1,below=hw.ELEVATOR_BELOW_1)
    icement_m_1 = iWEIGHT(loading = lambda: hw.AUGER_ON_1 or hw.AUGER_ON_2, unloading = hw.DCEMENT_OPEN_1,q=hw.CEMENT_M_1)
    iwater_m_1 = iWEIGHT(loading = hw.WPUMP_ON_1, unloading = hw.DWATER_OPEN_1,q=hw.WATER_M_1)
    iaddition_m_1 = iWEIGHT(loading = hw.APUMP_ON_1, unloading = hw.DADDITIONS_OPEN_1,q=hw.ADDITION_M_1)  
    ifillers_m_1 = iWEIGHT(loading = lambda: hw.FEEDER_ON_1 or hw.FEEDER_ON_3 or hw.FILLER_OPEN_2L or hw.FILLER_OPEN_2R, unloading = hw.CONVEYOR_ON_1,q=hw.FILLERS_M_1)
    
    return (imotor_1,ielevator_1,igate_1,icement_m_1,iwater_m_1,iaddition_m_1,ifillers_m_1)

instances = ( factory_1,mixer_1,gate_1,motor_1,elevator_1,manager_1,ready_1,loaded_1,
            cement_m_1,auger_1,auger_2,dcement_1,assembly_1,
            water_m_1,water_1,dwater_1,
            addition_m_1,addition_1,daddition_1,
            fillers_m_1,filler_1,filler_2,filler_3,assembly_2,fillers_1,vibrator_1,vibrator_2,vibrator_3,df_vibrator_1
            )
if platform=='linux':
    instances+=imitation()

if plc: plc.run(instances=instances,ctx=globals())
