import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);

  const [search, setSearch] = useState("");
  const [cuisine, setCuisine] = useState("");
  const [rating, setRating] = useState("");
  const [homeDelivery, setHomeDelivery] = useState(false);
  const [takeaway, setTakeaway] = useState(false);
  const [parking, setParking] = useState(false);

  const [selectedRestaurant, setSelectedRestaurant] = useState(null);

  const fetchRestaurants = () => {
    setLoading(true);

    let url = "http://127.0.0.1:8000/api/restaurants/?";

    if (cuisine) {
      url += `cuisine=${encodeURIComponent(cuisine)}&`;
    }

    if (rating) {
      url += `rating=${encodeURIComponent(rating)}&`;
    }

    if (homeDelivery) {
      url += "home_delivery=true&";
    }

    if (takeaway) {
      url += "takeaway=true&";
    }

    if (parking) {
      url += "parking=true&";
    }

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        setRestaurants(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching restaurants:", error);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchRestaurants();
  }, [cuisine, rating, homeDelivery, takeaway, parking]);

  const filteredRestaurants = restaurants.filter((restaurant) =>
    restaurant.name?.toLowerCase().includes(search.toLowerCase())
  );

  const totalRestaurants = filteredRestaurants.length;

  const ratings = filteredRestaurants
    .map((restaurant) => parseFloat(restaurant.rating))
    .filter((rating) => !isNaN(rating));

  const averageRating =
    ratings.length > 0
      ? (
          ratings.reduce((total, rating) => total + rating, 0) /
          ratings.length
        ).toFixed(1)
      : "N/A";

  const deliveryCount = filteredRestaurants.filter(
    (restaurant) => restaurant.home_delivery
  ).length;

  const takeawayCount = filteredRestaurants.filter(
    (restaurant) => restaurant.takeaway
  ).length;

  const parkingCount = filteredRestaurants.filter(
    (restaurant) => restaurant.parking
  ).length;

  const clearFilters = () => {
    setSearch("");
    setCuisine("");
    setRating("");
    setHomeDelivery(false);
    setTakeaway(false);
    setParking(false);
  };

  const closeDetails = () => {
    setSelectedRestaurant(null);
  };

  return (
    <div className="app">

      {/* Header */}

      <header className="header">

        <div className="header-content">

          <div>
            <div className="brand">
              <span className="brand-icon">🍽</span>
              <span>RestaurantHub</span>
            </div>

            <h1>Zomato Restaurant Dashboard</h1>

            <p>
              Explore, filter and discover restaurants collected from Zomato.
            </p>
          </div>

          <div className="header-badge">
            <span className="live-dot"></span>
            Live Dashboard
          </div>

        </div>

      </header>


      <main className="container">

        {/* Statistics */}

        <section className="stats-grid">

          <div className="stat-card">

            <div className="stat-icon restaurant-icon">
              🍽️
            </div>

            <div>
              <h3>{totalRestaurants}</h3>
              <p>Total Restaurants</p>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon rating-icon">
              ⭐
            </div>

            <div>
              <h3>{averageRating}</h3>
              <p>Average Rating</p>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon delivery-icon">
              🚚
            </div>

            <div>
              <h3>{deliveryCount}</h3>
              <p>Home Delivery</p>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon takeaway-icon">
              🥡
            </div>

            <div>
              <h3>{takeawayCount}</h3>
              <p>Takeaway</p>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon parking-icon">
              🅿️
            </div>

            <div>
              <h3>{parkingCount}</h3>
              <p>Parking</p>
            </div>

          </div>

        </section>


        {/* Filters */}

        <section className="filter-section">

          <div className="section-title">

            <div>
              <h2>Find Restaurants</h2>
              <p>Use filters to narrow down your results.</p>
            </div>

            <button
              className="clear-button"
              onClick={clearFilters}
            >
              ↻ Clear Filters
            </button>

          </div>


          <div className="filters">

            <div className="input-wrapper">

              <span>⌕</span>

              <input
                type="text"
                placeholder="Search restaurant..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />

            </div>


            <div className="input-wrapper">

              <span>🍴</span>

              <input
                type="text"
                placeholder="Cuisine e.g. Chinese"
                value={cuisine}
                onChange={(e) => setCuisine(e.target.value)}
              />

            </div>


            <select
              value={rating}
              onChange={(e) => setRating(e.target.value)}
            >
              <option value="">All Ratings</option>
              <option value="5">5+ ⭐</option>
              <option value="4.5">4.5+ ⭐</option>
              <option value="4">4+ ⭐</option>
              <option value="3.5">3.5+ ⭐</option>
              <option value="3">3+ ⭐</option>
            </select>


            <label className="filter-check">

              <input
                type="checkbox"
                checked={homeDelivery}
                onChange={(e) => setHomeDelivery(e.target.checked)}
              />

              <span>Home Delivery</span>

            </label>


            <label className="filter-check">

              <input
                type="checkbox"
                checked={takeaway}
                onChange={(e) => setTakeaway(e.target.checked)}
              />

              <span>Takeaway</span>

            </label>


            <label className="filter-check">

              <input
                type="checkbox"
                checked={parking}
                onChange={(e) => setParking(e.target.checked)}
              />

              <span>Parking</span>

            </label>

          </div>

        </section>


        {/* Restaurant heading */}

        <div className="dashboard-info">

          <div>
            <h2>Restaurants</h2>

            <p>
              Showing <strong>{filteredRestaurants.length}</strong> restaurants
            </p>
          </div>

          <span className="result-badge">
            {filteredRestaurants.length} Results
          </span>

        </div>


        {/* Restaurants */}

        {loading ? (

          <div className="message-box">

            <div className="loader"></div>

            <p>Loading restaurants...</p>

          </div>

        ) : filteredRestaurants.length === 0 ? (

          <div className="message-box">

            <div className="empty-icon">🍽️</div>

            <h3>No restaurants found</h3>

            <p>
              Try changing your search or filters.
            </p>

          </div>

        ) : (

          <div className="restaurant-grid">

            {filteredRestaurants.map((restaurant) => (

              <div
                className="restaurant-card"
                key={restaurant.id}
              >

                <div className="card-header">

                  <div className="restaurant-logo">
                    {restaurant.name?.charAt(0).toUpperCase() || "R"}
                  </div>

                  <div className="restaurant-title">

                    <h3>{restaurant.name}</h3>

                    <div className="rating-row">

                      <span className="rating">
                        ⭐ {restaurant.rating || "N/A"}
                      </span>

                      {restaurant.review_count && (
                        <span className="reviews">
                          {restaurant.review_count} reviews
                        </span>
                      )}

                    </div>

                  </div>

                </div>


                <div className="card-content">

                  <p className="cuisine">
                    🍽️ {restaurant.cuisines || "Cuisine not available"}
                  </p>

                  <p>
                    📍 {restaurant.address || "Address not available"}
                  </p>

                  <p>
                    💰 {restaurant.cost_for_two || "Cost not available"}
                  </p>

                  <p>
                    🕐 {restaurant.status || "Status not available"}

                    {restaurant.opening_time
                      ? ` • Opens ${restaurant.opening_time}`
                      : ""}
                  </p>


                  <div className="facilities">

                    {restaurant.home_delivery && (
                      <span>Delivery</span>
                    )}

                    {restaurant.takeaway && (
                      <span>Takeaway</span>
                    )}

                    {restaurant.parking && (
                      <span>Parking</span>
                    )}

                    {restaurant.family_friendly && (
                      <span>Family</span>
                    )}

                    {restaurant.kid_friendly && (
                      <span>Kids</span>
                    )}

                    {restaurant.luxury_dining && (
                      <span>Luxury</span>
                    )}

                  </div>

                </div>


                <div className="card-footer">

                  <button
                    className="details-button"
                    onClick={() => setSelectedRestaurant(restaurant)}
                  >
                    View Details
                    <span>→</span>
                  </button>

                </div>

              </div>

            ))}

          </div>

        )}

      </main>


      {/* Restaurant Details Modal */}

      {selectedRestaurant && (

        <div
          className="modal-overlay"
          onClick={closeDetails}
        >

          <div
            className="details-modal"
            onClick={(e) => e.stopPropagation()}
          >

            <div className="modal-header">

              <div className="modal-title-area">

                <div className="modal-logo">
                  {selectedRestaurant.name?.charAt(0).toUpperCase() || "R"}
                </div>

                <div>

                  <h2>{selectedRestaurant.name}</h2>

                  <div className="modal-rating">

                    <span>
                      ⭐ {selectedRestaurant.rating || "N/A"}
                    </span>

                    {selectedRestaurant.review_count && (
                      <span>
                        • {selectedRestaurant.review_count} reviews
                      </span>
                    )}

                  </div>

                </div>

              </div>


              <button
                className="close-button"
                onClick={closeDetails}
              >
                ×
              </button>

            </div>


            <div className="modal-body">

              {/* Basic Information */}

              <div className="detail-section">

                <h3>Restaurant Information</h3>

                <div className="detail-grid">

                  <div className="detail-item">
                    <span>🍴 Cuisines</span>
                    <strong>
                      {selectedRestaurant.cuisines || "Not available"}
                    </strong>
                  </div>

                  <div className="detail-item">
                    <span>💰 Cost for Two</span>
                    <strong>
                      {selectedRestaurant.cost_for_two || "Not available"}
                    </strong>
                  </div>

                  <div className="detail-item">
                    <span>📍 Address</span>
                    <strong>
                      {selectedRestaurant.address || "Not available"}
                    </strong>
                  </div>

                  <div className="detail-item">
                    <span>📞 Phone</span>
                    <strong>
                      {selectedRestaurant.phone || "Not available"}
                    </strong>
                  </div>

                  <div className="detail-item">
                    <span>🕐 Status</span>
                    <strong>
                      {selectedRestaurant.status || "Not available"}
                    </strong>
                  </div>

                  <div className="detail-item">
                    <span>⏰ Opening Time</span>
                    <strong>
                      {selectedRestaurant.opening_time || "Not available"}
                    </strong>
                  </div>

                </div>

              </div>


              {/* Ratings */}

              <div className="detail-section">

                <h3>Ratings</h3>

                <div className="rating-boxes">

                  <div className="rating-box">

                    <span>Overall</span>

                    <strong>
                      ⭐ {selectedRestaurant.rating || "N/A"}
                    </strong>

                  </div>


                  <div className="rating-box">

                    <span>Dining</span>

                    <strong>
                      ⭐ {selectedRestaurant.dining_rating || "N/A"}
                    </strong>

                  </div>


                  <div className="rating-box">

                    <span>Delivery</span>

                    <strong>
                      ⭐ {selectedRestaurant.delivery_rating || "N/A"}
                    </strong>

                  </div>

                </div>

              </div>


              {/* Offers */}

              {selectedRestaurant.offers && (

                <div className="detail-section">

                  <h3>Offers</h3>

                  <div className="offers-box">
                    🎁 {selectedRestaurant.offers}
                  </div>

                </div>

              )}


              {/* Facilities */}

              <div className="detail-section">

                <h3>Facilities</h3>

                <div className="modal-facilities">

                  {selectedRestaurant.digital_payments && (
                    <span>✓ Digital Payments</span>
                  )}

                  {selectedRestaurant.home_delivery && (
                    <span>✓ Home Delivery</span>
                  )}

                  {selectedRestaurant.takeaway && (
                    <span>✓ Takeaway</span>
                  )}

                  {selectedRestaurant.parking && (
                    <span>✓ Parking</span>
                  )}

                  {selectedRestaurant.stags_allowed && (
                    <span>✓ Stags Allowed</span>
                  )}

                  {selectedRestaurant.luxury_dining && (
                    <span>✓ Luxury Dining</span>
                  )}

                  {selectedRestaurant.indoor_seating && (
                    <span>✓ Indoor Seating</span>
                  )}

                  {selectedRestaurant.family_friendly && (
                    <span>✓ Family Friendly</span>
                  )}

                  {selectedRestaurant.kid_friendly && (
                    <span>✓ Kid Friendly</span>
                  )}

                  {selectedRestaurant.work_friendly && (
                    <span>✓ Work Friendly</span>
                  )}

                  {selectedRestaurant.free_parking && (
                    <span>✓ Free Parking</span>
                  )}

                </div>

              </div>


              {/* Links */}

              <div className="modal-actions">

                {selectedRestaurant.menu_url && (

                  <a
                    href={selectedRestaurant.menu_url}
                    target="_blank"
                    rel="noreferrer"
                    className="action-button"
                  >
                    📖 View Menu
                  </a>

                )}


                {selectedRestaurant.booking_url && (

                  <a
                    href={selectedRestaurant.booking_url}
                    target="_blank"
                    rel="noreferrer"
                    className="action-button"
                  >
                    📅 Book a Table
                  </a>

                )}


                {selectedRestaurant.direction_url && (

                  <a
                    href={selectedRestaurant.direction_url}
                    target="_blank"
                    rel="noreferrer"
                    className="action-button"
                  >
                    📍 Get Direction
                  </a>

                )}

              </div>

            </div>

          </div>

        </div>

      )}

    </div>
  );
}

export default App;