import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import LocationSearch from './components/LocationSearch';
import RestaurantDetails from './components/RestaurantDetails'; // Assuming this shows details
import RestaurantDetailPage from './components/RestaurantDetailPage'; // If this is different, adjust its path

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search-location" element={<LocationSearch />} />
        <Route path="/restaurant/:id" element={<RestaurantDetails />} />
        {/* Example: If RestaurantDetailPage serves another purpose, update its path */}
        <Route path="/restaurant-detail/:id" element={<RestaurantDetailPage />} />
      </Routes>
    </Router>
  );
}

export default App;
