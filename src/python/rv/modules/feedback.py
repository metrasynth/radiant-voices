from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.feedback import BaseFeedback


class Feedback(BaseFeedback, Module):

    behaviors = {B.receives_audio, B.receives_feedback, B.sends_audio, B.sends_feedback}
