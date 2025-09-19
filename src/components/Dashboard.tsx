import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Sidebar } from './Sidebar';
import { Overview } from './Overview';
import { Alerts } from './Alerts';
import { RouteOptimization } from './RouteOptimization';
import { AIChat } from './AIChat';
import { Settings } from './Settings';
import { AgroBot } from '../types';

export function Dashboard() {
  const { user } = useAuth();
  const [activeSection, setActiveSection] = useState('overview');
  const [selectedBot, setSelectedBot] = useState<AgroBot | null>(null);

  const renderContent = () => {
    switch (activeSection) {
      case 'overview':
        return <Overview selectedBot={selectedBot} />;
      case 'alerts':
        return <Alerts />;
      case 'routes':
        return <RouteOptimization />;
      case 'chat':
        return <AIChat selectedBot={selectedBot} onBotSelect={setSelectedBot} />;
      case 'settings':
        return <Settings />;
      default:
        return <Overview selectedBot={selectedBot} />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar 
        selectedBot={selectedBot}
        onSectionChange={setActiveSection}
        activeSection={activeSection}
      />
      
      <main className="flex-1 overflow-auto">
        <div className="p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Welcome back, {user?.name}
            </h1>
            <p className="text-gray-600 dark:text-gray-300 capitalize">
              {user?.role?.replace('_', ' ')} Dashboard
            </p>
          </div>
          
          {renderContent()}
        </div>
      </main>
    </div>
  );
}