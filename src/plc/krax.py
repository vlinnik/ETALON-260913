
from sys import platform
from pyplc.platform import plc,hw
from pyplc.utils.logging import logger
from pyplc.utils.misc import BLINK,TON,TP
from pyplc.sfc import SFC
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
    HW = namedtuple('HW',['CEMENT_M_1','WATER_M_1','ADDITION_M_1','FILLERS_M_1','MIXER_I_1','MIXER_ISON_1','MIXER_CLOSED_1','MIXER_OPENED_1','ELEVATOR_BELOW_1','ELEVATOR_ABOVE_1','DCEMENT_OPEN_1','DWATER_OPEN_1','DADDITIONS_OPEN_1','CONVEYOR_ON_1','AUGER_ON_1','AUGER_ON_2','WPUMP_ON_1','APUMP_ON_1','FEEDER_ON_1','FEEDER_ON_3','FILLER_OPEN_2L','FILLER_OPEN_2R','ELEVATOR_MOVEUP_1','ELEVATOR_MOVEDOWN_1','MIXER_ON_1','MIXER_OPEN_1','MIXER_CLOSE_1','BELL_ON_1','COMPRESSOR_ON_1','S_VIBRATOR_ON_1','S_VIBRATOR_ON_2','VIBRATOR_ON_1','VIBRATOR_ON_2','VIBRATOR_ON_3','DF_VIBRATOR_ON_1','ADDON_OPEN_1','OPUMP_ON_1','E_VIBRATOR_ON_1','WPUMP_ON_2','MIXER_OFF_1','APUMP_ON_2','ADDITION_1_BUSY','ADDITION_1_CLOSED','ADDITION_1_DONE','ADDITION_1_E','ADDITION_1_ERR','ADDITION_1_GO','ADDITION_1_LOCK','ADDITION_1_M','ADDITION_1_MAX_FF','ADDITION_1_MAX_W','ADDITION_1_MIN_FF','ADDITION_1_MIN_W','ADDITION_1_OUT','ADDITION_1_SP','ADDITION_2_BUSY','ADDITION_2_CLOSED','ADDITION_2_DONE','ADDITION_2_E','ADDITION_2_ERR','ADDITION_2_GO','ADDITION_2_LOCK','ADDITION_2_M','ADDITION_2_MAX_FF','ADDITION_2_MAX_W','ADDITION_2_MIN_FF','ADDITION_2_MIN_W','ADDITION_2_OUT','ADDITION_2_SP','ADDITION_M_1_A','ADDITION_M_1_K','ADDITION_M_1_M','ADDITION_M_1_MA','ADDITION_M_1_RAW','ADDITION_M_1_SET','ADDITION_M_1_SHIFT','ADDITION_M_1_STEP','ASSEMBLY_1_DISABLE_1','ASSEMBLY_1_DISABLE_2','ASSEMBLY_1_EN','ASSEMBLY_2_DISABLE_1','ASSEMBLY_2_DISABLE_2','ASSEMBLY_2_EN','AUGER_1_BUSY','AUGER_1_CLOSED','AUGER_1_DONE','AUGER_1_E','AUGER_1_ERR','AUGER_1_GO','AUGER_1_LOCK','AUGER_1_M','AUGER_1_MAX_FF','AUGER_1_MAX_W','AUGER_1_MIN_FF','AUGER_1_MIN_W','AUGER_1_OUT','AUGER_1_SP','AUGER_2_BUSY','AUGER_2_CLOSED','AUGER_2_DONE','AUGER_2_E','AUGER_2_ERR','AUGER_2_GO','AUGER_2_LOCK','AUGER_2_M','AUGER_2_MAX_FF','AUGER_2_MAX_W','AUGER_2_MIN_FF','AUGER_2_MIN_W','AUGER_2_OUT','AUGER_2_SP','CEMENT_M_1_A','CEMENT_M_1_K','CEMENT_M_1_M','CEMENT_M_1_MA','CEMENT_M_1_RAW','CEMENT_M_1_SET','CEMENT_M_1_SHIFT','CEMENT_M_1_STEP','DADDITION_1_ACK','DADDITION_1_CLOSED','DADDITION_1_COMPENSATION','DADDITION_1_COUNT','DADDITION_1_FAIL','DADDITION_1_GO','DADDITION_1_IGNORE','DADDITION_1_LEAVE','DADDITION_1_LOCK','DADDITION_1_M','DADDITION_1_NACK','DADDITION_1_OUT','DADDITION_1_UNLOADT','DCEMENT_1_ACK','DCEMENT_1_CLOSED','DCEMENT_1_COMPENSATION','DCEMENT_1_COUNT','DCEMENT_1_FAIL','DCEMENT_1_GO','DCEMENT_1_IGNORE','DCEMENT_1_LEAVE','DCEMENT_1_LOCK','DCEMENT_1_M','DCEMENT_1_NACK','DCEMENT_1_OUT','DCEMENT_1_UNLOADT','DF_VIBRATOR_1_AUTO','DF_VIBRATOR_1_IGNORE_DM','DF_VIBRATOR_1_Q','DWATER_1_ACK','DWATER_1_CLOSED','DWATER_1_COMPENSATION','DWATER_1_COUNT','DWATER_1_FAIL','DWATER_1_GO','DWATER_1_IGNORE','DWATER_1_LEAVE','DWATER_1_LOCK','DWATER_1_M','DWATER_1_NACK','DWATER_1_OUT','DWATER_1_UNLOADT','ELEVATOR_1_ABOVE','ELEVATOR_1_ACK','ELEVATOR_1_BELOW','ELEVATOR_1_DOWN','ELEVATOR_1_FAULT','ELEVATOR_1_LOADED','ELEVATOR_1_MANUAL','ELEVATOR_1_MAXT','ELEVATOR_1_MOVET','ELEVATOR_1_PAUSET','ELEVATOR_1_STATE','ELEVATOR_1_UNLOADT','ELEVATOR_1_UP','ELEVATOR_1_WEIGHT','FACTORY_1_ACTIVATED','FACTORY_1_EMERGENCY','FACTORY_1_HEARTBEAT','FACTORY_1_LOAD','FACTORY_1_MANUAL','FACTORY_1_MEM','FACTORY_1_MOTO','FACTORY_1_OVER','FACTORY_1_POWERACK','FACTORY_1_POWERED','FACTORY_1_POWERFAIL','FACTORY_1_SCANTIME','FACTORY_1_USED','FILLER_1_BUSY','FILLER_1_CLOSED','FILLER_1_DONE','FILLER_1_E','FILLER_1_ERR','FILLER_1_GO','FILLER_1_LOCK','FILLER_1_M','FILLER_1_MAX_FF','FILLER_1_MAX_W','FILLER_1_MIN_FF','FILLER_1_MIN_W','FILLER_1_OUT','FILLER_1_SP','FILLER_2_BUSY','FILLER_2_CLOSED','FILLER_2_DONE','FILLER_2_E','FILLER_2_ERR','FILLER_2_GO','FILLER_2_LOCK','FILLER_2_M','FILLER_2_MAX_FF','FILLER_2_MAX_W','FILLER_2_MIN_FF','FILLER_2_MIN_W','FILLER_2_OUT','FILLER_2_SP','FILLER_3_BUSY','FILLER_3_CLOSED','FILLER_3_DONE','FILLER_3_E','FILLER_3_ERR','FILLER_3_GO','FILLER_3_LOCK','FILLER_3_M','FILLER_3_MAX_FF','FILLER_3_MAX_W','FILLER_3_MIN_FF','FILLER_3_MIN_W','FILLER_3_OUT','FILLER_3_SP','FILLERS_1_ACK','FILLERS_1_CLOSED','FILLERS_1_COMPENSATION','FILLERS_1_COUNT','FILLERS_1_FAIL','FILLERS_1_GO','FILLERS_1_IGNORE','FILLERS_1_LEAVE','FILLERS_1_LOCK','FILLERS_1_M','FILLERS_1_NACK','FILLERS_1_OUT','FILLERS_1_UNLOADT','FILLERS_M_1_A','FILLERS_M_1_K','FILLERS_M_1_M','FILLERS_M_1_MA','FILLERS_M_1_RAW','FILLERS_M_1_SET','FILLERS_M_1_SHIFT','FILLERS_M_1_STEP','GATE_1_CLOSE','GATE_1_CLOSED','GATE_1_COUNT','GATE_1_DR','GATE_1_FORBID','GATE_1_LOCK','GATE_1_MANUAL','GATE_1_MIDDLE','GATE_1_MIDDLE_T','GATE_1_OPEN','GATE_1_OPENED','GATE_1_UNLOADING','MIXER_1_ACK','MIXER_1_BREAKPOINT','MIXER_1_CLOCK','MIXER_1_COUNT','MIXER_1_EXPENSE_0','MIXER_1_EXPENSE_1','MIXER_1_EXPENSE_2','MIXER_1_EXPENSE_3','MIXER_1_EXPENSE_4','MIXER_1_EXPENSE_5','MIXER_1_EXPENSE_6','MIXER_1_EXPENSE_7','MIXER_1_FORBID','MIXER_1_GO','MIXER_1_MIXT','MIXER_1_NACK','MIXER_1_QRESET','MIXER_1_READY','MIXER_1_REQ','MIXER_1_STATE','MIXER_1_UNLOADT','MOTOR_1_BELL','MOTOR_1_ISON','MOTOR_1_MANUAL','MOTOR_1_OFF','MOTOR_1_ON','MOTOR_1_POWERED','OIL_1_ENABLE','OIL_1_Q','OIL_1_T_OFF','OIL_1_T_ON','VIBRATOR_1_AUTO','VIBRATOR_1_Q','VIBRATOR_2_AUTO','VIBRATOR_2_Q','VIBRATOR_3_AUTO','VIBRATOR_3_Q','WATER_1_BUSY','WATER_1_CLOSED','WATER_1_DONE','WATER_1_E','WATER_1_ERR','WATER_1_GO','WATER_1_LOCK','WATER_1_M','WATER_1_MAX_FF','WATER_1_MAX_W','WATER_1_MIN_FF','WATER_1_MIN_W','WATER_1_OUT','WATER_1_SP','WATER_M_1_A','WATER_M_1_K','WATER_M_1_M','WATER_M_1_MA','WATER_M_1_RAW','WATER_M_1_SET','WATER_M_1_SHIFT','WATER_M_1_STEP','WPUMP_2_CLK','WPUMP_2_ET','WPUMP_2_PT','WPUMP_2_Q'],defaults=[])
    hw = HW()

