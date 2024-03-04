class Healing prediction:
    def __init__(self, height, weight, gender, program):
        self.height = height
        self.weight = weight
        self.gender = gender
        self.program = program
    
    def validate_input(self):
        try:
            float(self.height)
            float(self.weight)
        except ValueError:
            return False
        if self.gender not in ['남성', '여성']:
            return False
        if self.program not in ['등산로', '숲길', '재배', '치유']:
            return False
        return True
    
    def predict_healing_effect(self):
        if self.validate_input():
            return '36kcal'
        else:
            return 'error'
    
    @classmethod
    def prompt_and_predict(cls, height, weight, gender, program):
        instance = cls(height, weight, gender, program)
        return instance.predict_health_effect()


HealthEffectPredictor.prompt_and_predict(188, 88, '여성', '치유')

