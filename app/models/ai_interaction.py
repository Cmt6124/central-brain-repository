from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AIInteraction(Base):
    __tablename__ = "ai_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    interaction_type = Column(String)  # e.g., "decision", "recommendation", "analysis"
    context = Column(JSON)  # Store the context of the interaction
    input_data = Column(JSON)  # Store the input data
    output_data = Column(JSON)  # Store the AI's response
    confidence_score = Column(Float)  # AI's confidence in the decision
    metadata = Column(JSON)  # Additional metadata about the interaction

    def __repr__(self):
        return f"<AIInteraction(id={self.id}, type={self.interaction_type}, timestamp={self.timestamp})>" 