logger.info(f'Запуск проекта {project_name} {project_version}')

factory_1 = Factory()

cement_m_1 = Weight( raw=hw.CEMENT_M_1, mmax=1500 ) 
water_m_1 = Weight( raw=hw.WATER_M_1, mmax=900 )
addition_m_1 = Weight( raw=hw.ADDITION_M_1, mmax=50 )
fillers_m_1 = Weight( raw=hw.FILLERS_M_1, mmax=4500 )

assembly_1 = Assembly2(outs=(hw.AUGER_ON_1,hw.AUGER_ON_2),sts=(~hw.AUGER_ON_1,~hw.AUGER_ON_2))
auger_1 = Container(m = cement_m_1.get_m, out=hw.AUGER_ON_1,closed=assembly_1.state(0), lock=Lock(key=lambda: hw.DCEMENT_OPEN_1 or not assembly_1.allowed(0)() ), max_sp = 1000 )
auger_2 = Container(m = cement_m_1.get_m, out=hw.AUGER_ON_2,closed=assembly_1.state(1), lock=Lock(key=lambda: hw.DCEMENT_OPEN_1 or not assembly_1.allowed(1)() ), max_sp = 1000 )
assembly_1.link(auger_1)
dcement_1 = Dosator(m = cement_m_1.get_m, containers = (auger_1,auger_2), out = hw.DCEMENT_OPEN_1,lock=Lock(key=lambda: not auger_1.closed or not auger_2.closed or not hw.MIXER_ISON_1) )

