import matlab.engine
import os

class FSDA:
    def __init__(self, fsda_toolbox_path=None):
        self.eng = matlab.engine.start_matlab()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        matlab_engine_path = os.path.join(current_dir, 'matlab_engine')
        self.eng.addpath(matlab_engine_path, nargout=0)

        if fsda_toolbox_path:
            self.eng.addpath(fsda_toolbox_path, nargout=0)

        self.wrapper = self.eng.FSDAEngine()

    def run(self, func_name, *args):
        return self.eng.feval('execute', self.wrapper, func_name, *args, nargout=1)

    def close(self):
        self.eng.quit()