import os
import logging as log
import sys
from openvino.inference_engine import IENetwork,IECore

class Network:
    def __init__(self):
        self.plugin = None
        self.network = None
        self.input_blob = None
        self.output_blob = None
        self.exec_network = None
        self.infer_request = None
    
    def load_model(self,model,device="CPU",cpu_extension=None):
        model_xml = model
        model_bin = os.path.splitext(model_xml)[0]+".bin"
        print(model_bin)
        self.plugin = IECore()
        if cpu_extension and "CPU" in device:
            self.plugin.add_extension(cpu_extension, device)
        self.network = IENetwork(model=model_xml,weights=model_bin)
        self.exec_network = self.plugin.load_network(self.network,device)
        self.input_blob = next(iter(self.network.inputs))
        self.output_blob    = next(iter(self.network.outputs))
        return
    
    def get_input_shape(self):
        return self.network.inputs[self.input_blob].shape
    	
    	
    def async_inference(self,image):
        request_handler = self.exec_network.start_async(request_id=0,inputs={self.input_blob:image})
        status = self.exec_network.requests[0].wait()
    
    def sync_inference(self,image):
        res = self.exec_network.infer(inputs={self.input_blob:image})
        return res["Mconv7_stage6"]
    
    	
    def wait():
        status = self.exec_network.requests[0].wait()
        return status
    
    def extract_outputs(self):
        return self.exec_network.requests[0].outputs[self.output_blob]
    		
    
    
