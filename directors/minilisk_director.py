from minilisk.thermal_compositor import compose_slip , print_thermal_slip_escpos
from minilisk.thermal_assembler import assemble
from core.installation_constants import *
from PIL import Image
class MiniliskDirector():
    
    
    def __init__(self):
        self.isPrinting = False
        self.printer = self._init_printer()


    def _init_printer(self):
        if DEV_MODE:
            return None
        else:
            #TODO ESCPOS USB Printer init
            from escpos.printer import Usb
            vendor_id = THERMAL_VENDOR_ID
            product_id = THERMAL_PRODUCT_ID
            return Usb(vendor_id,product_id)

        

    def composite_thermal_slip(self, visitor):
        print("Assembling thermal..")
        assembled = visitor["assembled_slip"] 
        print("Composing thermal..")
        output = compose_slip(assembled)
        print("Showing thermal..")

        return output
    
    def assemble_slip(self, visitor):
        visitor["assembled_slip"] = assemble(visitor)

    def prepare_thermal_slip_print(self,visitor):
        if DEV_MODE:
           img = Image.open(visitor["output_path"])
           img.show()
        else:
            self._print_thermal_slip(visitor)

    

    def _print_thermal_slip(self, visitor):
        #send to THERMAL PRINTER via python escpos
        # try:
        #     filepath = visitor["output_path"]
        #     img = Image.open(filepath)
        #     self.printer.image(img)
        #     self.printer.cut()
        #     print("Thermal : Print Sent Successfully")
        # except Exception as e:
        #     print(f"Thermal: Print Failed {e}")
        assembled_data = visitor["assembled_slip"]

        print_thermal_slip_escpos(assembled_data,self.printer)