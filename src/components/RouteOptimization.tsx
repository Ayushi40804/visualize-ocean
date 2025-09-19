import React, { useState } from 'react';
import { Navigation, Fuel, Clock, Wind, MapPin, Plus, Save } from 'lucide-react';
import { Route } from '../types';

const mockRoutes: Route[] = [
  {
    id: '1',
    name: 'Mauritius to Seychelles',
    startPoint: { latitude: -20.348404, longitude: 57.552152 },
    endPoint: { latitude: -4.679574, longitude: 55.491977 },
    optimizedPath: [
      { latitude: -20.348404, longitude: 57.552152 },
      { latitude: -18.0, longitude: 57.0 },
      { latitude: -15.0, longitude: 56.5 },
      { latitude: -12.0, longitude: 56.0 },
      { latitude: -8.0, longitude: 55.8 },
      { latitude: -4.679574, longitude: 55.491977 }
    ],
    estimatedTime: '2 days 14 hours',
    fuelSavings: 15.2,
    weatherConditions: 'Favorable'
  },
  {
    id: '2',
    name: 'Fishing Route Alpha',
    startPoint: { latitude: -16.0, longitude: 60.0 },
    endPoint: { latitude: -20.0, longitude: 63.0 },
    optimizedPath: [
      { latitude: -16.0, longitude: 60.0 },
      { latitude: -17.5, longitude: 61.0 },
      { latitude: -19.0, longitude: 62.0 },
      { latitude: -20.0, longitude: 63.0 }
    ],
    estimatedTime: '18 hours',
    fuelSavings: 8.7,
    weatherConditions: 'Moderate winds'
  }
];

