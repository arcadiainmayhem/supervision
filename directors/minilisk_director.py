from minilisk.thermal_compositor import compose_slip
from minilisk.thermal_assembler import assemble
from core.installation_constants import DEV_MODE

class MiniliskDirector():
    
    
    def __init__(self):
        self.isPrinting = False
        self.printer = self._init_printer()


    def _init_printer(self):
        if DEV_MODE:
            return None
        else:
            #TODO ESCPOS USB Printer init
            pass

        

    def produce_thermal_slip(self, visitor, decider_data):
        print("Assembling thermal..")
        assembled = assemble(visitor , decider_data)
        print("Composing thermal..")
        output = compose_slip(assembled)
        print("Showing thermal..")
    
        if DEV_MODE:
            output.show()
        else:
            self._print_thermal_slip(output)
            
        return output
    
    def _print_thermal_slip(self, visitor):
        #send to THERMAL PRINTER via python escpos
        pass