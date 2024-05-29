import time
import random
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx

class ConversationTranscriber():
 
    def __init__(self, callback: callable):
        self.callback = callback
        self.running=True
        random.seed(5)

    def transcribe(self, filename: str):
        def dummy():
            while self.running:
                result = Object(speaker_id="foo", text="bar-"+str(random.random()))
                event = Object(result=result)
                self.callback(event)
                time.sleep(1)
        t = threading.Thread(target=add_script_run_ctx(dummy))
        t.start()

    def stop(self):
        self.running=False


class Object(object):
    '''
    Creates an object for simple key/value storage; enables access via
    object or dictionary syntax (i.e. obj.foo or obj['foo']).
    '''

    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __getitem__(self, prop):
        '''
        Enables dict-like access, ie. foo['bar']
        '''
        return self.__getattribute__(prop)

    def __str__(self):
        '''
        String-representation as newline-separated string useful in print()
        '''
        state = [f'{attr}: {val}' for (attr, val) in self.__dict__.items()]
        return '\n'.join(state)

    def items(self):
        '''
        Enables enumeration via foo.items()
        '''
        return self.__dict__.items()