water_1 = Container(m = water_m_1.get_m, out=hw.WPUMP_ON_1, lock=Lock(key=hw.DWATER_OPEN_1), max_sp = 300 )
dwater_1 = Dosator(m = water_m_1.get_m, containers = (water_1,), lock=Lock(key=hw.WPUMP_ON_1), out = hw.DWATER_OPEN_1 )
wpump_2 = TON(clk=hw.DWATER_OPEN_1, q = hw.WPUMP_ON_2)

addition_1 = Container(m = addition_m_1.get_m, out=hw.APUMP_ON_1, lock=Lock(key=hw.DADDITIONS_OPEN_1),max_sp = 100 )
addition_2 = Container(m = addition_m_1.get_m, out=hw.APUMP_ON_2, lock=Lock(key=hw.DADDITIONS_OPEN_1),max_sp = 100 )
daddition_1 = Dosator(m = addition_m_1.get_m, containers = (addition_1,addition_2),lock=Lock(key=hw.APUMP_ON_1), out = hw.DADDITIONS_OPEN_1 )

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

class ElevatorVibrator(SFC):
    def main(self):
        yield from self.until(lambda: hw.ELEVATOR_ABOVE_1,step='wait.above')
        
        clock = 0
        while hw.ELEVATOR_ABOVE_1 and clock<=elevator_1.unloadT:
            hw.E_VIBRATOR_ON_1 = True
            yield from self.pause(1000)
            clock+=1
        hw.E_VIBRATOR_ON_1 = False
        
        yield from self.till(lambda: hw.ELEVATOR_ABOVE_1,step='wait.after')
