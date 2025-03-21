from typing import Dict, Any, Optional
import openai
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from ..core.config import settings

class AIService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.llm = OpenAI(temperature=0.7, api_key=settings.OPENAI_API_KEY)
        
        # Initialize basic prompt templates
        self.decision_prompt = PromptTemplate(
            input_variables=["context", "options"],
            template="""
            Based on the following context and options, provide a decision recommendation:
            
            Context: {context}
            Options: {options}
            
            Please analyze the situation and provide a recommendation with explanation.
            """
        )
        
        self.analysis_prompt = PromptTemplate(
            input_variables=["data", "question"],
            template="""
            Analyze the following data and answer the question:
            
            Data: {data}
            Question: {question}
            
            Please provide a detailed analysis.
            """
        )

    async def get_decision(self, context: Dict[str, Any], options: list) -> Dict[str, Any]:
        """Generate a decision based on context and available options."""
        chain = LLMChain(llm=self.llm, prompt=self.decision_prompt)
        
        result = await chain.arun(
            context=str(context),
            options=str(options)
        )
        
        return {
            "decision": result,
            "confidence_score": 0.8,  # Placeholder - implement actual confidence scoring
            "metadata": {
                "model": "gpt-4",
                "timestamp": datetime.utcnow().isoformat()
            }
        }

    async def analyze_data(self, data: Dict[str, Any], question: str) -> Dict[str, Any]:
        """Analyze data and answer specific questions."""
        chain = LLMChain(llm=self.llm, prompt=self.analysis_prompt)
        
        result = await chain.arun(
            data=str(data),
            question=question
        )
        
        return {
            "analysis": result,
            "confidence_score": 0.8,  # Placeholder - implement actual confidence scoring
            "metadata": {
                "model": "gpt-4",
                "timestamp": datetime.utcnow().isoformat()
            }
        }

    async def get_recommendation(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized recommendations based on user context."""
        prompt = f"""
        Based on the following user context, provide personalized recommendations:
        
        User Context: {user_context}
        
        Please provide actionable recommendations with explanations.
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a business intelligence AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {
            "recommendations": response.choices[0].message.content,
            "confidence_score": 0.8,  # Placeholder - implement actual confidence scoring
            "metadata": {
                "model": "gpt-4",
                "timestamp": datetime.utcnow().isoformat()
            }
        } 