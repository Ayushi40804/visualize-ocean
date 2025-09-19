import React, { useState } from 'react';
import { AlertTriangle, Clock, MapPin, CheckCircle, X } from 'lucide-react';
import { Alert } from '../types';

const mockAlerts: Alert[] = [
  {
    id: '1',
    type: 'cyclone',
    severity: 'critical',
    title: 'Tropical Cyclone Belal Approaching',
    description: 'Category 4 cyclone detected 180km southeast of Mauritius. Wind speeds up to 220 km/h. All maritime activities should be suspended immediately.',
    location: { latitude: -22.0, longitude: 59.0 },
    timestamp: '2024-01-15T10:00:00Z',
    isRead: false
  },
  {
    id: '2',
    type: 'anomaly',
    severity: 'high',
    title: 'Temperature Anomaly Detected',
    description: 'Ocean temperature 3.2°C above seasonal average detected by Agro-Bot Delta. Possible coral bleaching risk in the area.',
    location: { latitude: -18.7, longitude: 63.1 },
    timestamp: '2024-01-15T09:45:00Z',
    isRead: false
  },
  {
    id: '3',
    type: 'pollution',
    severity: 'medium',
    title: 'Oil Spill Detection',
    description: 'Hydrocarbon traces detected in water samples. Pollution index increased to 4.2. Marine life monitoring recommended.',
    location: { latitude: -16.0, longitude: 61.0 },
    timestamp: '2024-01-15T08:30:00Z',
    isRead: true
  },
  {
    id: '4',
    type: 'equipment',
    severity: 'low',
    title: 'Sensor Calibration Required',
    description: 'Agro-Bot Gamma showing irregular pH readings. Scheduled maintenance required within 48 hours.',
    location: { latitude: -25.3, longitude: 55.8 },
    timestamp: '2024-01-15T07:15:00Z',
    isRead: true
  }
];

export function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>(mockAlerts);
  const [filter, setFilter] = useState<'all' | 'unread' | 'critical'>('all');

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'cyclone': return '🌪️';
      case 'anomaly': return '🌡️';
      case 'pollution': return '☣️';
      case 'equipment': return '⚙️';
      default: return '⚠️';
    }
  };

  const filteredAlerts = alerts.filter(alert => {
    if (filter === 'unread') return !alert.isRead;
    if (filter === 'critical') return alert.severity === 'critical';
    return true;
  });

  const markAsRead = (id: string) => {
    setAlerts(alerts.map(alert => 
      alert.id === id ? { ...alert, isRead: true } : alert
    ));
  };

  const dismissAlert = (id: string) => {
    setAlerts(alerts.filter(alert => alert.id !== id));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Alert Management</h2>
            <p className="text-gray-600">Monitor real-time ocean conditions and anomalies</p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg text-sm font-medium ${
                filter === 'all' 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              All ({alerts.length})
            </button>
            <button
              onClick={() => setFilter('unread')}
              className={`px-4 py-2 rounded-lg text-sm font-medium ${
                filter === 'unread' 
                  ? 'bg-red-100 text-red-700' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Unread ({alerts.filter(a => !a.isRead).length})
            </button>
            <button
              onClick={() => setFilter('critical')}
              className={`px-4 py-2 rounded-lg text-sm font-medium ${
                filter === 'critical' 
                  ? 'bg-red-100 text-red-700' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Critical ({alerts.filter(a => a.severity === 'critical').length})
            </button>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-red-50 p-4 rounded-lg">
            <div className="flex items-center">
              <AlertTriangle className="w-5 h-5 text-red-600 mr-2" />
              <div>
                <p className="text-sm font-medium text-red-900">Critical</p>
                <p className="text-2xl font-bold text-red-700">
                  {alerts.filter(a => a.severity === 'critical').length}
                </p>
              </div>
            </div>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg">
            <div className="flex items-center">
              <Clock className="w-5 h-5 text-orange-600 mr-2" />
              <div>
                <p className="text-sm font-medium text-orange-900">High Priority</p>
                <p className="text-2xl font-bold text-orange-700">
                  {alerts.filter(a => a.severity === 'high').length}
                </p>
              </div>
            </div>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg">
            <div className="flex items-center">
              <MapPin className="w-5 h-5 text-yellow-600 mr-2" />
              <div>
                <p className="text-sm font-medium text-yellow-900">Medium</p>
                <p className="text-2xl font-bold text-yellow-700">
                  {alerts.filter(a => a.severity === 'medium').length}
                </p>
              </div>
            </div>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 text-blue-600 mr-2" />
              <div>
                <p className="text-sm font-medium text-blue-900">Low Priority</p>
                <p className="text-2xl font-bold text-blue-700">
                  {alerts.filter(a => a.severity === 'low').length}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Alerts List */}
      <div className="space-y-4">
        {filteredAlerts.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No alerts found</h3>
            <p className="text-gray-600">
              {filter === 'all' ? 'No alerts to display' : `No ${filter} alerts at the moment`}
            </p>
          </div>
        ) : (
          filteredAlerts.map((alert) => (
            <div
              key={alert.id}
              className={`bg-white rounded-lg shadow border-l-4 ${
                alert.severity === 'critical' ? 'border-red-500' :
                alert.severity === 'high' ? 'border-orange-500' :
                alert.severity === 'medium' ? 'border-yellow-500' : 'border-blue-500'
              } ${!alert.isRead ? 'ring-2 ring-blue-100' : ''}`}
            >
              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      <span className="text-2xl mr-3">{getTypeIcon(alert.type)}</span>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{alert.title}</h3>
                        <div className="flex items-center space-x-3 mt-1">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getSeverityColor(alert.severity)}`}>
                            {alert.severity.toUpperCase()}
                          </span>
                          <span className="text-sm text-gray-500">
                            {new Date(alert.timestamp).toLocaleString()}
                          </span>
                          <span className="text-sm text-gray-500 flex items-center">
                            <MapPin className="w-3 h-3 mr-1" />
                            {alert.location.latitude.toFixed(2)}, {alert.location.longitude.toFixed(2)}
                          </span>
                        </div>
                      </div>
                    </div>
                    <p className="text-gray-700 leading-relaxed">{alert.description}</p>
                  </div>
                  
                  <div className="flex items-center space-x-2 ml-4">
                    {!alert.isRead && (
                      <button
                        onClick={() => markAsRead(alert.id)}
                        className="p-2 text-blue-600 hover:bg-blue-50 rounded-full"
                        title="Mark as read"
                      >
                        <CheckCircle className="w-4 h-4" />
                      </button>
                    )}
                    <button
                      onClick={() => dismissAlert(alert.id)}
                      className="p-2 text-gray-400 hover:bg-gray-50 rounded-full"
                      title="Dismiss alert"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}