e_vibrator_1 = ElevatorVibrator()

class Mixer8(Mixer):
    expense_0 = Mixer.var(0.0)
    expense_1 = Mixer.var(0.0)
    expense_2 = Mixer.var(0.0)
    expense_3 = Mixer.var(0.0)
    expense_4 = Mixer.var(0.0)
    expense_5 = Mixer.var(0.0)
    expense_6 = Mixer.var(0.0)
    expense_7 = Mixer.var(0.0)
    

gate_1 = MPGate( closed = hw.MIXER_CLOSED_1, opened = hw.MIXER_OPENED_1, open = hw.MIXER_OPEN_1,close=hw.MIXER_CLOSE_1)
motor_1 = Motor( on = hw.MIXER_ON_1,off=hw.MIXER_OFF_1, ison = hw.MIXER_ISON_1,bell = hw.BELL_ON_1 ) 
mixer_1 = Mixer8( gate = gate_1 , motor = motor_1,use_ack=False,flows=[x.q for x in [auger_1,auger_2,water_1,addition_1,addition_2]+elevator_1.expenses] )
oil_1 = BLINK(enable=hw.MIXER_ISON_1, q = hw.OPUMP_ON_1, t_off=1000*10*60,t_on=1000*1*60)

ready_1 = Readiness( rails=[dcement_1,dwater_1,daddition_1,elevator_1,mixer_1] )
loaded_1 = Loaded( rails=[dcement_1,dwater_1,daddition_1,elevator_1] )

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
    imotor_1 = iMOTOR(simple=False,on=hw.MIXER_ON_1,off=hw.MIXER_OFF_1,ison=hw.MIXER_ISON_1)
    ielevator_1=iELEVATOR(up=hw.ELEVATOR_MOVEUP_1,down=hw.ELEVATOR_MOVEDOWN_1,above=hw.ELEVATOR_ABOVE_1,below=hw.ELEVATOR_BELOW_1)
    icement_m_1 = iWEIGHT(loading = lambda: hw.AUGER_ON_1 or hw.AUGER_ON_2, unloading = hw.DCEMENT_OPEN_1,q=hw.CEMENT_M_1)
    iwater_m_1 = iWEIGHT(loading = hw.WPUMP_ON_1, unloading = hw.DWATER_OPEN_1,q=hw.WATER_M_1)
    iaddition_m_1 = iWEIGHT(loading = lambda: hw.APUMP_ON_1 or hw.APUMP_ON_2, unloading = hw.DADDITIONS_OPEN_1,q=hw.ADDITION_M_1)  
    ifillers_m_1 = iWEIGHT(loading = lambda: hw.FEEDER_ON_1 or hw.FEEDER_ON_3 or hw.FILLER_OPEN_2L or hw.FILLER_OPEN_2R, unloading = hw.CONVEYOR_ON_1,q=hw.FILLERS_M_1)
    
    return (imotor_1,ielevator_1,igate_1,icement_m_1,iwater_m_1,iaddition_m_1,ifillers_m_1)

instances = ( 
            cement_m_1,auger_1,auger_2,dcement_1,assembly_1,
            water_m_1,water_1,dwater_1,wpump_2,
            addition_m_1,addition_1,addition_2,daddition_1,
            elevator_1,e_vibrator_1,fillers_m_1,filler_1,filler_2,filler_3,assembly_2,fillers_1,vibrator_1,vibrator_2,vibrator_3,df_vibrator_1,
            factory_1,mixer_1,gate_1,motor_1,oil_1,manager_1,ready_1,loaded_1,
            )
if platform=='linux':
    instances+=imitation()

if plc: plc.run(instances=instances,ctx=globals())
