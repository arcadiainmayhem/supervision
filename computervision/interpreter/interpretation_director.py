from computervision.interpreter.presence_interpreter import interpret_presence
from computervision.interpreter.time_interpreter import intepret_time
from computervision.interpreter.expression_interpreter import intepret_expression
from computervision.interpreter.context_interpreter import intepret_context
from core.generators.context_reader import get_context


def intepret_everything(visitor):
    
    get_context(visitor)        # ← writes moon_phase, element, numerology to visitor

    interpret_presence(visitor)
    intepret_time(visitor)
    intepret_expression(visitor)
    intepret_context(visitor)