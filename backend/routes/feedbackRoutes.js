const express = require('express');
const router = express.Router();

const Feedback = require('../models/feedback'); // Adjust the path if needed

// POST: Submit feedback
router.post('/addFeedback', async (req, res) => {
  try {
    const { name, email, description, rating, suggestions } = req.body;

    if (!name || !email || rating === undefined) {
      return res.status(400).json({ message: "Missing required fields" });
    }

    const newFeedback = new Feedback({
      name,
      email,
      description,
      rating,
      suggestions,
    });

    const savedFeedback = await newFeedback.save();
    res.status(201).json({ message: "Feedback submitted successfully", feedback: savedFeedback });
  } catch (error) {
    res.status(500).json({ message: "Server error", error: error.message });
  }
});

// GET: All feedbacks
router.get('/getAllFeedbacks', async (req, res) => {
  try {
    const feedbacks = await Feedback.find().sort({ submittedAt: -1 });
    res.json(feedbacks);
  } catch (error) {
    res.status(500).json({ message: "Error fetching feedbacks", error: error.message });
  }
});

module.exports = router;
