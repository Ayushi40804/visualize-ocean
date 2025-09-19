import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Lightbulb, TrendingUp, AlertCircle } from 'lucide-react';
import { ChatMessage, AgroBot } from '../types';
import { InteractiveMap } from './InteractiveMap';

interface AIChatProps {
  selectedBot: AgroBot | null;
  onBotSelect: (bot: AgroBot) => void;
}

const initialMessages: ChatMessage[] = [
  {
    id: '1',
    type: 'ai',
    content: 'Hello! I\'m your AI marine research assistant. I can help you analyze ocean data, interpret sensor readings, provide insights about marine life patterns, and answer questions about the blue economy. What would you like to explore today?',
    timestamp: new Date().toISOString()
  }
];

const suggestedQuestions = [
  'What are the current ocean temperature trends?',
  'Analyze pollution levels in the monitored areas',
  'Show me marine life migration patterns',
  'What\'s the optimal fishing time based on current data?',
  'Explain the correlation between temperature and pH levels',
  'Predict cyclone formation risk this week'
];

export function AIChat({ selectedBot, onBotSelect }: AIChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateAIResponse = (userMessage: string): string => {
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes('temperature') || lowerMessage.includes('thermal')) {
      return 'Based on the latest data from our Agro-Bot network, ocean temperatures in the Indian Ocean are showing a 1.2°C increase compared to seasonal averages. Agro-Bot Delta reported the highest reading at 26.1°C. This elevation could indicate:\n\n• Potential coral bleaching risk in shallow areas\n• Altered marine life behavior patterns\n• Changes in current circulation\n\nI recommend monitoring the thermal stratification and checking dissolved oxygen levels, which typically decrease with higher temperatures.';
    }
    
    if (lowerMessage.includes('pollution') || lowerMessage.includes('contamination')) {
      return 'Current pollution analysis reveals:\n\n🔴 **Alert Zone**: Agro-Bot Beta detected elevated hydrocarbon traces (pollution index: 3.2)\n🟡 **Moderate Concern**: pH fluctuations near industrial shipping lanes\n🟢 **Clean Areas**: Southern monitoring stations show normal baseline levels\n\n**Recommendations**:\n• Deploy additional monitoring in alert zones\n• Coordinate with maritime authorities on shipping route adjustments\n• Increase sampling frequency for the next 48 hours';
    }
    
    if (lowerMessage.includes('marine life') || lowerMessage.includes('migration') || lowerMessage.includes('fish')) {
      return 'Marine life analysis indicates several interesting patterns:\n\n🐟 **Fish Migration**: Large pelagic species are moving southeast, likely following temperature gradients\n🐢 **Turtle Activity**: Increased nesting activity detected near Mauritius (seasonal pattern)\n🦈 **Predator Movement**: Shark tracking shows concentration near deeper channels\n\n**Fishing Recommendations**:\n• Best fishing zones: 18-20°S, 60-62°E\n• Optimal times: Early morning (5-7 AM) and late afternoon (4-6 PM)\n• Target species: Yellowfin tuna showing increased activity';
    }
    
    if (lowerMessage.includes('cyclone') || lowerMessage.includes('storm') || lowerMessage.includes('weather')) {
      return 'Weather analysis and cyclone risk assessment:\n\n⚠️ **Current Status**: Tropical disturbance detected 300km southeast\n📈 **Risk Level**: Moderate (40% chance of cyclone development)\n🌡️ **Key Factors**: Sea surface temperature 28.5°C (above cyclone threshold)\n\n**72-hour Forecast**:\n• Wind speeds may increase to 65-85 km/h\n• Wave heights: 3-4 meters\n• Recommended action: Monitor closely, prepare contingency plans for maritime operations';
    }
    
    if (lowerMessage.includes('correlation') || lowerMessage.includes('relationship')) {
      return 'Data correlation analysis reveals several key relationships:\n\n📊 **Temperature vs pH**: Strong negative correlation (-0.73)\n• As temperature increases, pH tends to decrease (ocean acidification)\n• Critical threshold appears around 26°C\n\n📊 **Salinity vs Oxygen**: Moderate positive correlation (0.58)\n• Higher salinity areas show better oxygen retention\n• Deep water masses maintain stable ratios\n\n💡 **Insight**: Current temperature anomalies are driving pH changes faster than expected, suggesting accelerated acidification in warmer zones.';
    }
    
    // Default responses for general queries
    const defaultResponses = [
      'Based on the current data from our Agro-Bot network, I can see several interesting patterns. The ocean conditions are generally stable, though we\'re monitoring some thermal anomalies. Would you like me to focus on any specific parameter?',
      'The marine ecosystem in your monitored areas is showing typical seasonal variations. Water quality parameters are within normal ranges, with some localized variations that I can analyze further. What specific aspect interests you most?',
      'Our AI analysis of the latest sensor data indicates optimal conditions for marine research. The current flow patterns and temperature gradients suggest interesting opportunities for data collection. How can I assist with your research objectives?'
    ];
    
    return defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Simulate AI thinking time
    setTimeout(() => {
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: generateAIResponse(userMessage.content),
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1500 + Math.random() * 1000);
  };

  const handleSuggestionClick = (question: string) => {
    setInputValue(question);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 min-h-[calc(100vh-8rem)]">
      {/* AI Chat Panel */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow flex flex-col min-h-[600px] h-fit order-1 xl:order-none">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="bg-blue-100 dark:bg-blue-900/50 p-2 rounded-lg mr-3">
              <Bot className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">AI Marine Assistant</h2>
              <p className="text-sm text-gray-600 dark:text-gray-300">Powered by advanced ocean data analytics</p>
            </div>
          </div>
        </div>

      {/* Suggested Questions */}
      {messages.length <= 1 && (
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3 flex items-center">
            <Lightbulb className="w-4 h-4 mr-2" />
            Suggested Questions
          </h3>
          <div className="grid grid-cols-1 gap-2 max-h-32 overflow-y-auto">
            {suggestedQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(question)}
                className="text-left text-sm bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg p-3 hover:border-blue-300 dark:hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors text-gray-900 dark:text-gray-100"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[400px] min-h-[300px]">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-3xl flex ${
                message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
              } items-start space-x-3`}
            >
              <div
                className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300'
                }`}
              >
                {message.type === 'user' ? (
                  <User className="w-4 h-4" />
                ) : (
                  <Bot className="w-4 h-4" />
                )}
              </div>
              <div
                className={`rounded-lg px-4 py-3 ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white ml-3'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 mr-3'
                }`}
              >
                <div className="text-sm whitespace-pre-wrap">
                  {message.content}
                </div>
                <div
                  className={`text-xs mt-2 ${
                    message.type === 'user' ? 'text-blue-200' : 'text-gray-500 dark:text-gray-400'
                  }`}
                >
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </div>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex justify-start">
            <div className="max-w-3xl flex flex-row items-start space-x-3">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 flex items-center justify-center">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-lg px-4 py-3">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

        {/* Input */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <div className="flex space-x-3">
            <div className="flex-1 relative">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about ocean conditions, marine life, data analysis, or the blue economy..."
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                rows={1}
                style={{ minHeight: '44px', maxHeight: '120px' }}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isTyping}
              className="bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          <div className="flex items-center justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
            <span>Press Enter to send, Shift+Enter for new line</span>
            <div className="flex items-center space-x-4">
              <span className="flex items-center">
                <TrendingUp className="w-3 h-3 mr-1" />
                Live data analysis
              </span>
              <span className="flex items-center">
                <AlertCircle className="w-3 h-3 mr-1" />
                Real-time insights
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Map Panel */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow min-h-[600px] order-2 xl:order-none">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Live Ocean Map</h3>
          <p className="text-sm text-gray-600 dark:text-gray-300">Click on Agro-Bots to analyze data</p>
        </div>
        <div className="p-4">
          <InteractiveMap onBotSelect={onBotSelect} selectedBot={selectedBot} />
        </div>
      </div>
    </div>
  );
}