export function RouteOptimization() {
  const [routes, setRoutes] = useState<Route[]>(mockRoutes);
  const [selectedRoute, setSelectedRoute] = useState<Route | null>(null);
  const [isCreatingRoute, setIsCreatingRoute] = useState(false);
  const [newRoute, setNewRoute] = useState({
    name: '',
    startLat: '',
    startLng: '',
    endLat: '',
    endLng: ''
  });

  const createOptimizedRoute = () => {
    if (newRoute.name && newRoute.startLat && newRoute.startLng && newRoute.endLat && newRoute.endLng) {
      const route: Route = {
        id: Date.now().toString(),
        name: newRoute.name,
        startPoint: {
          latitude: parseFloat(newRoute.startLat),
          longitude: parseFloat(newRoute.startLng)
        },
        endPoint: {
          latitude: parseFloat(newRoute.endLat),
          longitude: parseFloat(newRoute.endLng)
        },
        optimizedPath: [
          { latitude: parseFloat(newRoute.startLat), longitude: parseFloat(newRoute.startLng) },
          { latitude: parseFloat(newRoute.endLat), longitude: parseFloat(newRoute.endLng) }
        ],
        estimatedTime: '1 day 8 hours',
        fuelSavings: Math.random() * 20,
        weatherConditions: 'Calculating...'
      };

      setRoutes([...routes, route]);
      setNewRoute({ name: '', startLat: '', startLng: '', endLat: '', endLng: '' });
      setIsCreatingRoute(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Route Optimization</h2>
            <p className="text-gray-600">AI-powered maritime navigation and fleet management</p>
          </div>
          <button
            onClick={() => setIsCreatingRoute(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center"
          >
            <Plus className="w-4 h-4 mr-2" />
            New Route
          </button>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="flex items-center">
              <Navigation className="w-5 h-5 text-blue-600 mr-2" />
              <div>
                <p className="text-sm font-medium text-blue-900">Active Routes</p>
                <p className="text-2xl font-bold text-blue-700">{routes.length}</p>
              </div>
            </div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="flex items-center">
              <Fuel className="w-5 h-5 text-green-600 mr-2" />
              <div>
                <p className="text-sm font-medium text-green-900">Avg. Fuel Savings</p>
                <p className="text-2xl font-bold text-green-700">
                  {(routes.reduce((sum, r) => sum + r.fuelSavings, 0) / routes.length).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg">
            <div className="flex items-center">
              <Clock className="w-5 h-5 text-orange-600 mr-2" />
              <div>
                <p className="text-sm font-medium text-orange-900">Time Saved</p>
                <p className="text-2xl font-bold text-orange-700">24h</p>
              </div>
            </div>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <div className="flex items-center">
              <Wind className="w-5 h-5 text-purple-600 mr-2" />
              <div>
                <p className="text-sm font-medium text-purple-900">Weather Factor</p>
                <p className="text-2xl font-bold text-purple-700">92%</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Route List */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Optimized Routes</h3>
          </div>
          <div className="divide-y divide-gray-200">
            {routes.map((route) => (
              <div
                key={route.id}
                className={`p-4 cursor-pointer hover:bg-gray-50 ${
                  selectedRoute?.id === route.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
                }`}
                onClick={() => setSelectedRoute(route)}
              >
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900">{route.name}</h4>
                  <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                    -{route.fuelSavings.toFixed(1)}% fuel
                  </span>
                </div>
                <div className="text-sm text-gray-600 space-y-1">
                  <div className="flex items-center">
                    <MapPin className="w-3 h-3 mr-1" />
                    <span>From: {route.startPoint.latitude.toFixed(2)}, {route.startPoint.longitude.toFixed(2)}</span>
                  </div>
                  <div className="flex items-center">
                    <Navigation className="w-3 h-3 mr-1" />
                    <span>To: {route.endPoint.latitude.toFixed(2)}, {route.endPoint.longitude.toFixed(2)}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <Clock className="w-3 h-3 mr-1" />
                      <span>{route.estimatedTime}</span>
                    </div>
                    <div className="flex items-center">
                      <Wind className="w-3 h-3 mr-1" />
                      <span>{route.weatherConditions}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Route Details / Map */}
        <div className="bg-white rounded-lg shadow">
          {selectedRoute ? (
            <>
              <div className="p-6 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">{selectedRoute.name}</h3>
                <p className="text-sm text-gray-600">Optimized route visualization</p>
              </div>
              <div className="p-6">
                <div className="bg-gradient-to-br from-blue-500 to-blue-700 rounded-lg h-64 mb-4 relative overflow-hidden">
                  <svg viewBox="0 0 400 200" className="w-full h-full">
                    <defs>
                      <pattern id="ocean-pattern" patternUnits="userSpaceOnUse" width="20" height="10">
                        <path d="M0 5 Q5 0 10 5 T20 5" stroke="#ffffff30" strokeWidth="0.5" fill="none"/>
                      </pattern>
                    </defs>
                    <rect width="400" height="200" fill="url(#ocean-pattern)" />
                    
                    {/* Route path */}
                    <path
                      d={`M ${50} ${150} Q ${150} ${100} ${250} ${80} T ${350} ${50}`}
                      stroke="#FFC107"
                      strokeWidth="3"
                      fill="none"
                      strokeDasharray="5,5"
                      className="animate-pulse"
                    />
                    
                    {/* Start point */}
                    <circle cx="50" cy="150" r="6" fill="#10B981" stroke="white" strokeWidth="2" />
                    <text x="50" y="170" textAnchor="middle" fill="white" fontSize="10">START</text>
                    
                    {/* End point */}
                    <circle cx="350" cy="50" r="6" fill="#EF4444" stroke="white" strokeWidth="2" />
                    <text x="350" y="40" textAnchor="middle" fill="white" fontSize="10">END</text>
                  </svg>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="text-sm font-medium text-gray-700">Estimated Time</p>
                    <p className="text-lg font-semibold text-gray-900">{selectedRoute.estimatedTime}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="text-sm font-medium text-gray-700">Fuel Savings</p>
                    <p className="text-lg font-semibold text-green-600">{selectedRoute.fuelSavings.toFixed(1)}%</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="text-sm font-medium text-gray-700">Weather</p>
                    <p className="text-lg font-semibold text-gray-900">{selectedRoute.weatherConditions}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="text-sm font-medium text-gray-700">Waypoints</p>
                    <p className="text-lg font-semibold text-gray-900">{selectedRoute.optimizedPath.length}</p>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="p-8 text-center">
              <Navigation className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Route Selected</h3>
              <p className="text-gray-600">Select a route from the list to view optimization details</p>
            </div>
          )}
        </div>
      </div>

      {/* Create Route Modal */}
      {isCreatingRoute && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Route</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Route Name</label>
                <input
                  type="text"
                  value={newRoute.name}
                  onChange={(e) => setNewRoute({ ...newRoute, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter route name"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Start Latitude</label>
                  <input
                    type="number"
                    value={newRoute.startLat}
                    onChange={(e) => setNewRoute({ ...newRoute, startLat: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="-20.0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Start Longitude</label>
                  <input
                    type="number"
                    value={newRoute.startLng}
                    onChange={(e) => setNewRoute({ ...newRoute, startLng: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="57.5"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">End Latitude</label>
                  <input
                    type="number"
                    value={newRoute.endLat}
                    onChange={(e) => setNewRoute({ ...newRoute, endLat: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="-4.7"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">End Longitude</label>
                  <input
                    type="number"
                    value={newRoute.endLng}
                    onChange={(e) => setNewRoute({ ...newRoute, endLng: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="55.5"
                  />
                </div>
              </div>
            </div>
            <div className="flex space-x-3 mt-6">
              <button
                onClick={createOptimizedRoute}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 flex items-center justify-center"
              >
                <Save className="w-4 h-4 mr-2" />
                Create Route
              </button>
              <button
                onClick={() => setIsCreatingRoute(false)}
                className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-400"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}