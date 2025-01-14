import google.generativeai as genai

class Gemini:
    def __init__(self, api_key, model_name):
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name)

    def generate_content(self, prompt):
        response = self._model.generate_content(prompt)
        return response.text

    def suggest_preparation(self, testplan_description, user_information):
        prompt_template = f"""
        You are an expert assistant designed to help individuals prepare for specific test plans by analyzing their current skills and experience against the requirements of the test plan.
        Below are two inputs:
        user_information: This is a string describing the user's skills, experience, certifications, and technical proficiency.
        testplan_description: This is a string describing the test plan, including required skills, prerequisites, and objectives.
        Your task is to:
        Analyze the Skills Gap: Identify which skills/tools the user already possesses that align with the test plan requirements and which skills/tools the user needs to learn or improve to meet the objectives.
        Provide Learning Recommendations: Suggest topics, tools, or concepts the user should focus on to bridge the skills gap. If possible, recommend specific courses, certifications, or online resources to help the user upskill.
        Develop a Preparation Plan: Propose actionable steps the user can take to prepare effectively for the test plan, including strategies for hands-on practice or gaining relevant experience.
        Inputs:
        user_information:
        {user_information}
        testplan_description:
        {testplan_description}
        Expected Output:
        Skills Gap Analysis: Clearly outline the alignment between the user’s skills and the test plan requirements, and highlight the gaps.
        Learning Recommendations: Provide specific and actionable learning suggestions, including resources such as courses, certifications, or tools to explore.
        Preparation Plan: Suggest a step-by-step plan for the user to prepare for the test plan, emphasizing practical experience and skill-building activities.
        Ensure the response is clear, actionable, and tailored to the provided inputs.
        """
        return self.generate_content(prompt_template)