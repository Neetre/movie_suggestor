import React, { useState, FormEvent, useEffect } from 'react';

const MovieRecommender: React.FC = () => {
  const [title, setTitle] = useState<string>('');
  const [recommendations, setRecommendations] = useState<string[]>([]);
  const [error, setError] = useState<string>('');
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
  
    try {
      const response = await fetch('http://localhost:5000/similar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `title=${encodeURIComponent(title)}`
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data: string[] = await response.json();
      setRecommendations(data);
      setError('');
    } catch (err) {
      setError('Error fetching recommendations. Please check the server connection.');
      console.error('Fetch error:', err);
    }
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${isDarkMode ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
      <div className="container mx-auto px-4 max-w-2xl pt-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 dark:text-gray-100">Movie Recommender</h1>
          <button
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="relative rounded-full w-12 h-6 bg-gray-200 dark:bg-gray-700 transition-colors"
          >
            <div className={`absolute top-1 w-4 h-4 rounded-full transform transition-transform duration-300 
              ${isDarkMode ? 'translate-x-6 bg-blue-400' : 'translate-x-1 bg-yellow-400'}`} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 shadow-md rounded px-8 pt-6 pb-8 mb-6">
          <div className="mb-4">
            <label className="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2" htmlFor="title">
              Movie Title
            </label>
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter movie title"
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 
                dark:bg-gray-700 dark:border-gray-600 dark:text-white
                focus:ring-blue-500 dark:focus:ring-blue-400"
              required
            />
          </div>
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 
              text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline 
              transition-colors w-full"
          >
            Get Recommendations
          </button>
        </form>

        <div className="mt-8">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 dark:bg-red-200 dark:border-red-500 
              dark:text-red-900 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          {recommendations.length > 0 ? (
            <div className="bg-white dark:bg-gray-800 shadow-md rounded px-8 pt-6 pb-8">
              <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">Recommendations:</h3>
              <ul className="divide-y divide-gray-200 dark:divide-gray-700">
                {recommendations.map((movie, index) => (
                  <li 
                    key={index}
                    className="px-4 py-2 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors
                      text-gray-700 dark:text-gray-300"
                  >
                    {movie}
                  </li>
                ))}
              </ul>
            </div>
          ) : (
            recommendations.length === 0 && !error && (
              <p className="text-gray-600 dark:text-gray-400 text-center">
                No recommendations found.
              </p>
            )
          )}
        </div>
      </div>
    </div>
  );
};

export default MovieRecommender;