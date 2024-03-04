class ProgramRecommender:
    available_program_types = ["등산로", "숲 체험", "둘레길", "산림 치유원"]
    available_children_status = ["Y", "N"]
    available_jobs = ["사무직", "주부", "학생", "생산직", "무직"]
    recommended_programs = [
        "프로그램 1", "프로그램 2", "프로그램 3", "프로그램 4", "프로그램 5",
        "프로그램 6", "프로그램 7", "프로그램 8", "프로그램 9", "프로그램 10"
    ]
    
    @staticmethod
    def validate_input(program_type, age, children, job):
        if program_type not in ProgramRecommender.available_program_types:
            return False
        if not isinstance(age, int):
            return False
        if children not in ProgramRecommender.available_children_status:
            return False
        if job not in ProgramRecommender.available_jobs:
            return False
        return True

    @staticmethod
    def get_recommendations(program_type, age, children, job, location, gender):
        if ProgramRecommender.validate_input(program_type, age, children, job):
            return ProgramRecommender.recommended_programs
        else:
            return "ERROR"

#이 부분이 input -> output 실행
print(ProgramRecommender.get_recommendations("등산로", 35, "Y", "사무직", "서울시 강동구", "남성"))
