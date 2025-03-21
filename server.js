const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors({
  origin: '*', // Allow all origins in development
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json());

// MongoDB Connection with retry logic
const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
      serverSelectionTimeoutMS: 5000
    });
    console.log('MongoDB Connected:', conn.connection.host);
  } catch (error) {
    console.error('MongoDB connection error:', error);
    // Retry connection after 5 seconds
    setTimeout(connectDB, 5000);
  }
};

connectDB();

// Chat Message Schema
const messageSchema = new mongoose.Schema({
  text: String,
  isAI: Boolean,
  isUser: Boolean,
  timestamp: { type: Date, default: Date.now }
});

const Message = mongoose.model('Message', messageSchema);

// Chat endpoints
app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;
    
    // Save user message
    const userMessage = new Message({
      text: message,
      isUser: true,
      timestamp: new Date()
    });
    await userMessage.save();

    // Generate AI response (placeholder for now)
    const aiResponse = "I understand your message: " + message + ". How can I help you further?";
    
    // Save AI response
    const aiMessage = new Message({
      text: aiResponse,
      isAI: true,
      timestamp: new Date()
    });
    await aiMessage.save();

    res.json({ message: aiResponse });
  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({ error: 'Failed to process message' });
  }
});

app.get('/api/chat', async (req, res) => {
  try {
    const messages = await Message.find().sort({ timestamp: 1 });
    res.json(messages);
  } catch (error) {
    console.error('Get chat history error:', error);
    res.status(500).json({ error: 'Failed to get chat history' });
  }
});

// Health Check Routes
app.get('/', (req, res) => {
  res.json({ 
    message: 'Central Brain API is running',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    services: {
      server: 'up',
      mongodb: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected'
    },
    timestamp: new Date().toISOString(),
    env: process.env.NODE_ENV
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ 
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV}`);
  console.log(`MongoDB URI: ${process.env.MONGODB_URI?.split('@')[1]}`); // Log only the host part
}); 