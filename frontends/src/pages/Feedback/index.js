"use client";

import { useState, useEffect } from "react";
import Navbar from "../../components/Navbar/Navbar";
import { motion } from "framer-motion";
import { Star } from "lucide-react";

export default function Feedback() {
  const [feedbackList, setFeedbackList] = useState([]);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    description: "",
    rating: 0,
    suggestions: "",
  });

  // Fetch existing feedback from the API
  const getAllFeedbacks = async () => {
    try {
      const response = await fetch("http://localhost:4000/api/feedback/getAllFeedbacks");
      const data = await response.json();
      console.log("Fetched feedback data:", data);
      setFeedbackList(data || []);
    } catch (error) {
      console.error("Error fetching feedback:", error);
    }
  };
  useEffect(() => {
    getAllFeedbacks();
    console.log("Feedbacks fetched successfully!");
  }, []);

  // Handle input change
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle rating selection
  const handleRating = (newRating) => {
    setFormData((prev) => ({ ...prev, rating: newRating }));
  };

  // Handle form submission (POST request)
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.name || !formData.description) {
      alert("Name and Description are required!");
      return;
    }

    try {
      const response = await fetch("http://localhost:4000/api/feedback/addFeedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      if (response.ok) {
        // setFeedbackList([formData, ...feedbackList]); // Add new feedback to UI
        getAllFeedbacks();
        setFormData({ name: "", email: "", description: "", rating: 0, suggestions: "" }); // Reset form
      } else {
        console.error("Error submitting feedback:", result.error);
      }
    } catch (error) {
      console.error("Network error:", error);
    }
  };

  return (
    <>
      <Navbar />
      <div className="bg-gradient-to-b from-green-50 to-white min-h-screen py-12 px-6">
        {/* Feedback Form */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="max-w-2xl mx-auto bg-white shadow-lg rounded-xl p-6 border border-green-200"
        >
          <h2 className="text-2xl font-semibold text-green-700 mb-4">Your Feedback Matters!</h2>
          <form onSubmit={handleSubmit} className="space-y-3">
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Full Name"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400 placeholder-gray-500 text-gray-700 text-sm"
              required
            />
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Email (optional)"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400 placeholder-gray-500 text-gray-700 text-sm"
            />
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="How is the model performing?"
              rows="3"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400 placeholder-gray-500 text-gray-700 text-sm"
              required
            ></textarea>

            {/* Star Rating */}
            <div className="flex items-center space-x-3">
              <label className="text-gray-700 font-medium text-sm">Rating:</label>
              <div className="flex space-x-1">
                {[1, 2, 3, 4, 5].map((star) => (
                  <Star
                    key={star}
                    size={24}
                    className={`cursor-pointer transition-colors ${
                      star <= formData.rating ? "text-yellow-500 fill-yellow-500" : "text-gray-400"
                    }`}
                    onClick={() => handleRating(star)}
                  />
                ))}
              </div>
            </div>

            <textarea
              name="suggestions"
              value={formData.suggestions}
              onChange={handleChange}
              placeholder="Any suggestions?"
              rows="2"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400 placeholder-gray-500 text-gray-700 text-sm"
            ></textarea>

            <button
              type="submit"
              className="w-full bg-green-600 text-white font-bold py-2 px-3 rounded-md hover:bg-green-700 transition-all duration-300 text-sm"
            >
              Submit
            </button>
          </form>
        </motion.div>

        {/* Display Feedback */}
        {feedbackList.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            viewport={{ once: true }}
            className="mt-12 max-w-4xl mx-auto"
          >
            <h2 className="text-3xl font-semibold text-green-700 mb-6">User Feedback</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {feedbackList.map((feedback, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="bg-white shadow-md rounded-xl p-4 border-l-4 border-green-600"
                >
                  <h3 className="text-lg font-bold text-gray-800">{feedback.name}</h3>
                  <p className="text-gray-600">{feedback.description}</p>
                  <div className="flex items-center">
                    <p className="text-gray-500">⭐ Rating: </p>
                    <div className="flex space-x-1 ml-1">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <Star
                          key={star}
                          size={18}
                          className={star <= feedback.rating ? "text-yellow-500 fill-yellow-500" : "text-gray-400"}
                        />
                      ))}
                    </div>
                  </div>
                  {feedback.suggestions && (
                    <p className="text-sm text-gray-500 italic">"{feedback.suggestions}"</p>
                  )}
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </>
  );
}
