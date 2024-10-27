import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Welcome from "./compoenents/Welcome";
import LoginPage from "./compoenents/LoginPage";
import AuthPage from "./compoenents/AuthPage";

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="login" element={<LoginPage />} />
          <Route path="/" element={<AuthPage />}>
            <Route path="/welcome-page" element={<Welcome />} />
          </Route>
        </Routes>
      </div>
    </Router>
  );
};

export default App;
