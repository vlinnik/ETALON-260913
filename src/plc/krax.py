
from sys import platform
from pyplc.platform import plc,hw
from pyplc.utils.logging import logger
from project import name as project_name,version as project_version


#VSCode autocompleter блок.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from collections import namedtuple
    HW = namedtuple('HW',['CEMENT_M_1','WATER_M_1','ADDITION_M_1','FILLERS_M_1','MIXER_I_1','MIXER_ISON_1','MIXER_CLOSED_1','MIXER_OPENED_1','ELEVATOR_BELOW_1','ELEVATOR_ABOVE_1','DCEMENT_OPEN_1','DWATER_OPEN_1','DADDITIONS_OPEN_1','CONVEYOR_ON_1','AUGER_ON_1','AUGER_ON_2','WPUMP_ON_1','APUMP_ON_1','FEEDER_ON_1','FEEDER_ON_3','FILLER_OPEN_2L','FILLER_OPEN_2R','ELEVATOR_MOVEUP_1','ELEVATOR_MOVEDOWN_1','MIXER_ON_1','MIXER_OPEN_1','MIXER_CLOSE_1','BELL_ON_1','COMPRESSOR_ON_1','S_VIBRATOR_ON_1','S_VIBRATOR_ON_2','VIBRATOR_ON_1','VIBRATOR_ON_2','VIBRATOR_ON_3','DF_VIBRATOR_ON_1','ADDON_OPEN_1'],defaults=[])
    hw = HW()

logger.info(f'Запуск проекта {project_name} {project_version}')

def imitation()-> tuple:
    from concrete.imitation import iMOTOR,iELEVATOR,iGATE
    igate_1 = iGATE(open=hw.MIXER_OPEN_1,close=hw.MIXER_CLOSE_1,opened=hw.MIXER_OPENED_1,closed=hw.MIXER_CLOSED_1,simple=True)
    imotor_1 = iMOTOR(simple=True,on=hw.MIXER_ON_1,ison=hw.MIXER_ISON_1)
    ielevator_1=iELEVATOR(up=hw.ELEVATOR_MOVEUP_1,down=hw.ELEVATOR_MOVEDOWN_1,above=hw.ELEVATOR_ABOVE_1,below=hw.ELEVATOR_BELOW_1)
    return (imotor_1,ielevator_1,igate_1)

instances = ()
if platform=='linux' or True:
    instances+=imitation()

if plc: plc.run(instances=instances,ctx=globals())
